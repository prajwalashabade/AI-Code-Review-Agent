from app.agents.security_agent import security_detection_agent


# ============================================
# Test code containing security vulnerabilities
# ============================================

code = """
import java.sql.Connection;
import java.sql.Statement;

public class LoginService {

    private String username = "admin";
    private String password = "admin123";

    public void login(String userInput) {

        String query =
            "SELECT * FROM users WHERE username = '"
            + userInput
            + "'";

        System.out.println("Executing query: " + query);

        Runtime.getRuntime().exec(userInput);

        System.out.println(
            "User password: " + password
        );
    }
}
"""


# ============================================
# Run Security Detection Agent
# ============================================

result = security_detection_agent(
    code=code,
    language="Java"
)


# ============================================
# Display result
# ============================================

print("\n========================================")
print("     SECURITY DETECTION AGENT RESULT")
print("========================================\n")

print("Agent:")
print(result.get("agent"))

print("\nSummary:")
print(result.get("summary"))

print("\nSecurity Vulnerabilities:")

for index, vulnerability in enumerate(
    result.get("vulnerabilities", []),
    start=1
):

    print(
        f"\n{index}. "
        f"{vulnerability.get('title')}"
    )

    print(
        f"   Severity: "
        f"{vulnerability.get('severity')}"
    )

    print(
        f"   Line: "
        f"{vulnerability.get('line')}"
    )

    print(
        f"   Description: "
        f"{vulnerability.get('description')}"
    )

    print(
        f"   Recommendation: "
        f"{vulnerability.get('recommendation')}"
    )