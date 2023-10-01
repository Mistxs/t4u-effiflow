import urllib.parse

original_string = "Солнцезащитный крем Oil Free SPF50+PA++++/UV  Oil Free SPF50+PA++++"
url_encoded_string = urllib.parse.quote_plus(original_string, encoding='utf-8')
print('%D0%A1%D0%BE%D0%BB%D0%BD%D1%86%D0%B5%D0%B7%D0%B0%D1%89%D0%B8%D1%82%D0%BD%D1%8B%D0%B9+%D0%BA%D1%80%D0%B5%D0%BC+Oil+Free+SPF50%2BPA%2B%2B%2B%2B%2FUV++Oil+Free+SPF50%2BPA%2B%2B%2B%2B')
print(url_encoded_string)

