def keyword_match_score(
    text: str,
    keywords: list[str],
) -> float:
    text_lower = text.lower()

    matches = sum(
        1
        for keyword in keywords
        if keyword.lower()
        in text_lower
    )

    return matches / len(keywords)