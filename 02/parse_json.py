import json


def keyword_callback(keyword):
    print(keyword)


def get_tokens(field):
    if field:
        tokens = field.split(" ")
        return tokens
    return None


def add_to_dict(token, num, found_keywords):
    if token not in found_keywords:
        found_keywords[token] = num
    else:
        found_keywords[token] += num


def parse_json(
    json_str: str, keyword_callback, required_fields=None, keywords=None
):
    if not required_fields or not keywords or not json_str:
        return None
    set_keywords = set(keywords)
    found_keywords = {}
    parsed_json = json.loads(json_str)

    for field in required_fields:
        if field not in parsed_json:
            continue

        tokens = get_tokens(parsed_json[field])
        if not tokens:
            continue

        matched_tokens = set(tokens) & set_keywords
        for token in matched_tokens:
            num = tokens.count(token)
            for _ in range(num):
                keyword_callback(token)
            add_to_dict(token, num, found_keywords)
    return found_keywords
