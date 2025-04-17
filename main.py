from fastapi import FastAPI
from pydantic import BaseModel
import swisseph as swe
from datetime import datetime

app = FastAPI()
swe.set_ephe_path('.')  # Gerekirse ephemeris dosyaları

ZODIAC = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

class AyBurcuIstek(BaseModel):
    tarih: str     # "1995-04-15"
    saat: str      # "10:45"
    utc: str       # "+03:00"
    lat: float
    lon: float

def get_zodiac(degree):
    index = int(degree / 30) % 12
    return ZODIAC[index]

@app.post("/ayburcu")
def hesapla(data: AyBurcuIstek):
    try:
        dt = datetime.strptime(f"{data.tarih} {data.saat}", "%Y-%m-%d %H:%M")
        julday = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0)

        # 🌕 Ay pozisyonu (longitude)
        moon_long = swe.calc_ut(julday, swe.MOON)[0][0]
        burc = get_zodiac(moon_long)
        derece = round(moon_long % 30, 2)

        # 🏠 Ev hesaplama (Placidus)
        cusps, ascmc = swe.houses(julday, data.lat, data.lon, b'P')
        ev = 12
        for i in range(12):
            if cusps[i] <= moon_long < cusps[(i + 1) % 12]:
                ev = i + 1
                break

        return {
            "burc": burc,
            "derece": derece,
            "ev": ev
        }

    except Exception as e:
        return {"hata": str(e)}
