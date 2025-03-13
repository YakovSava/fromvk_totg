import re


def check_to_stop(text: str, stop: list[str]) -> bool:
    for stop_word in stop:
        if stop_word in text:
            return True
    return False


def replace_word(text: str, word_list: list[list[str]]) -> str:
    for repl1 in word_list:
        try:
            original = repl1[0]
            replacement = repl1[1]

            # Если это хэштег (начинается с #), используем другой шаблон
            if original.startswith('#'):
                pattern = re.compile(r'(?:{})\b'.format(re.escape(original)), re.IGNORECASE)
            else:
                pattern = re.compile(r'\b(?:{})\b'.format(re.escape(original)), re.IGNORECASE)

            text = pattern.sub(replacement, text)
        except Exception as e:
            print(f"Error in replace_word: {e}")

    return text
