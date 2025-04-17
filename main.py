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
        # 🔁 Tarih formatı düzelt
        tarih_str = data.tarih.replace("-", "/")  # flatlib yyyy/mm/dd istiyor

        # ✅ Flatlib Datetime ve GeoPos kullan
        dt = Datetime(tarih_str, data.saat, data.utc)
        pos = GeoPos(str(float(data.lat)), str(float(data.lon)))  # float → str

        # ✅ Chart oluştur ve Ay'ı al
        chart = Chart(dt, pos)
        moon = chart.get(const.MOON)

        return {
            "burc": moon.sign,
            "derece": round(moon.lon, 2),
            "ev": moon.house
        }

    except Exception as e:
        return {"hata": str(e)}
