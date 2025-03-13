import re


def check_to_stop(text: str, stop: list[str]) -> bool:
    for stop_word in stop:
        if stop_word in text:
            return True
    return False


def replace_word(text: str, word_list: list[list[str]]) -> str:
    for repl1 in word_list:
        try:
            word_dict = {repl1[0]: repl1[1]}

            pattern = re.compile(r'\b(?:{})\b'.format('|'.join(word_dict.keys())), re.IGNORECASE)
            text = pattern.sub(lambda match: word_dict[match.group(0)], text)
        except:
            pass

    return text
