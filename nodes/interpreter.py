from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from schemas import AgentState, InterpretedBrief
import json

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

INTERPRET_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a senior content strategist at a short-form video agency.
You will receive a client brief and brand context. Your job is to rewrite it into
an internal creative brief that a scriptwriter can act on immediately.

Return ONLY a valid JSON object with these exact keys:
- hook_options: array of exactly 3 strings, ranked best to weakest
- tone_direction: string describing the tone and energy of the piece
- visual_treatment: string describing the visual style suggestion
- scriptwriter_notes: string with specific guidance for the writer
- one_line_summary: string, max 15 words summarising the brief
- ambiguity_flags: array of strings describing unclear areas (empty array if none)
- confidence_score: float between 0.0 and 1.0

Confidence score rules:
- 0.9+ : all fields clear, strong brand context match
- 0.7-0.9 : minor gaps but enough to proceed
- below 0.7 : significant ambiguity, flag for coordinator

Return ONLY the JSON. No markdown. No explanation.
"""),
    ("human", """CLIENT BRIEF
Brand: {brand_name}
Content type: {content_type}
Topic: {topic}
Key message: {key_message}
Target audience: {target_audience}
Mandatory inclusions: {mandatory_inclusions}
Reference URLs: {reference_urls}
Additional notes: {notes}

BRAND CONTEXT
Tone of voice: {tone_of_voice}
Past themes: {past_themes}
Client rules: {client_rules}
""")
])

CONFIDENCE_THRESHOLD = 0.70

def interpret_brief(state: AgentState) -> AgentState:
    if state.flagged:
        return state

    raw = state.raw_brief
    ctx = state.brand_context

    chain = INTERPRET_PROMPT | llm
    response = chain.invoke({
        "brand_name":           raw.brand_name,
        "content_type":         raw.content_type,
        "topic":                raw.topic,
        "key_message":          raw.key_message or "",
        "target_audience":      raw.target_audience or "",
        "mandatory_inclusions": raw.mandatory_inclusions or "",
        "reference_urls":       raw.reference_urls or "",
        "notes":                raw.free_text_notes or "",
        "tone_of_voice":        ctx.tone_of_voice,
        "past_themes":          ", ".join(ctx.past_themes),
        "client_rules":         ", ".join(ctx.client_rules),
    })

    try:
        data = json.loads(response.content.strip())
    except json.JSONDecodeError:
        return state.model_copy(update={
            "flagged": True,
            "flag_reason": "Interpreter returned malformed response — manual review needed."
        })

    interpreted = InterpretedBrief(**data)

    if interpreted.confidence_score < CONFIDENCE_THRESHOLD:
        flags = "; ".join(interpreted.ambiguity_flags) or "Low confidence — reason unclear"
        return state.model_copy(update={
            "interpreted_brief": interpreted,
            "flagged": True,
            "flag_reason": f"Low confidence ({interpreted.confidence_score:.2f}): {flags}"
        })

    return state.model_copy(update={"interpreted_brief": interpreted})