from fastapi import FastAPI
from pydantic import BaseModel
import swisseph as swe
from datetime import datetime

app = FastAPI()

# Gerekirse ephemeris yolu
swe.set_ephe_path('.')

ZODIAC = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

class AyBurcuIstek(BaseModel):
    tarih: str      # "1995-04-15"
    saat: str       # "10:45"
    utc: str        # "+02:00"
    lat: float      # 39.92
    lon: float      # 32.85

def get_zodiac(degree):
    index = int(degree / 30) % 12
    return ZODIAC[index]

@app.post("/ayburcu")
def hesapla(data: AyBurcuIstek):
    try:
        # Tarihi UTC ile birlikte parse et
        dt = datetime.strptime(f"{data.tarih} {data.saat}", "%Y-%m-%d %H:%M")
        utc_offset = int(data.utc.replace("+", "").replace(":", ""))
        hour_decimal = dt.hour + dt.minute / 60.0
        julday = swe.julday(dt.year, dt.month, dt.day, hour_decimal)

        # 🌕 Ay derecesi (boylam)
        moon = swe.calc_ut(julday, swe.MOON)[0]  # [longitude, latitude, distance]
        moon_lon = moon[0]

        burc = get_zodiac(moon_lon)
        derece = round(moon_lon % 30, 2)

        # 🏠 Ev hesabı (Placidus)
        cusps, _ = swe.houses(julday, data.lat, data.lon, b'P')

        ev = 12
        for i in range(12):
            c1 = cusps[i]
            c2 = cusps[(i + 1) % 12]
            if c1 < c2:
                if c1 <= moon_lon < c2:
                    ev = i + 1
                    break
            else:
                if moon_lon >= c1 or moon_lon < c2:
                    ev = i + 1
                    break

        return {
            "burc": burc,
            "derece": derece,
            "ev": ev
        }

    except Exception as e:
