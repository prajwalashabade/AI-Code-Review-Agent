from app.agents.performance_agent import performance_detection_agent


# ============================================
# Test Java code containing performance issues
# ============================================

code = """
import java.util.ArrayList;
import java.util.List;

public class PerformanceTest {

    public static void main(String[] args) {

        List<Integer> numbers = new ArrayList<>();

        for (int i = 0; i < 10000; i++) {
            numbers.add(i);
        }

        for (int i = 0; i < numbers.size(); i++) {

            for (int j = 0; j < numbers.size(); j++) {

                if (numbers.get(i).equals(numbers.get(j))) {
                    System.out.println("Match found");
                }
            }
        }

        String result = "";

        for (int i = 0; i < 10000; i++) {
            result = result + i;
        }

        for (int i = 0; i < 1000; i++) {
            System.out.println("Processing...");
        }
    }
}
"""


# ============================================
# Run Performance Detection Agent
# ============================================

result = performance_detection_agent(
    code=code,
    language="Java"
)


# ============================================
# Display result
# ============================================

print("\n========================================")
print("   PERFORMANCE DETECTION AGENT RESULT")
print("========================================\n")

print("Agent:")
print(result.get("agent"))

print("\nSummary:")
print(result.get("summary"))

print("\nPerformance Issues:")

for index, issue in enumerate(
    result.get("performance_issues", []),
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