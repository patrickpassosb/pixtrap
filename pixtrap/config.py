import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIGS_DIR = BASE_DIR / "configs"
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "results"
RESULTS_RAW_DIR = RESULTS_DIR / "raw"
RESULTS_SCORED_DIR = RESULTS_DIR / "scored"
RESULTS_CHARTS_DIR = RESULTS_DIR / "charts"

# API Keys
OPENCODE_API_KEY = os.getenv("OPENCODE_API_KEY", "")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")

# Endpoints
OPENCODE_CHAT_COMPLETIONS_URL = os.getenv(
    "OPENCODE_CHAT_COMPLETIONS_URL",
    "https://opencode.ai/zen/go/v1/chat/completions"
)
OPENCODE_MESSAGES_URL = os.getenv(
    "OPENCODE_MESSAGES_URL",
    "https://opencode.ai/zen/go/v1/messages"
)
OPENCODE_MODELS_URL = os.getenv(
    "OPENCODE_MODELS_URL",
    "https://opencode.ai/zen/go/v1/models"
)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "https://ollama.com")
OLLAMA_GENERATE_URL = os.getenv("OLLAMA_GENERATE_URL", "https://ollama.com/api/generate")
NVIDIA_BASE_URL = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com")
NVIDIA_CHAT_COMPLETIONS_URL = os.getenv(
    "NVIDIA_CHAT_COMPLETIONS_URL",
    "https://integrate.api.nvidia.com/v1/chat/completions"
)

# Concurrency & Retries
PIXTRAP_MAX_CONCURRENCY = int(os.getenv("PIXTRAP_MAX_CONCURRENCY", "1"))
PIXTRAP_MAX_RETRIES = int(os.getenv("PIXTRAP_MAX_RETRIES", "3"))
PIXTRAP_REQUEST_TIMEOUT_SECONDS = float(os.getenv("PIXTRAP_REQUEST_TIMEOUT_SECONDS", "90.0"))

def load_yaml_config(file_path: Path) -> dict:
    """Helper to load a YAML config file."""
    if not file_path.exists():
        raise FileNotFoundError(f"Config file not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_models_config() -> dict:
    """Load configs/models.yml."""
    return load_yaml_config(CONFIGS_DIR / "models.yml")

def get_scoring_config() -> dict:
    """Load configs/scoring.yml."""
    return load_yaml_config(CONFIGS_DIR / "scoring.yml")
