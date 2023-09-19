from datetime import datetime
import pytz

# Получение текущей временной метки
ts = datetime.now()

# Определение временной зоны UTC+3 (Московское время)
timezone = pytz.timezone('Etc/GMT-3')

# Преобразование временной метки во временную зону UTC+3
ts_utc_plus_3 = ts.astimezone(timezone)

print("Local time:", ts)
print("UTC+3 time:", ts_utc_plus_3)