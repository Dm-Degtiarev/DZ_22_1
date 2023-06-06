import re


def len_text_matching(text, stop_list):
    lower_text = text.lower()
    split_object = set(re.split(r'[^a-zA-Z0-9А-Яа-я]', lower_text))
    len_data = len(split_object.intersection(stop_list))

    return len_data
