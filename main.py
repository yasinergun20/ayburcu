from fastapi import FastAPI
from pydantic import BaseModel
import swisseph as swe
from datetime import datetime
from timezonefinder import TimezoneFinder
import pytz

app = FastAPI()

# Swiss Ephemeris path
swe.set_ephe_path('.')

ZODIAC = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

class AyBurcuIstek(BaseModel):
    tarih: str      # "1995-04-15"
    saat: str       # "10:45"
    lat: float      # 39.92
    lon: float      # 32.85


def get_zodiac(degree):
    index = int(degree / 30) % 12
    return ZODIAC[index]

@app.post("/ayburcu")
def hesapla(data: AyBurcuIstek):
    try:
        # 1. Tarih-saat birleşimi
        dt = datetime.strptime(f"{data.tarih} {data.saat}", "%Y-%m-%d %H:%M")

        # 2. Timezone belirle
        tf = TimezoneFinder()
        timezone_name = tf.timezone_at(lat=data.lat, lng=data.lon)
        if not timezone_name:
            return {"hata": "Timezone bulunamadı."}

        tz = pytz.timezone(timezone_name)
        localized_dt = tz.localize(dt)
        utc_dt = localized_dt.astimezone(pytz.utc)

        # 3. Julian Day hesapla (UTC olarak)
        hour_decimal = utc_dt.hour + utc_dt.minute / 60.0
        julday = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, hour_decimal)

        # 4. Ay burcu
        moon = swe.calc_ut(julday, swe.MOON)[0]
        moon_lon = moon[0]
        burc = get_zodiac(moon_lon)
        derece = round(moon_lon % 30, 2)

        # 5. Ev hesabı
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
            "ev": ev,
            "zamanDilimi": timezone_name
        }

    except Exception as e:
        return {"hata": str(e)}
