import re

phone_number = input("Введите номер телефона: ")

cleaned_number = re.sub(r"\D", "", phone_number)

if cleaned_number.startswith("8"):
    cleaned_number = "+7" + cleaned_number[1:]

# Вывод правильного формата номера
print("Правильный номер телефона в формате '+7XXXXXXXXXX':", cleaned_number)