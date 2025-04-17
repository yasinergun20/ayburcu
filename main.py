from datetime import datetime
import swisseph as swe
from timezonefinder import TimezoneFinder
import pytz

swe.set_ephe_path('.')

# VERİLER
tarih = "2000-01-01"
saat = "12:00"
lat = 39.92
lon = 32.85

# ZAMAN HESABI
tf = TimezoneFinder()
tz_name = tf.timezone_at(lat=lat, lng=lon)
tz = pytz.timezone(tz_name)

dt = datetime.strptime(f"{tarih} {saat}", "%Y-%m-%d %H:%M")
local_dt = tz.localize(dt)
utc_dt = local_dt.astimezone(pytz.utc)

print("🌐 Timezone:", tz_name)
print("🕒 Yerel:", local_dt)
print("🕒 UTC:", utc_dt)

# JULDAY
utc_hour = utc_dt.hour + utc_dt.minute / 60.0
jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_hour)

# AY BURCU
moon = swe.calc_ut(jd, swe.MOON)[0]
moon_lon = moon[0]
zodiacs = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]
burc = zodiacs[int(moon_lon // 30)]
derece = round(moon_lon % 30, 2)

# EV
cusps, _ = swe.houses(jd, lat, lon, b'P')
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

print("🌕 Ay Burcu:", burc)
print("📐 Derece:", derece)
print("🏠 Ev:", ev)
