import json


def keyword_callback(keyword):
    print(keyword)


def get_tokens(field):
    if field:
        tokens = field.split(" ")
        return tokens
    return None


def parse_json(
    json_str: str, keyword_callback, required_fields=None, keywords=None
):
    if not required_fields or not keywords or not json_str:
        return None
    found_keywords = {}
    parsed_json = json.loads(json_str)

    for field in required_fields:
        tokens = get_tokens(parsed_json[field])
        if tokens:
            for token in tokens:
                if token in keywords:
                    keyword_callback(token)
                    if token not in found_keywords:
                        found_keywords[token] = 1
                    else:
                        found_keywords[token] += 1
    return found_keywords
