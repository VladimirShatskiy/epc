
def read(str_to_convert: str) -> str:
    """
    Получает строку госномера и возвращает его без пробелов, символов и с латинскими буквами
    :param str_to_convert: срока для конвертации
    """
    get_vals = list([val for val in str_to_convert
                    if val.isalpha() or val.isnumeric()])
    result = "".join(get_vals).upper()
    return convert_latin(result)


def convert_latin(str_to_convert: str) -> str:
    """
    Конвертирует строку из кирилици в латиницу
    """
    rus_latin_dict = {
        "А": "А",
        "В": "В",
        "Е": "Е",
        "К": "К",
        "М": "М",
        "Н": "Н",
        "О": "О",
        "Р": "Р",
        "С": "С",
        "Т": "Т",
        "Х": "Х",
    }
    convert_str = ''
    for item in str_to_convert:
        if item in rus_latin_dict.keys():
            convert_str += rus_latin_dict[item]
        else:
            convert_str += item
    return convert_str

read("1234 ав - 7")
