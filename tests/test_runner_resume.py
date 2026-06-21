import pytest
from unittest.mock import patch, MagicMock
import httpx
from pixtrap.providers import ProviderClient

@pytest.fixture
def client():
    return ProviderClient()

def test_chat_completions_success(client):
    model_config = {
        "provider": "opencode",
        "model_id": "glm-5.2",
        "endpoint_type": "chat_completions",
        "max_output_tokens": 100,
        "temperature": 0.0
    }
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{
            "message": {"content": "Olá, sou o GLM."},
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 5,
            "total_tokens": 15
        }
    }
    
    with patch("httpx.post", return_value=mock_response) as mock_post:
        res = client.complete(model_config=model_config, prompt_text="Oi")
        assert res["status"] == "completed"
        assert res["output_text"] == "Olá, sou o GLM."
        assert res["usage"]["total_tokens"] == 15
        mock_post.assert_called_once()

def test_chat_completions_null_content_is_normalized(client):
    model_config = {
        "provider": "opencode",
        "model_id": "kimi-k2.6",
        "endpoint_type": "chat_completions",
        "max_output_tokens": 100,
        "temperature": 0.0
    }
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{
            "message": {"content": None, "reasoning": "internal reasoning"},
            "finish_reason": "length"
        }],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 5,
            "total_tokens": 15
        }
    }

    with patch("httpx.post", return_value=mock_response):
        res = client.complete(model_config=model_config, prompt_text="Oi")
        assert res["status"] == "completed"
        assert res["output_text"] == ""

def test_messages_success(client):
    model_config = {
        "provider": "opencode",
        "model_id": "minimax-m3",
        "endpoint_type": "messages",
        "max_output_tokens": 100,
        "temperature": 0.0
    }
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "content": [{"type": "text", "text": "Olá, sou o MiniMax."}],
        "stop_reason": "stop_sequence",
        "usage": {
            "input_tokens": 12,
            "output_tokens": 6
        }
    }
    
    with patch("httpx.post", return_value=mock_response) as mock_post:
        res = client.complete(model_config=model_config, prompt_text="Oi")
        assert res["status"] == "completed"
        assert res["output_text"] == "Olá, sou o MiniMax."
        assert res["usage"]["prompt_tokens"] == 12
        assert res["usage"]["completion_tokens"] == 6
        mock_post.assert_called_once()

def test_ollama_generate_success(client):
    model_config = {
        "provider": "ollama",
        "model_id": "gemma4:31b-cloud",
        "endpoint_type": "ollama_generate",
        "max_output_tokens": 100,
        "temperature": 0.0
    }
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "response": "Olá, sou o Gemma.",
        "done_reason": "stop",
        "prompt_eval_count": 8,
        "eval_count": 4
    }
    
    with patch("httpx.post", return_value=mock_response) as mock_post:
        res = client.complete(model_config=model_config, prompt_text="Oi")
        assert res["status"] == "completed"
        assert res["output_text"] == "Olá, sou o Gemma."
        assert res["usage"]["total_tokens"] == 12
        mock_post.assert_called_once()

def test_rate_limited_error(client):
    model_config = {
        "provider": "opencode",
        "model_id": "glm-5.2",
        "endpoint_type": "chat_completions"
    }
    mock_response = MagicMock()
    mock_response.status_code = 429
    mock_response.content = b'{"error": {"message": "Rate limit exceeded"}}'
    mock_response.json.return_value = {"error": {"message": "Rate limit exceeded"}}
    
    with patch("httpx.post", return_value=mock_response):
        res = client.complete(model_config=model_config, prompt_text="Oi")
        assert res["status"] == "rate_limited"
        assert res["error"]["type"] == "rate_limited"

def test_quota_exceeded_error(client):
    model_config = {
        "provider": "opencode",
        "model_id": "glm-5.2",
        "endpoint_type": "chat_completions"
    }
    mock_response = MagicMock()
    mock_response.status_code = 402
    mock_response.content = b'{"error": {"message": "Insufficient credits"}}'
    mock_response.json.return_value = {"error": {"message": "Insufficient credits"}}
    
    with patch("httpx.post", return_value=mock_response):
        res = client.complete(model_config=model_config, prompt_text="Oi")
        assert res["status"] == "quota_exceeded"

def test_timeout_error(client):
    model_config = {
        "provider": "opencode",
        "model_id": "glm-5.2",
        "endpoint_type": "chat_completions"
    }
    with patch("httpx.post", side_effect=httpx.TimeoutException("Timeout")):
        res = client.complete(model_config=model_config, prompt_text="Oi")
        assert res["status"] == "timeout"


from pixtrap.runner import EvaluationRunner
from pixtrap.dataset import PromptRecord

def test_runner_resume(tmp_path):
    # Set up temp directory for results
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    
    # Mock config to point to temp dir
    with patch("pixtrap.config.RESULTS_RAW_DIR", results_dir):
        # Create a mock output file with one completed run
        run_id = "test_run"
        output_file = results_dir / f"results_{run_id}.jsonl"
        output_file.write_text(
            '{"run_id": "test_run", "prompt_id": "p1", "model_key": "m1", "status": "completed"}\n'
        )
        
        # Define prompts and models
        prompts = [
            PromptRecord(
                id="p1", language="pt-BR", category="impersonation_false_authority",
                safety_label="harmful", difficulty="medium", prompt="p1_text",
                expected_behavior="refuse_and_redirect", public_release=False
            ),
            PromptRecord(
                id="p2", language="pt-BR", category="impersonation_false_authority",
                safety_label="harmful", difficulty="medium", prompt="p2_text",
                expected_behavior="refuse_and_redirect", public_release=False
            ),
        ]
        model_configs = [
            {"id": "m1", "provider": "opencode", "model_id": "m1", "endpoint_type": "chat_completions", "enabled": True}
        ]
        
        # Instantiate runner with resume=True
        runner = EvaluationRunner(run_id=run_id, model_configs=model_configs, prompt_records=prompts, force=False, resume=True)
        assert runner.completed_pairs == {("p1", "m1")}
        
        # Run and mock the client complete method
        with patch.object(runner.client, "complete", return_value={"status": "completed", "output_text": "resp", "usage": {}}) as mock_complete:
            # Concurrency limit sleep mock to speed up test
            with patch("time.sleep"):
                runner.run()
                # Should only call complete for p2 (since p1 is already completed)
                mock_complete.assert_called_once()
                assert mock_complete.call_args[1]["prompt_text"] == "p2_text"
