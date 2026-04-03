from pydantic import BaseModel
from typing import Optional, List

class RawBrief(BaseModel):
    row_id: str
    brand_name: str
    content_type: str
    topic: str
    key_message: Optional[str]
    target_audience: Optional[str]
    mandatory_inclusions: Optional[str]
    reference_urls: Optional[str]
    free_text_notes: Optional[str]

class BrandContext(BaseModel):
    tone_of_voice: str
    past_themes: List[str]
    client_rules: List[str]
    similarity_score: float

class InterpretedBrief(BaseModel):
    hook_options: List[str]          # 2-3 ranked hooks
    tone_direction: str
    visual_treatment: str
    scriptwriter_notes: str
    one_line_summary: str
    ambiguity_flags: List[str]       # empty list = confident
    confidence_score: float          # 0.0 to 1.0

class AgentState(BaseModel):
    raw_brief: Optional[RawBrief] = None
    brand_context: Optional[BrandContext] = None
    interpreted_brief: Optional[InterpretedBrief] = None
    assigned_scriptwriter: Optional[str] = None
    notion_page_url: Optional[str] = None
    airtable_record_id: Optional[str] = None
    error: Optional[str] = None
    flagged: bool = False
    flag_reason: Optional[str] = None