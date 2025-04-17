from fastapi import FastAPI
from pydantic import BaseModel
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
import swisseph as swe

app = FastAPI()
swe.set_ephe_path('.')  # Gerekirse yol ver

ZODIAC = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

class AyBurcuIstek(BaseModel):
    tarih: str  # "2000-01-01"
    saat: str   # "12:00"
    lat: float  # 39.92
    lon: float  # 32.85

def get_zodiac(degree):
    index = int(degree / 30) % 12
    return ZODIAC[index]

@app.post("/ayburcu")
def hesapla(data: AyBurcuIstek):
    try:
        # 🕒 Yerel saat → UTC
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lat=data.lat, lng=data.lon)
        tz = pytz.timezone(tz_name)
        
        local_dt = datetime.strptime(f"{data.tarih} {data.saat}", "%Y-%m-%d %H:%M")
        localized = tz.localize(local_dt)
        utc_dt = localized.astimezone(pytz.utc)

        # 🌍 UTC zamanı → Julian Day
        utc_hour = utc_dt.hour + utc_dt.minute / 60.0
        jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_hour)

        # 🌕 Ay'ın konumu
        moon = swe.calc_ut(jd, swe.MOON)[0]
        moon_lon = moon[0]
        burc = get_zodiac(moon_lon)
        derece = round(moon_lon % 30, 2)

        # 🏠 Ev konumu
        cusps, _ = swe.houses(jd, data.lat, data.lon, b'P')
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
