import re

def replace_words_with_spaces(text):
    # Регулярное выражение для поиска слов, окруженных пробелами или специальными символами
    pattern = r'\b\W*(Зде+)\W*\b'
    
    # Замена найденных слов на "[заменено]"
    replaced_text = re.sub(pattern, '[удалено]', text)
    
    return replaced_text

# Пример использования функции
original_text = "Привет! Это тестовый текст. Здесь есть слова, которые будут заменены."
replaced_text = replace_words_with_spaces(original_text)

print("Оригинальный текст:")
print(original_text)
print("\nТекст после замены:")
print(replaced_text)