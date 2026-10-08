from app.agents.autofix_agent import generate_code_fix


# ============================================================
# 1. Sample Java code containing multiple problems
# ============================================================

code = """
public class Test {

    public static void main(String[] args) {

        int[] numbers = {10, 20, 30};

        for (int i = 0; i <= numbers.length; i++) {
            System.out.println(numbers[i]);
        }

        String password = "admin123";

        String query = "SELECT * FROM users WHERE password = '" 
                     + password + "'";

        System.out.println(query);
    }
}
"""


# ============================================================
# 2. Findings from our AI code-review agents
# ============================================================

findings = [

    {
        "title": "ArrayIndexOutOfBoundsException",
        "category": "Bug",
        "severity": "CRITICAL",
        "description": (
            "The loop uses <= numbers.length, "
            "which can access an invalid array index."
        ),
        "recommendation": (
            "Change i <= numbers.length to "
            "i < numbers.length."
        )
    },

    {
        "title": "Hardcoded Credentials",
        "category": "Security",
        "severity": "HIGH",
        "description": (
            "A password is hardcoded directly "
            "inside the source code."
        ),
        "recommendation": (
            "Remove hardcoded credentials and "
            "use secure configuration."
        )
    },

    {
        "title": "SQL Injection",
        "category": "Security",
        "severity": "CRITICAL",
        "description": (
            "The SQL query is constructed using "
            "string concatenation."
        ),
        "recommendation": (
            "Use PreparedStatement or another "
            "parameterized database approach."
        )
    }
]


# ============================================================
# 3. Run the AI Auto-Fix Agent
# ============================================================

result = generate_code_fix(
    code=code,
    language="Java",
    findings=findings
)


# ============================================================
# 4. Display the result
# ============================================================

print("\n")
print("=" * 70)
print("                 AI AUTO-FIX RESULT")
print("=" * 70)

print("\nEXPLANATION:")
print(result["explanation"])

print("\n")
print("CHANGES:")
print(result["changes"])

print("\n")
print("FIXED CODE:")
print("=" * 70)
print(result["fixed_code"])
print("=" * 70)