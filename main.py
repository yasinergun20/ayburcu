from fastapi import FastAPI
from pydantic import BaseModel
import swisseph as swe
from datetime import datetime
import math

app = FastAPI()
swe.set_ephe_path('.')  # ephemeris dosyaları için yol

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
        # Tarih ve saat formatı
        dt = datetime.strptime(f"{data.tarih} {data.saat}", "%Y-%m-%d %H:%M")
        julday = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0)

        # Ay pozisyonu
        moon_pos = swe.calc_ut(julday, swe.MOON)[0]
        burc = get_zodiac(moon_pos)
        derece = round(moon_pos % 30, 2)

        # Ev hesaplama
        ascmc, cusps = swe.houses(julday, data.lat, data.lon, b'P')  # Placidus sistemi
        for i in range(1, 13):
            if cusps[i - 1] <= moon_pos < cusps[i % 12]:
                ev = i
                break
        else:
            ev = 12  # fallback

        return {
            "burc": burc,
            "derece": derece,
            "ev": ev
        }

    except Exception as e:
        return {"hata": str(e)}
