"""Generate a human-readable ATS report from simulation results."""


def format_ats_report(result: dict) -> str:
    lines = []
    score = result.get("score", 0)
    lines.append(f"Predicted ATS score: {score}/100")
    found = result.get("found", [])
    if found:
        lines.append("Matched keywords:")
        for k in found:
            lines.append(f" - {k}")
    else:
        lines.append("No required keywords matched.")
    lines.append(
        "Recommendations: Add exact required skills in Skills section; avoid images/headers."
    )
    return "\n".join(lines)
