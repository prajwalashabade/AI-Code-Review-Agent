import re


def deduplicate_findings(findings):
    """
    Remove duplicate or highly similar findings reported
    by different AI analysis agents.
    """

    unique_findings = []
    seen = set()

    for finding in findings:

        title = str(
            finding.get("title", "")
        ).strip()

        category = str(
            finding.get("category", "")
        ).strip().upper()

        line = finding.get(
            "line",
            ""
        )

        # Convert title to lowercase for comparison
        normalized_title = title.lower()

        # --------------------------------------------------
        # Normalize common variations of the same issue
        # --------------------------------------------------

        if (
            "zero division" in normalized_title
            or "zerodivisionerror" in normalized_title
        ):
            issue_type = "zero_division"

        elif (
            "array index" in normalized_title
            or "arrayindexoutofbounds" in normalized_title
        ):
            issue_type = "array_index"

        elif (
            "null pointer" in normalized_title
            or "nullpointerexception" in normalized_title
        ):
            issue_type = "null_pointer"

        elif "sql injection" in normalized_title:
            issue_type = "sql_injection"

        elif (
            "hardcoded credential" in normalized_title
            or "hardcoded password" in normalized_title
            or "hardcoded password" in normalized_title
        ):
            issue_type = "hardcoded_credentials"

        elif "command injection" in normalized_title:
            issue_type = "command_injection"

        elif "string concatenation" in normalized_title:
            issue_type = "string_concatenation"

        else:
            # Generic normalization for other issues
            issue_type = re.sub(
                r"[^a-z0-9]+",
                "_",
                normalized_title
            ).strip("_")

        # --------------------------------------------------
        # Create a unique fingerprint
        # --------------------------------------------------

        fingerprint = (
            category,
            issue_type,
            str(line)
        )

        # --------------------------------------------------
        # Keep only the first occurrence
        # --------------------------------------------------

        if fingerprint in seen:
            continue

        seen.add(fingerprint)

        unique_findings.append(finding)

    return unique_findings