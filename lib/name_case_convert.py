def snake_to_pascal(snake_case_str):
    """
    スネークケースからパスカルケースに変換する
    :param snake_case_str:
    :return:
    """
    words = snake_case_str.split('_')
    pascal_case_words = [word.capitalize() for word in words]
    return ''.join(pascal_case_words)
