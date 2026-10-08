from app.agents.agent import code_review_agent


# Sample Java code with a deliberate bug
code = """
public class Test {

    public static void main(String[] args) {

        int[] numbers = {10, 20, 30};

        for (int i = 0; i <= numbers.length; i++) {
            System.out.println(numbers[i]);
        }
    }
}
"""


# Send the code to the AI Code Review Agent
result = code_review_agent.invoke({
    "code": code,
    "language": "Java",
    "review": ""
})


# Display the result
print("\n========================================")
print("        AI CODE REVIEW RESULT")
print("========================================\n")

print(result["review"])