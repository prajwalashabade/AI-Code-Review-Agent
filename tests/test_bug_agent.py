from app.agents.bug_agent import bug_detection_agent


# ============================================
# Test Java code containing deliberate bugs
# ============================================

code = """
public class Test {

    public static void main(String[] args) {

        int[] numbers = {10, 20, 30};

        for (int i = 0; i <= numbers.length; i++) {
            System.out.println(numbers[i]);
        }

        int result = 10 / 0;

        String name = null;

        System.out.println(name.length());
    }
}
"""


# ============================================
# Run Bug Detection Agent
# ============================================

result = bug_detection_agent(
    code=code,
    language="Java"
)


# ============================================
# Display result
# ============================================

print("\n========================================")
print("       BUG DETECTION AGENT RESULT")
print("========================================\n")

print("Agent:")
print(result.get("agent"))

print("\nSummary:")
print(result.get("summary"))

print("\nBugs:")

for index, bug in enumerate(
    result.get("bugs", []),
    start=1
):

    print(f"\n{index}. {bug.get('title')}")

    print(
        f"   Severity: "
        f"{bug.get('severity')}"
    )

    print(
        f"   Line: "
        f"{bug.get('line')}"
    )

    print(
        f"   Description: "
        f"{bug.get('description')}"
    )

    print(
        f"   Recommendation: "
        f"{bug.get('recommendation')}"
    )