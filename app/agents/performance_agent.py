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
# 3. Performance Detection Agent
# ============================================

def performance_detection_agent(code: str, language: str):

    prompt = f"""
You are a specialized AI Performance Detection Agent.

Your ONLY responsibility is to analyze source code
for performance and efficiency problems.

Look specifically for:

1. Unnecessary loops
2. Inefficient algorithms
3. O(n^2) or worse operations when avoidable
4. Repeated calculations
5. Unnecessary object creation
6. Inefficient string operations
7. Excessive memory usage
8. Inefficient collection usage
9. Repeated database operations
10. Repeated API or network calls
11. Blocking operations
12. Unnecessary recursion
13. Memory leaks or resource misuse
14. Other significant performance problems

Do NOT focus on:

- Security vulnerabilities
- General programming bugs
- Code formatting or style

Those will be handled by other specialized agents.

For every performance issue, provide:

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
    "agent": "Performance Detection Agent",

    "performance_issues": [
        {{
            "title": "Example performance issue",
            "severity": "MEDIUM",
            "line": 10,
            "description": "Explain the performance problem clearly.",
            "recommendation": "Explain how to improve the performance."
        }}
    ],

    "summary": "Short summary of the performance analysis."
}}

If no significant performance issues are found, return:

{{
    "agent": "Performance Detection Agent",
    "performance_issues": [],
    "summary": "No significant performance issues were found."
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
        "agent": "Performance Detection Agent",
        "performance_issues": [],
        "summary": "The performance analysis could not be parsed."
    }