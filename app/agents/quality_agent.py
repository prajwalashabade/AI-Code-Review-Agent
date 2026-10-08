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
# 3. Code Quality Detection Agent
# ============================================

def quality_detection_agent(code: str, language: str):

    prompt = f"""
You are a specialized AI Code Quality Detection Agent.

Your ONLY responsibility is to analyze source code
for code quality, readability, maintainability,
and software engineering best-practice issues.

Look specifically for:

1. Poor variable or method names
2. Poor class names
3. Hardcoded values or magic numbers
4. Duplicate code
5. Unnecessary complexity
6. Very long methods
7. Very large classes
8. Poor separation of responsibilities
9. Lack of meaningful comments where useful
10. Excessive comments where unnecessary
11. Poor formatting or inconsistent structure
12. Unnecessary code
13. Difficult-to-maintain code
14. Violation of common programming best practices
15. Poor object-oriented design when applicable
16. Weak separation of concerns
17. Opportunities to make the code cleaner and easier to understand

Do NOT focus on:

- Runtime bugs
- Security vulnerabilities
- Performance optimization

Those will be handled by other specialized agents.

For every code-quality issue, provide:

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

If the exact line cannot be determined, use null.

Return ONLY valid JSON.

Do NOT use Markdown.
Do NOT use ```json.
Do NOT add explanations outside the JSON.

Use exactly this structure:

{{
    "agent": "Code Quality Detection Agent",

    "quality_issues": [
        {{
            "title": "Example quality issue",
            "severity": "MEDIUM",
            "line": 10,
            "description": "Explain the code-quality problem clearly.",
            "recommendation": "Explain how the code can be improved."
        }}
    ],

    "summary": "Short summary of the code quality analysis."
}}

If no significant quality issues are found, return:

{{
    "agent": "Code Quality Detection Agent",
    "quality_issues": [],
    "summary": "No significant code quality issues were found."
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
        "agent": "Code Quality Detection Agent",
        "quality_issues": [],
        "summary": "The code quality analysis could not be parsed."
    }