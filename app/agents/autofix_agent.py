import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# ============================================================
# 1. Load environment variables
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found in the .env file."
    )


# ============================================================
# 2. Create Gemini AI model
# ============================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=api_key,
    temperature=0.1
)


# ============================================================
# 3. AI Auto-Fix Agent
# ============================================================

def generate_code_fix(
    code: str,
    language: str,
    findings: list
):
    """
    Generate an improved version of the submitted source code.

    The agent receives:
    - Original source code
    - Programming language
    - Findings from the multi-agent review

    It returns:
    - Improved source code
    - Explanation of the changes
    """

    # --------------------------------------------------------
    # Convert findings into readable text
    # --------------------------------------------------------

    findings_text = ""

    if findings:

        for index, finding in enumerate(
            findings,
            start=1
        ):

            title = finding.get(
                "title",
                "Issue"
            )

            category = finding.get(
                "category",
                "General"
            )

            severity = finding.get(
                "severity",
                "INFO"
            )

            description = finding.get(
                "description",
                ""
            )

            recommendation = finding.get(
                "recommendation",
                ""
            )

            findings_text += f"""
Finding {index}:
Title: {title}
Category: {category}
Severity: {severity}
Description: {description}
Recommendation: {recommendation}

"""

    else:

        findings_text = """
No specific findings were provided.
Review the code for general bugs, security,
performance, and code-quality problems.
"""


    # ========================================================
    # 4. Create Auto-Fix prompt
    # ========================================================

    prompt = f"""
You are an expert AI Code Repair Agent.

Your task is to improve and repair the following
{language} source code.

The code was previously analyzed by multiple
specialized AI code-review agents.

Your responsibilities are:

1. Fix confirmed bugs.
2. Fix security vulnerabilities.
3. Improve performance where appropriate.
4. Improve code quality and readability.
5. Preserve the original functionality.
6. Do not remove important functionality.
7. Do not invent unnecessary features.
8. Do not introduce new security vulnerabilities.
9. Keep the solution understandable for a developer.
10. Make sure the resulting code is syntactically valid.

IMPORTANT:
- Only make changes that are useful or necessary.
- Do not simply rewrite the entire program unnecessarily.
- Preserve the original programming language.
- Do not include Markdown code fences around the final code.

Return your response using EXACTLY this format:

EXPLANATION:
Give a short explanation of the important changes.

CHANGES:
List the main fixes that were applied.

FIXED_CODE:
Provide the complete corrected source code.

ORIGINAL CODE:

{code}

LANGUAGE:

{language}

AI REVIEW FINDINGS:

{findings_text}
"""


    # ========================================================
    # 5. Send request to Gemini
    # ========================================================

    response = llm.invoke(prompt)


    # ========================================================
    # 6. Extract Gemini response
    # ========================================================

    response_text = response.content


    # Some Gemini responses can be returned as a list
    # of content blocks. Convert them into plain text.

    if isinstance(
        response_text,
        list
    ):

        text_parts = []

        for part in response_text:

            if isinstance(
                part,
                dict
            ):

                text_parts.append(
                    str(
                        part.get(
                            "text",
                            ""
                        )
                    )
                )

            else:

                text_parts.append(
                    str(part)
                )

        response_text = "\n".join(
            text_parts
        )


    # ========================================================
    # 7. Parse the AI response
    # ========================================================

    explanation = ""
    changes = ""
    fixed_code = response_text


    if "EXPLANATION:" in response_text:

        explanation_part = response_text.split(
            "EXPLANATION:",
            1
        )[1]

        if "CHANGES:" in explanation_part:

            explanation = explanation_part.split(
                "CHANGES:",
                1
            )[0].strip()


    if "CHANGES:" in response_text:

        changes_part = response_text.split(
            "CHANGES:",
            1
        )[1]

        if "FIXED_CODE:" in changes_part:

            changes = changes_part.split(
                "FIXED_CODE:",
                1
            )[0].strip()


    if "FIXED_CODE:" in response_text:

        fixed_code = response_text.split(
            "FIXED_CODE:",
            1
        )[1].strip()


    # --------------------------------------------------------
    # Remove Markdown code fences if Gemini adds them
    # --------------------------------------------------------

    if fixed_code.startswith(
        "```"
    ):

        lines = fixed_code.splitlines()

        if lines:

            lines = lines[1:]

        if lines and lines[-1].strip() == "```":

            lines = lines[:-1]

        fixed_code = "\n".join(
            lines
        ).strip()


    # ========================================================
    # 8. Return structured result
    # ========================================================

    return {

        "explanation": explanation,

        "changes": changes,

        "fixed_code": fixed_code
    }