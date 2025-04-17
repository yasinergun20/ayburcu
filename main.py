from fastapi import FastAPI
from pydantic import BaseModel
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const

app = FastAPI()

class AyBurcuIstek(BaseModel):
    tarih: str     # örn: "1995-04-15"
    saat: str      # örn: "10:45"
    utc: str       # örn: "+03:00"
    lat: float     # örn: 39.92
    lon: float     # örn: 32.85

@app.post("/ayburcu")
def hesapla(data: AyBurcuIstek):
    try:
        # 🔥 Tarih formatını düzelt: flatlib sadece '/' ile çalışıyor
        yil, ay, gun = data.tarih.split("-")
        tarih = f"{yil}/{ay}/{gun}"  # flatlib bunu istiyor

        # 🔥 Koordinatlar string olarak verilmeli, int/float değil
        lat = f"{data.lat:.6f}"
        lon = f"{data.lon:.6f}"

        dt = Datetime(tarih, data.saat, data.utc)
        pos = GeoPos(lat, lon)
        chart = Chart(dt, pos)
        moon = chart.get(const.MOON)

        return {
            "burc": moon.sign,
            "derece": round(moon.lon, 2),
            "ev": moon.house
        }

    except Exception as e:
        return {"hata": str(e)}
