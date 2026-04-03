from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import ValidationError
from schemas import RawBrief, AgentState
import json, os

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

PARSE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a brief quality checker for a content agency.
You will receive a raw form submission. Your job is to:
1. Identify if any CRITICAL fields are missing or contain meaningless content (e.g. 'tbd', 'idk', '???', 'n/a', or just whitespace).
2. Critical fields are: brand_name, content_type, topic, key_message, target_audience.
3. Return a JSON object with two keys:
   - 'is_complete': true or false
   - 'missing_fields': list of field names that are missing or meaningless (empty list if complete)

Return ONLY the JSON object. No explanation. No markdown.
"""),
    ("human", """Raw brief submission:
Brand name: {brand_name}
Content type: {content_type}
Topic: {topic}
Key message: {key_message}
Target audience: {target_audience}
Mandatory inclusions: {mandatory_inclusions}
Reference URLs: {reference_urls}
Notes: {notes}
""")
])

def parse_brief(state: AgentState) -> AgentState:
    raw = state.raw_brief

    chain = PARSE_PROMPT | llm
    response = chain.invoke({
        "brand_name":           raw.brand_name or "",
        "content_type":         raw.content_type or "",
        "topic":                raw.topic or "",
        "key_message":          raw.key_message or "",
        "target_audience":      raw.target_audience or "",
        "mandatory_inclusions": raw.mandatory_inclusions or "",
        "reference_urls":       raw.reference_urls or "",
        "notes":                raw.free_text_notes or "",
    })

    try:
        result = json.loads(response.content.strip())
    except json.JSONDecodeError:
        # LLM returned something unparseable — treat as flagged
        return state.model_copy(update={
            "flagged": True,
            "flag_reason": "Parser could not evaluate brief quality — manual review needed."
        })

    if not result.get("is_complete", False):
        missing = ", ".join(result.get("missing_fields", []))
        return state.model_copy(update={
            "flagged": True,
            "flag_reason": f"Incomplete brief — missing or unusable fields: {missing}"
        })

    return state  # passes through unchanged if complete