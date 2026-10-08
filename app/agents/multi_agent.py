from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.agents.bug_agent import bug_detection_agent
from app.agents.security_agent import security_detection_agent
from app.agents.performance_agent import performance_detection_agent
from app.agents.quality_agent import quality_detection_agent
from app.agents.dedup_agent import deduplicate_findings


# ============================================================
# 1. Define the shared state
# ============================================================

class MultiAgentState(TypedDict, total=False):

    code: str
    language: str

    bug_result: dict
    security_result: dict
    performance_result: dict
    quality_result: dict

    final_report: dict


# ============================================================
# 2. Bug Analysis Node
# ============================================================

def run_bug_agent(state: MultiAgentState):

    result = bug_detection_agent(
        code=state["code"],
        language=state["language"]
    )

    return {
        "bug_result": result
    }


# ============================================================
# 3. Security Analysis Node
# ============================================================

def run_security_agent(state: MultiAgentState):

    result = security_detection_agent(
        code=state["code"],
        language=state["language"]
    )

    return {
        "security_result": result
    }


# ============================================================
# 4. Performance Analysis Node
# ============================================================

def run_performance_agent(state: MultiAgentState):

    result = performance_detection_agent(
        code=state["code"],
        language=state["language"]
    )

    return {
        "performance_result": result
    }


# ============================================================
# 5. Code Quality Analysis Node
# ============================================================

def run_quality_agent(state: MultiAgentState):

    result = quality_detection_agent(
        code=state["code"],
        language=state["language"]
    )

    return {
        "quality_result": result
    }


# ============================================================
# 6. Final Report Node
# ============================================================

def create_final_report(state: MultiAgentState):

    # --------------------------------------------------------
    # Get results from each specialized agent
    # --------------------------------------------------------

    bug_result = state.get(
        "bug_result",
        {}
    )

    security_result = state.get(
        "security_result",
        {}
    )

    performance_result = state.get(
        "performance_result",
        {}
    )

    quality_result = state.get(
        "quality_result",
        {}
    )


    # --------------------------------------------------------
    # Safely collect findings
    # --------------------------------------------------------

    bugs = bug_result.get(
        "bugs",
        []
    ) or []

    vulnerabilities = security_result.get(
        "vulnerabilities",
        []
    ) or []

    performance_issues = performance_result.get(
        "performance_issues",
        []
    ) or []

    quality_issues = quality_result.get(
        "quality_issues",
        []
    ) or []


    # --------------------------------------------------------
    # Remove duplicate findings from each category
    # --------------------------------------------------------

    bugs = deduplicate_findings(bugs)

    vulnerabilities = deduplicate_findings(
        vulnerabilities
    )

    performance_issues = deduplicate_findings(
        performance_issues
    )

    quality_issues = deduplicate_findings(
        quality_issues
    )


    # --------------------------------------------------------
    # Combine all unique findings
    # --------------------------------------------------------

    all_findings = (
        bugs
        + vulnerabilities
        + performance_issues
        + quality_issues
    )


    # --------------------------------------------------------
    # Remove duplicates across all agents
    # --------------------------------------------------------

    all_findings = deduplicate_findings(
        all_findings
    )


    # --------------------------------------------------------
    # Count total findings
    # --------------------------------------------------------

    total_findings = len(
        all_findings
    )


    # --------------------------------------------------------
    # Calculate code health score
    # --------------------------------------------------------

    score = 100


    for finding in all_findings:

        severity = str(
            finding.get(
                "severity",
                "INFO"
            )
        ).upper()


        if severity == "CRITICAL":

            score -= 20


        elif severity == "HIGH":

            score -= 12


        elif severity == "MEDIUM":

            score -= 7


        elif severity == "LOW":

            score -= 3


    # --------------------------------------------------------
    # Keep score between 0 and 100
    # --------------------------------------------------------

    score = max(
        0,
        min(
            100,
            score
        )
    )


    # --------------------------------------------------------
    # Determine overall risk level
    # --------------------------------------------------------

    if score >= 85:

        risk_level = "LOW"


    elif score >= 65:

        risk_level = "MEDIUM"


    elif score >= 40:

        risk_level = "HIGH"


    else:

        risk_level = "CRITICAL"


    # --------------------------------------------------------
    # Create final combined report
    # --------------------------------------------------------

    final_report = {

        "code_health_score": score,

        "risk_level": risk_level,

        "total_findings": total_findings,

        "bugs": bugs,

        "security_vulnerabilities": vulnerabilities,

        "performance_issues": performance_issues,

        "quality_issues": quality_issues,

        "agent_summaries": {

            "bug_agent": bug_result.get(
                "summary",
                ""
            ),

            "security_agent": security_result.get(
                "summary",
                ""
            ),

            "performance_agent": performance_result.get(
                "summary",
                ""
            ),

            "quality_agent": quality_result.get(
                "summary",
                ""
            )
        }
    }


    # --------------------------------------------------------
    # Return final report to LangGraph
    # --------------------------------------------------------

    return {
        "final_report": final_report
    }


# ============================================================
# 7. Create LangGraph workflow
# ============================================================

graph_builder = StateGraph(
    MultiAgentState
)


# ============================================================
# 8. Add specialized agents as nodes
# ============================================================

graph_builder.add_node(
    "bug_agent",
    run_bug_agent
)

graph_builder.add_node(
    "security_agent",
    run_security_agent
)

graph_builder.add_node(
    "performance_agent",
    run_performance_agent
)

graph_builder.add_node(
    "quality_agent",
    run_quality_agent
)

graph_builder.add_node(
    "final_report",
    create_final_report
)


# ============================================================
# 9. Start four specialized agents
# ============================================================

graph_builder.add_edge(
    START,
    "bug_agent"
)

graph_builder.add_edge(
    START,
    "security_agent"
)

graph_builder.add_edge(
    START,
    "performance_agent"
)

graph_builder.add_edge(
    START,
    "quality_agent"
)


# ============================================================
# 10. Send all agent results to final report
# ============================================================

graph_builder.add_edge(
    "bug_agent",
    "final_report"
)

graph_builder.add_edge(
    "security_agent",
    "final_report"
)

graph_builder.add_edge(
    "performance_agent",
    "final_report"
)

graph_builder.add_edge(
    "quality_agent",
    "final_report"
)


# ============================================================
# 11. End workflow
# ============================================================

graph_builder.add_edge(
    "final_report",
    END
)


# ============================================================
# 12. Compile the multi-agent system
# ============================================================

multi_agent_code_reviewer = (
    graph_builder.compile()
)