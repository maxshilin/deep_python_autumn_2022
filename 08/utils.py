def delete_uninteresting_words(counter):
    ignore = [
        "",
        "the",
        "a",
        "if",
        "in",
        "it",
        "of",
        "or",
        "and",
        "is",
        "to",
        "by",
        "on",
        "that",
        "from",
        "s",
        "t",
        "mathbf",
        "for",
        "are",
        "was",
        "as",
        "with",
        "this",
        "be",
        "at",
        "can",
        "an",
    ]
    for word in ignore:
        if word in counter:
            del counter[word]

    return counter
