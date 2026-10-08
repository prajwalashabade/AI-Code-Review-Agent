import os
import json
from typing_extensions import TypedDict

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END


# ============================================
# 1. Load environment variables
# ============================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in the .env file.")


# ============================================
# 2. Create Gemini AI model
# ============================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=api_key,
    temperature=0.2
)


# ============================================
# 3. Define the agent state
# ============================================

class CodeReviewState(TypedDict):
    code: str
    language: str
    review: str
    score: int
    risk_level: str
    findings: list
    recommendations: list
    improved_code: str


# ============================================
# 4. Extract text from Gemini response
# ============================================

def extract_response_text(response):

    content = response.content

    # Gemini/LangChain may return a list
    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, dict) and "text" in item:
                text_parts.append(item["text"])

            else:
                text_parts.append(str(item))

        return "\n".join(text_parts)

    return str(content)


# ============================================
# 5. Parse structured AI response
# ============================================

def parse_ai_response(text):

    cleaned = text.strip()

    # Remove Markdown code fences if Gemini adds them
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()

        if lines:
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        cleaned = "\n".join(lines).strip()

    try:
        return json.loads(cleaned)

    except json.JSONDecodeError:

        # Try to locate the JSON object
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start != -1 and end != -1 and end > start:

            possible_json = cleaned[start:end + 1]

            try:
                return json.loads(possible_json)

            except json.JSONDecodeError:
                pass

    return None


# ============================================
# 6. Convert structured result into readable report
# ============================================

def create_readable_review(data):

    lines = []

    lines.append("OVERALL ASSESSMENT:")
    lines.append(data.get("overall_assessment", "No assessment provided."))
    lines.append("")

    lines.append(
        f"CODE HEALTH SCORE: "
        f"{data.get('score', 0)}/100"
    )

    lines.append(
        f"RISK LEVEL: "
        f"{data.get('risk_level', 'UNKNOWN')}"
    )

    lines.append("")

    lines.append("FINDINGS:")

    findings = data.get("findings", [])

    if not findings:

        lines.append("No significant findings detected.")

    else:

        for index, finding in enumerate(findings, start=1):

            lines.append(f"{index}. {finding.get('title', 'Issue')}")
            lines.append(
                f"   Category: {finding.get('category', 'General')}"
            )
            lines.append(
                f"   Severity: {finding.get('severity', 'UNKNOWN')}"
            )
            lines.append(
                f"   Line: {finding.get('line', 'Not specified')}"
            )
            lines.append(
                f"   Problem: {finding.get('description', '')}"
            )
            lines.append(
                f"   Recommendation: {finding.get('recommendation', '')}"
            )
            lines.append("")

    lines.append("RECOMMENDATIONS:")

    recommendations = data.get("recommendations", [])

    if not recommendations:

        lines.append("No additional recommendations.")

    else:

        for index, recommendation in enumerate(
            recommendations,
            start=1
        ):

            lines.append(
                f"{index}. {recommendation}"
            )

    lines.append("")

    lines.append("IMPROVED CODE:")
    lines.append(
        data.get(
            "improved_code",
            "No improved code provided."
        )
    )

    return "\n".join(lines)


# ============================================
# 7. AI Code Review function
# ============================================

def review_code(state: CodeReviewState):

    code = state["code"]
    language = state["language"]

    prompt = f"""
You are an expert AI Code Review Agent.

Analyze the following {language} source code.

Your job is to identify programming problems and provide
practical improvements.

Analyze:

1. Bugs and runtime errors
2. Security vulnerabilities
3. Performance problems
4. Code quality issues
5. Maintainability problems
6. Best-practice violations

For every important finding, provide:

- title
- category
- severity
- line number
- description
- recommendation

Severity must be one of:

CRITICAL
HIGH
MEDIUM
LOW
INFO

Also calculate:

- score: integer from 0 to 100
- risk_level: LOW, MEDIUM, HIGH, or CRITICAL

The score should represent the overall health of the code.
Higher score means better code quality and lower risk.

IMPORTANT:
Use the actual line numbers from the supplied code whenever
possible. If the exact line cannot be determined, use null.

Return ONLY valid JSON.

Do NOT use Markdown.
Do NOT use ```json.
Do NOT add explanations outside the JSON.

Use exactly this JSON structure:

{{
    "overall_assessment": "Short overall assessment",

    "score": 75,

    "risk_level": "MEDIUM",

    "findings": [
        {{
            "title": "Example issue",
            "category": "Bug",
            "severity": "HIGH",
            "line": 10,
            "description": "Explain the problem",
            "recommendation": "Explain how to fix it"
        }}
    ],

    "recommendations": [
        "Recommendation 1",
        "Recommendation 2"
    ],

    "improved_code": "Complete improved version of the code"
}}

If there are no findings, return an empty findings array.

Code to review:

{code}
"""

    # Send code to Gemini
    response = llm.invoke(prompt)

    # Extract text from Gemini response
    response_text = extract_response_text(response)

    # Parse JSON
    structured_result = parse_ai_response(response_text)

    # ========================================
    # Fallback if JSON parsing fails
    # ========================================

    if structured_result is None:

        return {
            "review": response_text,
            "score": 0,
            "risk_level": "UNKNOWN",
            "findings": [],
            "recommendations": [],
            "improved_code": ""
        }

    # ========================================
    # Create readable report
    # ========================================

    readable_review = create_readable_review(
        structured_result
    )

    return {
        "review": readable_review,
        "score": structured_result.get("score", 0),
        "risk_level": structured_result.get(
            "risk_level",
            "UNKNOWN"
        ),
        "findings": structured_result.get(
            "findings",
            []
        ),
        "recommendations": structured_result.get(
            "recommendations",
            []
        ),
        "improved_code": structured_result.get(
            "improved_code",
            ""
        )
    }


# ============================================
# 8. Create LangGraph workflow
# ============================================

graph_builder = StateGraph(CodeReviewState)


# Add AI review node
graph_builder.add_node(
    "review_code",
    review_code
)


# Start → AI Review
graph_builder.add_edge(
    START,
    "review_code"
)


# AI Review → End
graph_builder.add_edge(
    "review_code",
    END
)


# Compile the agent
code_review_agent = graph_builder.compile()