import os
import json

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# ============================================
# 1. Load environment variables
# ============================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found in the .env file."
    )


# ============================================
# 2. Create Gemini model
# ============================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=api_key,
    temperature=0.1
)


# ============================================
# 3. Bug Detection Agent
# ============================================

def bug_detection_agent(code: str, language: str):

    prompt = f"""
You are a specialized AI Bug Detection Agent.

Your ONLY responsibility is to analyze source code for:

1. Syntax-related problems
2. Runtime errors
3. Logical errors
4. Incorrect conditions
5. Incorrect loops
6. Array or collection indexing errors
7. Null or None related problems
8. Incorrect variable usage
9. Exception-prone code
10. Other bugs that could cause incorrect program behavior

Do NOT focus on:
- Security vulnerabilities
- Performance optimization
- General code style

Those will be handled by other specialized agents.

For every bug you identify, provide:

- title
- severity
- line
- description
- recommendation

Severity must be one of:

CRITICAL
HIGH
MEDIUM
LOW
INFO

Use the actual source-code line number whenever possible.

If you cannot determine the exact line number, use null.

Return ONLY valid JSON.

Do NOT use Markdown.
Do NOT use ```json.
Do NOT add explanations outside the JSON.

Use exactly this structure:

{{
    "agent": "Bug Detection Agent",

    "bugs": [
        {{
            "title": "Example bug",
            "severity": "HIGH",
            "line": 10,
            "description": "Explain the bug clearly.",
            "recommendation": "Explain how to fix it."
        }}
    ],

    "summary": "Short summary of the bug analysis."
}}

If no bugs are found, return:

{{
    "agent": "Bug Detection Agent",
    "bugs": [],
    "summary": "No obvious bugs were found."
}}

Programming language:

{language}

Source code:

{code}
"""

    # ========================================
    # Send code to Gemini
    # ========================================

    response = llm.invoke(prompt)

    content = response.content

    # Gemini may return content as a list
    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, dict) and "text" in item:
                text_parts.append(item["text"])

            else:
                text_parts.append(str(item))

        content = "\n".join(text_parts)

    else:

        content = str(content)


    # ========================================
    # Clean Gemini response
    # ========================================

    cleaned = content.strip()

    if cleaned.startswith("```"):

        lines = cleaned.splitlines()

        if lines:
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        cleaned = "\n".join(lines).strip()


    # ========================================
    # Parse JSON
    # ========================================

    try:

        result = json.loads(cleaned)

        return result

    except json.JSONDecodeError:

        # Try to find JSON inside the response

        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start != -1 and end != -1:

            try:

                result = json.loads(
                    cleaned[start:end + 1]
                )

                return result

            except json.JSONDecodeError:
                pass


    # ========================================
    # Fallback response
    # ========================================

    return {
        "agent": "Bug Detection Agent",
        "bugs": [],
        "summary": "The bug analysis could not be parsed."
    }