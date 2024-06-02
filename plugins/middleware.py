import re

def check_to_stop(text:str, stop:list[str]) -> bool:
    for stop_word in stop:
        if stop_word in text:
            return True
    return False

def replace_word(text:str, word_repl:list[list[str], list[str]]) -> str:
    for word, repl_to in word_repl:
    	pattern = r'\b\W*('+word+r'+)\W*\b'
    	text = re.sub(pattern, repl_to, text)
    return text