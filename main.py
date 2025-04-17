from fastapi import FastAPI
from pydantic import BaseModel
import swisseph as swe
from datetime import datetime

app = FastAPI()
swe.set_ephe_path('.')  # Ephemeris path

ZODIAC = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

class AyBurcuIstek(BaseModel):
    tarih: str
    saat: str
    utc: str
    lat: float
    lon: float

def get_zodiac(degree):
    index = int(degree / 30) % 12
    return ZODIAC[index]

@app.post("/ayburcu")
def hesapla(data: AyBurcuIstek):
    try:
        dt = datetime.strptime(f"{data.tarih} {data.saat}", "%Y-%m-%d %H:%M")

        # ✅ UTC farkını saat cinsine çevir
        utc_saat = int(data.utc.replace(":", "").replace("+", ""))
        hour_decimal = dt.hour + dt.minute / 60.0 - utc_saat

        julday = swe.julday(dt.year, dt.month, dt.day, hour_decimal)

        # 🌕 Ay konumu
        moon = swe.calc_ut(julday, swe.MOON)[0]
        moon_lon = moon[0]
        burc = get_zodiac(moon_lon)
        derece = round(moon_lon % 30, 2)

        # 🏠 Ev hesabı
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
        return {"hata": str(e)}
