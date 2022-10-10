text = "some some some some some thing thing thing thing thing some thing"
pattern = "thi"

current_index = 0
found_word_index = 0
new_str = ""

while True:
    try:
        # Находим начало слова, необходимое для поиска, начиная с current_index
        find_index = text[current_index:].lower().index(pattern.lower())
    except:
        # Выход из цикла если слова больше нет
        break
    # Находим индекс начала найденного слова
    found_word_index = current_index + find_index
    # Изменяем цвет найденного слова на красный
    new_str += text[current_index:found_word_index] + "<span style='color: red;'>" + text[found_word_index:found_word_index + len(pattern)] + "</span>"

    # Нужен для поиска не с 0 элемента
    current_index = found_word_index + len(pattern)

# Добавляем последние символы в строку
new_str += text[found_word_index + len(pattern):]

print(new_str)  