from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.const import MOON

app = FastAPI()

# CORS ayarı (Flutter için açık)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dereceyi burç + dereceye çevir
def ecliptic_degree_to_zodiac(degree):
    index = int(degree // 30)
    zodiac_signs = [
        'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    burc = zodiac_signs[index % 12]
    derece = round(degree % 30, 2)
    return burc, derece

# Float enlem/boylamı DMS formatına çevir
def float_to_dms(value):
    derece = int(value)
    dakika_float = abs(value - derece) * 60
    dakika = int(dakika_float)
    saniye = int((dakika_float - dakika) * 60)
    return f"{derece}:{dakika}:{saniye}"

# Ay Burcu Hesaplama Endpoint'i
@app.get("/ayburcu")
def ay_burcu_hesapla(
    yil: int,
    ay: int,
    gun: int,
    saat: int,
    dakika: int,
    enlem: float,
    boylam: float
):
    try:
        dt = Datetime(f'{yil}/{ay:02d}/{gun:02d}', f'{saat:02d}:{dakika:02d}', '+00:00')
        pos = GeoPos(float_to_dms(enlem), float_to_dms(boylam))
        chart = Chart(dt, pos)
        moon = chart.get(MOON)
        burc, derece = ecliptic_degree_to_zodiac(moon.lon)

        return {
            "burc": burc,
            "derece": derece
        }
    except Exception as e:
        return {"error": str(e)}
