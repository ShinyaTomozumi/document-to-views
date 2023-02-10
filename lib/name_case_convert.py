def snake_to_pascal(string: str) -> str:
    """
    スネークケースからパスカルケースに変換する
    :param string:
    :return:
    """
    # スネークケースでない場合は、そのまま返却する
    if not is_snake_case(string):
        return string

    words = string.split('_')
    pascal_case_words = [word.capitalize() for word in words]
    return ''.join(pascal_case_words)


def is_snake_case(string: str) -> bool:
    """
    パスカル形式かどうかを判定する
    :param string:
    :return:
    """
    if string.isalnum() or string.isalpha():
        return False
    if string[0].isdigit():
        return False
    if " " in string:
        return False
    return True


def is_pascal_case(string: str) -> bool:
    """
    指定した文字列がパスカルケースかどうかを判定する
    :param string:
    :return:
    """
    if not string.isalnum():
        return False
    if not string[0].isalpha() or not string[0].isupper():
        return False
    for char in string[1:]:
        if not char.isalpha() or not char.islower():
            return False
    return True
