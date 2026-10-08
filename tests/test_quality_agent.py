from app.agents.quality_agent import quality_detection_agent


# ============================================
# Test Java code containing quality problems
# ============================================

code = """
public class Test {

    public static void main(String[] args) {

        int x = 10;
        int y = 20;

        int z = x + y;

        System.out.println("Result: " + z);

        int a = 100;
        int b = 200;
        int c = 300;

        System.out.println(a);
        System.out.println(b);
        System.out.println(c);

        String userName = "admin";
        String userName2 = "admin";

        if (userName.equals(userName2)) {
            System.out.println("Same user");
        }

        for (int i = 0; i < 10; i++) {
            System.out.println("Processing");
        }

        for (int i = 0; i < 10; i++) {
            System.out.println("Processing");
        }
    }
}
"""


# ============================================
# Run Code Quality Detection Agent
# ============================================

result = quality_detection_agent(
    code=code,
    language="Java"
)


# ============================================
# Display result
# ============================================

print("\n========================================")
print("    CODE QUALITY DETECTION AGENT RESULT")
print("========================================\n")

print("Agent:")
print(result.get("agent"))

print("\nSummary:")
print(result.get("summary"))

print("\nQuality Issues:")

for index, issue in enumerate(
    result.get("quality_issues", []),
    start=1
):

    print(
        f"\n{index}. "
        f"{issue.get('title')}"
    )

    print(
        f"   Severity: "
        f"{issue.get('severity')}"
    )

    print(
        f"   Line: "
        f"{issue.get('line')}"
    )

    print(
        f"   Description: "
        f"{issue.get('description')}"
    )

    print(
        f"   Recommendation: "
        f"{issue.get('recommendation')}"
    )
    