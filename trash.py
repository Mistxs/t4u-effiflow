import re

string = "143095 ГОЛИЦЫНО 53 ПАРКОВАЯ 7"

pattern = r'(\d+)\s+(.+?)\s+(\d)\s+(.+)'

try:

    substr = string.split(" ")
    print(substr)

    match = re.match(pattern, string)

    if match:
        def replace(match):
            if match.group(1)[-1] == match.group(3):
                return f"{match.group(1)} {match.group(2)} {match.group(4)}"
            else:
                return match.group(0)
        new_string = re.sub(pattern, replace, string)
        print(new_string)
    else:
        raise Exception("Строка не соответствует регулярному выражению")

except Exception as e:
    print(f"Ошибка - {e}")

