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
# 3. Security Detection Agent
# ============================================

def security_detection_agent(code: str, language: str):

    prompt = f"""
You are a specialized AI Security Detection Agent.

Your ONLY responsibility is to analyze source code
for security vulnerabilities.

Look specifically for:

1. Hardcoded passwords or credentials
2. API keys or secret keys
3. SQL injection
4. Command injection
5. Unsafe user input handling
6. Authentication problems
7. Authorization problems
8. Sensitive information exposure
9. Insecure file operations
10. Weak cryptographic practices
11. Unsafe deserialization
12. Cross-site scripting risks
13. Insecure configuration
14. Other serious security vulnerabilities

Do NOT focus on:

- General programming bugs
- Performance optimization
- Code style

Those will be handled by other specialized agents.

For every security issue, provide:

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
    "agent": "Security Detection Agent",

    "vulnerabilities": [
        {{
            "title": "Example vulnerability",
            "severity": "HIGH",
            "line": 10,
            "description": "Explain the security problem clearly.",
            "recommendation": "Explain how to fix the security problem."
        }}
    ],

    "summary": "Short summary of the security analysis."
}}

If no security vulnerabilities are found, return:

{{
    "agent": "Security Detection Agent",
    "vulnerabilities": [],
    "summary": "No obvious security vulnerabilities were found."
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
        "agent": "Security Detection Agent",
        "vulnerabilities": [],
        "summary": "The security analysis could not be parsed."
    }