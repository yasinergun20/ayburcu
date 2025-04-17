from fastapi import FastAPI
from pydantic import BaseModel
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const

app = FastAPI()

class AyBurcuIstek(BaseModel):
    tarih: str     # "1995-04-15"
    saat: str      # "10:45"
    utc: str       # "+03:00"
    lat: float     # 39.92
    lon: float     # 32.85

@app.post("/ayburcu")
def hesapla(data: AyBurcuIstek):
    try:
        # 🔁 Tarih formatını düzelt: '-' yerine '/' kullanılmalı
        tarih_parcali = data.tarih.replace("-", "/")

        # 🔁 Koordinatlar string olmalı, düz float değil
        lat = "{:.6f}".format(data.lat)
        lon = "{:.6f}".format(data.lon)

        # ✅ Flatlib uyumlu datetime objesi
        dt = Datetime(tarih_parcali, data.saat, data.utc)

        # ✅ GeoPos oluştur
        pos = GeoPos(lat, lon)

        # ✅ Harita oluştur ve Ay bilgilerini al
        chart = Chart(dt, pos)
        moon = chart.get(const.MOON)

        return {
            "burc": moon.sign,
            "derece": round(moon.lon, 2),
            "ev": moon.house
        }

    except Exception as e:
        return {"hata": str(e)}
