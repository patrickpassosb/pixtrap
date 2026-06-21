import json
import time
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Set
from pathlib import Path
from pixtrap import config
from pixtrap.dataset import PromptRecord
from pixtrap.providers import ProviderClient

logger = logging.getLogger(__name__)

class EvaluationRunner:
    def __init__(self, run_id: str, model_configs: List[Dict[str, Any]], prompt_records: List[PromptRecord], force: bool = False, resume: bool = False):
        self.run_id = run_id
        self.model_configs = model_configs
        self.prompt_records = prompt_records
        self.force = force
        self.resume = resume
        
        self.output_dir = config.RESULTS_RAW_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.output_file = self.output_dir / f"results_{run_id}.jsonl"
        
        self.client = ProviderClient()
        self.completed_pairs = self._load_completed_pairs()

    def _load_completed_pairs(self) -> Set[tuple]:
        """Load already completed prompt/model pairs from output file if resuming."""
        completed = set()
        if not self.resume or not self.output_file.exists():
            return completed

        with open(self.output_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    if data.get("status") == "completed":
                        completed.add((data.get("prompt_id"), data.get("model_key")))
                except Exception as e:
                    logger.warning(f"Error reading line from output file: {e}")
        return completed

    def run(self):
        """Execute the evaluation run."""
        # Create output file if it doesn't exist, or keep it if resuming
        if not self.output_file.exists():
            with open(self.output_file, "w", encoding="utf-8") as f:
                pass

        total_runs = len(self.prompt_records) * len(self.model_configs)
        attempted = 0
        skipped = 0

        for prompt in self.prompt_records:
            for model in self.model_configs:
                model_key = model.get("id")
                # Skip disabled models
                if not model.get("enabled", True):
                    continue

                pair = (prompt.id, model_key)
                if pair in self.completed_pairs and not self.force:
                    skipped += 1
                    continue

                attempted += 1
                started_at = datetime.now(timezone.utc).isoformat()
                
                # Model query with retries
                retry_count = 0
                res = None
                while retry_count < config.PIXTRAP_MAX_RETRIES:
                    res = self.client.complete(model_config=model, prompt_text=prompt.prompt)
                    status = res.get("status")
                    if status == "completed":
                        break
                    
                    # If rate limited or similar, wait and retry
                    if status in ["rate_limited", "timeout"]:
                        retry_count += 1
                        wait_sec = 2 ** retry_count
                        logger.warning(f"Run rate limited or timed out. Waiting {wait_sec}s to retry ({retry_count}/{config.PIXTRAP_MAX_RETRIES})...")
                        time.sleep(wait_sec)
                    else:
                        break # Don't retry API errors or other hard errors

                completed_at = datetime.now(timezone.utc).isoformat()
                
                # Prepare run record
                run_record = {
                    "run_id": self.run_id,
                    "prompt_id": prompt.id,
                    "model_key": model_key,
                    "provider": model.get("provider"),
                    "model_id": model.get("model_id"),
                    "canonical_model": model.get("canonical_model"),
                    "language": prompt.language,
                    "category": prompt.category,
                    "safety_label": prompt.safety_label,
                    "expected_behavior": prompt.expected_behavior,
                    "status": res.get("status", "api_error"),
                    "retry_count": retry_count,
                    "started_at": started_at,
                    "completed_at": completed_at,
                    "prompt_text": prompt.prompt,
                    "output_text": res.get("output_text", ""),
                    "usage": res.get("usage"),
                    "error": res.get("error")
                }

                # Save record immediately
                with open(self.output_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(run_record, ensure_ascii=False) + "\n")

                print(f"[{attempted + skipped}/{total_runs}] Model {model_key} - Prompt {prompt.id}: {res.get('status')}")
                
                # Concurrency rate limiting delay
                if config.PIXTRAP_MAX_CONCURRENCY == 1:
                    time.sleep(1.0)

        print(f"Run completed: {attempted} calls executed, {skipped} skipped, {len(self.model_configs) * len(self.prompt_records)} total pairs.")
