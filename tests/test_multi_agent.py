from app.agents.multi_agent import (
    multi_agent_code_reviewer
)


# ============================================================
# Test code containing multiple types of problems
# ============================================================

code = """
public class UserService {

    public static void main(String[] args) {

        String username = "admin";
        String password = "admin123";

        int[] numbers = {10, 20, 30};

        for (int i = 0; i <= numbers.length; i++) {
            System.out.println(numbers[i]);
        }

        int result = 10 / 0;

        String name = null;

        System.out.println(name.length());

        String query =
            "SELECT * FROM users WHERE name = '"
            + username
            + "'";

        System.out.println(query);

        String resultText = "";

        for (int i = 0; i < 10000; i++) {
            resultText = resultText + i;
        }

        int x = 10;
        int y = 20;

        System.out.println(x + y);
    }
}
"""


# ============================================================
# Run Multi-Agent Code Reviewer
# ============================================================

result = multi_agent_code_reviewer.invoke({

    "code": code,

    "language": "Java"
})


# ============================================================
# Get final report
# ============================================================

report = result["final_report"]


# ============================================================
# Display final result
# ============================================================

print("\n")
print("==============================================")
print("       MULTI-AGENT CODE REVIEW RESULT")
print("==============================================")

print(
    f"\nCODE HEALTH SCORE: "
    f"{report['code_health_score']}/100"
)

print(
    f"RISK LEVEL: "
    f"{report['risk_level']}"
)

print(
    f"TOTAL FINDINGS: "
    f"{report['total_findings']}"
)


# ============================================================
# Bug findings
# ============================================================

print("\n")
print("--------------- BUG AGENT ----------------")

for bug in report["bugs"]:

    print(
        f"\n{bug.get('title')}"
    )

    print(
        f"Severity: "
        f"{bug.get('severity')}"
    )

    print(
        f"Line: "
        f"{bug.get('line')}"
    )


# ============================================================
# Security findings
# ============================================================

print("\n")
print("------------ SECURITY AGENT ---------------")

for vulnerability in report[
    "security_vulnerabilities"
]:

    print(
        f"\n{vulnerability.get('title')}"
    )

    print(
        f"Severity: "
        f"{vulnerability.get('severity')}"
    )

    print(
        f"Line: "
        f"{vulnerability.get('line')}"
    )


# ============================================================
# Performance findings
# ============================================================

print("\n")
print("---------- PERFORMANCE AGENT --------------")

for issue in report[
    "performance_issues"
]:

    print(
        f"\n{issue.get('title')}"
    )

    print(
        f"Severity: "
        f"{issue.get('severity')}"
    )

    print(
        f"Line: "
        f"{issue.get('line')}"
    )


# ============================================================
# Quality findings
# ============================================================

print("\n")
print("------------- QUALITY AGENT ---------------")

for issue in report[
    "quality_issues"
]:

    print(
        f"\n{issue.get('title')}"
    )

    print(
        f"Severity: "
        f"{issue.get('severity')}"
    )

    print(
        f"Line: "
        f"{issue.get('line')}"
    )


# ============================================================
# Agent summaries
# ============================================================

print("\n")
print("------------- AGENT SUMMARIES -------------")

for agent, summary in report[
    "agent_summaries"
].items():

    print(
        f"\n{agent.upper()}:"
    )

    print(summary)


print("\n")
print("==============================================")
print("        MULTI-AGENT REVIEW COMPLETE")
print("==============================================")