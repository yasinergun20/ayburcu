from fastapi import FastAPI
from pydantic import BaseModel
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const
from flatlib.tools import houses

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
        tarih = data.tarih.replace("-", "/")
        dt = Datetime(tarih, data.saat, data.utc)
        pos = GeoPos(data.lat, data.lon)

        # ❌ hsys='PLACIDUS' kullanılmıyor!
        chart = Chart(dt, pos)

        moon = chart.get(const.MOON)
        moon_house = houses.getHouse(chart, moon)

        return {
            "burc": moon.sign,
            "derece": round(moon.lon, 2),
            "ev": moon_house
        }

    except Exception as e:
        return {"hata": str(e)}
