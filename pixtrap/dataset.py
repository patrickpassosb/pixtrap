import json
from typing import Literal, Optional, List
from pydantic import BaseModel, Field, field_validator

# Allowed categories and types
CATEGORIES = [
    "impersonation_false_authority",
    "urgency_coercion",
    "transaction_receipt_fraud",
    "recovery_support_scams",
    "benign_near_neighbors",
]

ATTACK_TYPES = [
    "direct_misuse_request",
    "rewriting_request",
    "roleplay_framing",
    "indirect_polite_malicious_framing",
    "pressure_urgency_optimization",
]

BENIGN_TYPES = [
    "anti_fraud_education",
    "victim_support",
    "consumer_protection",
    "bank_fintech_compliance",
    "journalism_research",
    "security_awareness_training",
]

class PromptRecord(BaseModel):
    id: str = Field(..., description="Unique prompt identifier")
    language: Literal["pt-BR", "en"] = Field(..., description="Language of the prompt")
    category: str = Field(..., description="Taxonomy category")
    attack_type: Optional[str] = Field(None, description="Type of attack if harmful")
    safety_label: Literal["harmful", "benign_near_neighbor"] = Field(..., description="Harmful vs benign label")
    paired_with: Optional[str] = Field(None, description="ID of the paired prompt (if any)")
    english_pair_id: Optional[str] = Field(None, description="ID of the English matched baseline prompt (if any)")
    difficulty: Literal["easy", "medium", "hard"] = Field(..., description="Difficulty level")
    prompt: str = Field(..., description="Prompt text")
    expected_behavior: Literal["refuse_and_redirect", "comply_safely"] = Field(..., description="Expected safe behavior")
    public_release: bool = Field(..., description="Whether the raw prompt is safe for public release")
    notes: Optional[str] = Field(None, description="Explanatory notes")

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: str) -> str:
        if value not in CATEGORIES:
            raise ValueError(f"Category '{value}' must be one of {CATEGORIES}")
        return value

    @field_validator("attack_type")
    @classmethod
    def validate_attack_type(cls, value: Optional[str], info) -> Optional[str]:
        if value is None:
            return value
        # Normalize slashes or spaces to underscores if needed, or check exact list
        # We will support the spec types, normalized to snake_case or as exact strings.
        # Let's map spec strings to standard names to be flexible but structured.
        valid_attacks = ATTACK_TYPES + [
            "direct misuse request",
            "rewriting request",
            "roleplay framing",
            "indirect/polite malicious framing",
            "pressure/urgency optimization"
        ]
        if value not in valid_attacks and value not in BENIGN_TYPES and value not in [
            "anti-fraud education",
            "victim support",
            "consumer protection",
            "bank or fintech compliance",
            "journalism or research",
            "security awareness training"
        ]:
            raise ValueError(f"attack_type or benign_type '{value}' is not recognized")
        return value

def load_dataset(file_path: str) -> List[PromptRecord]:
    """Load and validate a JSONL dataset of prompts."""
    records = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                record = PromptRecord(**data)
                records.append(record)
            except Exception as e:
                raise ValueError(f"Error validating line {line_num} in {file_path}: {e}")
    return records
