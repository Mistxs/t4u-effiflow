def crc16_ccitt(data):
    crc = 0xFFFF
    for byte in data:
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
            crc &= 0xFFFF
    return crc

def calculate_rnm_kkt(serial_number, inn, factory_number):
    data = serial_number.zfill(10) + inn.zfill(12) + factory_number.zfill(20)
    crc_result = crc16_ccitt(data.encode('cp866'))
    crc_decimal = str(crc_result).zfill(6)
    return crc_decimal

# Пример использования:
serial_number = '0000000001'
inn = '7708274185'
factory_number = '00000000177044008917'
rnm_kkt = calculate_rnm_kkt(serial_number, inn, factory_number)
print(f"РНМ ККТ равен {rnm_kkt}")
