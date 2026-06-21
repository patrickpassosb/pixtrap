import json
import httpx
import logging
from typing import Dict, Any, Optional
from pixtrap import config

logger = logging.getLogger(__name__)

class ProviderClient:
    def __init__(self):
        # We can use a client but we will instantiate a fresh client or use httpx directly
        pass

    def _extract_chat_content(self, message: Dict[str, Any]) -> str:
        """Normalize chat-completions content across providers."""
        content = message.get("content", "")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            text_parts = []
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("type") in {"text", "output_text"} and isinstance(block.get("text"), str):
                    text_parts.append(block["text"])
                elif isinstance(block.get("content"), str):
                    text_parts.append(block["content"])
            return "".join(text_parts)
        return ""

    def _parse_response(self, resp_data: Dict[str, Any], endpoint_type: str) -> tuple:
        """Parse a successful API response into (output_text, finish_reason, usage)."""
        output_text = ""
        finish_reason = "stop"
        usage = None

        if endpoint_type == "chat_completions":
            choices = resp_data.get("choices", [])
            if choices:
                message = choices[0].get("message", {})
                output_text = self._extract_chat_content(message)
                finish_reason = choices[0].get("finish_reason", "stop")
            usage = resp_data.get("usage")

        elif endpoint_type == "messages":
            content = resp_data.get("content", [])
            if isinstance(content, list):
                text_parts = []
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
                output_text = "".join(text_parts)
            elif isinstance(content, str):
                output_text = content
            finish_reason = resp_data.get("stop_reason")
            usage_data = resp_data.get("usage", {})
            if usage_data:
                usage = {
                    "prompt_tokens": usage_data.get("input_tokens", 0),
                    "completion_tokens": usage_data.get("output_tokens", 0),
                    "total_tokens": usage_data.get("input_tokens", 0) + usage_data.get("output_tokens", 0)
                }

        elif endpoint_type == "ollama_generate":
            output_text = resp_data.get("response", "")
            finish_reason = resp_data.get("done_reason", "stop")
            prompt_eval_count = resp_data.get("prompt_eval_count", 0)
            eval_count = resp_data.get("eval_count", 0)
            usage = {
                "prompt_tokens": prompt_eval_count,
                "completion_tokens": eval_count,
                "total_tokens": prompt_eval_count + eval_count
            }

        return output_text, finish_reason, usage

    def complete(self, *, model_config: Dict[str, Any], prompt_text: str) -> Dict[str, Any]:
        provider = model_config.get("provider")
        endpoint_type = model_config.get("endpoint_type")
        model_id = model_config.get("model_id")
        max_tokens = model_config.get("max_output_tokens", 350)
        temperature = model_config.get("temperature", 0.0)

        # Retrieve API key based on provider
        api_key = ""
        if provider == "opencode":
            api_key = config.OPENCODE_API_KEY
        elif provider == "ollama":
            api_key = config.OLLAMA_API_KEY
        elif provider == "nvidia":
            api_key = config.NVIDIA_API_KEY

        # Set up URL, headers and payload based on endpoint_type
        headers = {
            "Content-Type": "application/json",
        }
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        url = ""
        payload = {}

        if endpoint_type == "chat_completions":
            if provider == "opencode":
                url = config.OPENCODE_CHAT_COMPLETIONS_URL
            elif provider == "nvidia":
                url = config.NVIDIA_CHAT_COMPLETIONS_URL
            else:
                raise ValueError(f"Unknown chat_completions provider: {provider}")

            headers["Accept"] = "application/json"
            payload = {
                "model": model_id,
                "messages": [{"role": "user", "content": prompt_text}],
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": False,
            }

        elif endpoint_type == "messages":
            if provider == "opencode":
                url = config.OPENCODE_MESSAGES_URL
            else:
                raise ValueError(f"Unknown messages provider: {provider}")

            headers["Accept"] = "application/json"
            payload = {
                "model": model_id,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [{"role": "user", "content": prompt_text}],
            }

        elif endpoint_type == "ollama_generate":
            url = config.OLLAMA_GENERATE_URL
            payload = {
                "model": model_id,
                "prompt": prompt_text,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }

        else:
            raise ValueError(f"Unknown endpoint type: {endpoint_type}")

        # Execute HTTP Request
        try:
            timeout = httpx.Timeout(config.PIXTRAP_REQUEST_TIMEOUT_SECONDS)
            response = httpx.post(url, headers=headers, json=payload, timeout=timeout)
            
            # Check for HTTP errors
            if response.status_code == 429:
                return self._error_response("rate_limited", provider, model_id, "HTTP 429: Rate Limit Exceeded", response.json() if response.content else {})
            elif response.status_code == 403:
                return self._error_response("provider_blocked", provider, model_id, "HTTP 403: Provider Blocked / Forbidden", response.json() if response.content else {})
            elif response.status_code == 402:
                return self._error_response("quota_exceeded", provider, model_id, "HTTP 402: Quota Exceeded / Payment Required", response.json() if response.content else {})
            elif response.status_code != 200:
                # Some APIs return quota errors as 400 or other codes with message
                resp_json = {}
                msg = f"HTTP {response.status_code}"
                if response.content:
                    try:
                        resp_json = response.json()
                        error_info = resp_json.get("error", {})
                        if isinstance(error_info, dict):
                            msg = error_info.get("message", msg)
                        else:
                            msg = str(error_info)
                    except Exception:
                        msg = response.text
                
                # Check common error signatures
                msg_lower = msg.lower()
                if "quota" in msg_lower or "credit" in msg_lower or "insufficient funds" in msg_lower:
                    return self._error_response("quota_exceeded", provider, model_id, msg, resp_json)
                elif "blocked" in msg_lower or "safety" in msg_lower:
                    return self._error_response("provider_blocked", provider, model_id, msg, resp_json)
                else:
                    return self._error_response("api_error", provider, model_id, f"HTTP {response.status_code}: {msg}", resp_json)

            # Success response parsing
            resp_data = response.json()
            output_text, finish_reason, usage = self._parse_response(resp_data, endpoint_type)

            # Reasoning-exhaustion guard: if chat_completions returned empty
            # visible output (likely a reasoning model that spent the entire
            # token budget on internal reasoning), retry once with a higher cap.
            if endpoint_type == "chat_completions" and not output_text:
                raised_budget = min(max_tokens * 4, 8000)
                if raised_budget > max_tokens:
                    logger.info(
                        "Empty visible output with max_tokens=%d, retrying with %d for model %s",
                        max_tokens, raised_budget, model_id,
                    )
                    payload["max_tokens"] = raised_budget
                    retry_response = httpx.post(url, headers=headers, json=payload, timeout=timeout)
                    if retry_response.status_code == 200:
                        retry_data = retry_response.json()
                        retry_text, retry_fr, retry_usage = self._parse_response(retry_data, endpoint_type)
                        if retry_text:
                            return {
                                "status": "completed",
                                "provider": provider,
                                "model_id": model_id,
                                "output_text": retry_text,
                                "finish_reason": retry_fr,
                                "usage": retry_usage,
                                "raw_response": retry_data,
                            }

            return {
                "status": "completed",
                "provider": provider,
                "model_id": model_id,
                "output_text": output_text,
                "finish_reason": finish_reason,
                "usage": usage,
                "raw_response": resp_data,
            }

        except httpx.TimeoutException as e:
            return self._error_response("timeout", provider, model_id, f"Request timeout: {e}", {})
        except Exception as e:
            return self._error_response("api_error", provider, model_id, f"API Exception: {e}", {})

    def _error_response(self, status: str, provider: str, model_id: str, message: str, raw_response: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "status": status,
            "provider": provider,
            "model_id": model_id,
            "output_text": "",
            "finish_reason": None,
            "usage": None,
            "error": {
                "type": status,
                "message": message
            },
            "raw_response": raw_response
        }
