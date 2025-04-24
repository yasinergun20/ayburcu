from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.const import MOON

# Dereceyi burç ve dereceye çeviren fonksiyon
def ecliptic_degree_to_zodiac(degree):
    index = int(degree // 30)
    zodiac_signs = [
        'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    burc = zodiac_signs[index % 12]
    derece = round(degree % 30, 2)
    return burc, derece

# Float enlem/boylamı DMS (derece:dakika:saniye) formatına çevir
def float_to_dms(value):
    derece = int(value)
    dakika_float = abs(value - derece) * 60
    dakika = int(dakika_float)
    saniye = int((dakika_float - dakika) * 60)
    return f"{derece}:{dakika}:{saniye}"

# Ay burcu, derecesi ve ev bilgisi döner
def get_ay_burcu_derece_ev(yil, ay, gun, saat, dakika, enlem, boylam):
    dt = Datetime(f'{yil}/{ay:02d}/{gun:02d}', f'{saat:02d}:{dakika:02d}', '+00:00')
    enlem_dms = float_to_dms(enlem)
    boylam_dms = float_to_dms(boylam)
    pos = GeoPos(enlem_dms, boylam_dms)
    chart = Chart(dt, pos, hsys='PLACIDUS')

    moon = chart.get(MOON)
    burc, derece = ecliptic_degree_to_zodiac(moon.lon)
    ev = moon.house
    return burc, derece, ev

# ÖRNEK: 15 Ocak 2025, saat 12:00 UTC, Ankara koordinatları
burc, derece, ev = get_ay_burcu_derece_ev(2025, 1, 15, 12, 0, 39.9208, 32.8541)
print(f"Ay Burcu: {burc}")
print(f"Ay Derecesi: {derece}°")
print(f"Ay Evi: {ev}")
