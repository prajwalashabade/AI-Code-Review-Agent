from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.agents.multi_agent import multi_agent_code_reviewer
from app.agents.autofix_agent import generate_code_fix


# ============================================================
# 1. Create FastAPI application
# ============================================================

app = FastAPI(
    title="AI Code Review Agent",
    description="Multi-Agent AI Code Review System",
    version="3.0.0"
)


# ============================================================
# 2. Enable CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# 3. Request model for code review
# ============================================================

class CodeReviewRequest(BaseModel):

    code: str
    language: str


# ============================================================
# 4. Request model for AI Auto-Fix
# ============================================================

class AutoFixRequest(BaseModel):

    code: str
    language: str

    findings: list[dict[str, Any]] = Field(
        default_factory=list
    )


# ============================================================
# 5. Home endpoint
# ============================================================

@app.get("/")
def home():

    return {
        "message": "AI Code Review Agent is running!",
        "version": "Multi-Agent LangGraph + AI Auto-Fix"
    }


# ============================================================
# 6. Review endpoint
# ============================================================

@app.post("/review")
def review_code(request: CodeReviewRequest):

    # --------------------------------------------------------
    # Run the LangGraph multi-agent workflow
    # --------------------------------------------------------

    result = multi_agent_code_reviewer.invoke({

        "code": request.code,

        "language": request.language
    })


    # --------------------------------------------------------
    # Get the final report
    # --------------------------------------------------------

    report = result.get(
        "final_report",
        {}
    )


    # --------------------------------------------------------
    # Extract findings
    # --------------------------------------------------------

    bugs = report.get(
        "bugs",
        []
    )

    security_vulnerabilities = report.get(
        "security_vulnerabilities",
        []
    )

    performance_issues = report.get(
        "performance_issues",
        []
    )

    quality_issues = report.get(
        "quality_issues",
        []
    )


    # --------------------------------------------------------
    # Combine all findings
    # --------------------------------------------------------

    findings = []

    findings.extend(
        bugs
    )

    findings.extend(
        security_vulnerabilities
    )

    findings.extend(
        performance_issues
    )

    findings.extend(
        quality_issues
    )


    # --------------------------------------------------------
    # Create recommendations
    # --------------------------------------------------------

    recommendations = []

    for finding in findings:

        recommendation = finding.get(
            "recommendation"
        )

        if recommendation:

            recommendations.append(
                recommendation
            )


    # --------------------------------------------------------
    # Create readable overall review
    # --------------------------------------------------------

    review_parts = []

    review_parts.append(
        "Multi-agent analysis completed successfully."
    )

    review_parts.append(
        f"Code Health Score: "
        f"{report.get('code_health_score', 0)}/100"
    )

    review_parts.append(
        f"Risk Level: "
        f"{report.get('risk_level', 'UNKNOWN')}"
    )

    review_parts.append(
        f"Total Findings: "
        f"{report.get('total_findings', 0)}"
    )


    review_text = "\n".join(
        review_parts
    )


    # --------------------------------------------------------
    # Return response to frontend
    # --------------------------------------------------------

    return {

        "language": request.language,

        "review": review_text,

        "score": report.get(
            "code_health_score",
            0
        ),

        "risk_level": report.get(
            "risk_level",
            "UNKNOWN"
        ),

        "total_findings": report.get(
            "total_findings",
            len(findings)
        ),

        "findings": findings,

        "bugs": bugs,

        "security_vulnerabilities":
            security_vulnerabilities,

        "performance_issues":
            performance_issues,

        "quality_issues":
            quality_issues,

        "recommendations":
            recommendations,

        "agent_summaries":
            report.get(
                "agent_summaries",
                {}
            )
    }


# ============================================================
# 7. AI Auto-Fix endpoint
# ============================================================

@app.post("/autofix")
def autofix_code(request: AutoFixRequest):

    # --------------------------------------------------------
    # Send original code and AI findings to Auto-Fix Agent
    # --------------------------------------------------------

    result = generate_code_fix(

        code=request.code,

        language=request.language,

        findings=request.findings
    )


    # --------------------------------------------------------
    # Return the improved code
    # --------------------------------------------------------

    return {

        "language": request.language,

        "explanation":
            result.get(
                "explanation",
                ""
            ),

        "changes":
            result.get(
                "changes",
                ""
            ),

        "fixed_code":
            result.get(
                "fixed_code",
                ""
            )
    }


# ============================================================
# 8. Health check endpoint
# ============================================================

@app.get("/health")
def health_check():

    return {

        "status": "healthy",

        "service":
            "AI Code Review Agent",

        "architecture":
            "Multi-Agent LangGraph + AI Auto-Fix"
    }