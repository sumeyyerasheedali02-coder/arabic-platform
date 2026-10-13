"""Server-owned grading rules. Missing marks never silently count as zero."""
ACTIVITIES = ("writing", "class_activity", "home_activity", "language_lab")


def weekly_total(entry):
    if entry is None or any(entry[key] is None for key in ACTIVITIES):
        return None
    return sum(entry[key] for key in ACTIVITIES)


def term_result(term, weeks, entries, exam, *, published_only=False):
    if term is None or (published_only and not term["published"]):
        return None
    by_number = {w["number"]: w for w in weeks}
    totals = []
    for number in range(term["first_week"], term["last_week"] + 1):
        week = by_number.get(number)
        if week is None or (published_only and not week["published"]):
            return None
        total = weekly_total(entries.get(week["id"]))
        if total is None:
            return None
        totals.append(total)
    activity = sum(totals) / len(totals)
    return {"activity": round(activity, 2), "exam": exam,
            "total": None if exam is None else round(activity + exam, 2)}


def overall_result(results):
    if len(results) != 2 or any(r is None or r["total"] is None for r in results):
        return None
    score = round(sum(r["total"] for r in results) / 2, 2)
    return {"score": score, "passed": score >= 50, "needed": round(max(0, 50 - score), 2)}
