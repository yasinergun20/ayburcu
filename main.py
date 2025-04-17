from fastapi import FastAPI
from pydantic import BaseModel
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const

app = FastAPI()

class AyBurcuIstek(BaseModel):
    tarih: str  # Tarih string olarak kalmalı!
    saat: str
    utc: str
    lat: float
    lon: float

@app.post("/ayburcu")
def hesapla(data: AyBurcuIstek):
    try:
        # Tüm veriler string olarak alınır
        tarih = str(data.tarih)
        saat = str(data.saat)
        utc = str(data.utc)

        dt = Datetime(tarih, saat, utc)
        pos = GeoPos(str(data.lat), str(data.lon))
        chart = Chart(dt, pos)
        moon = chart.get(const.MOON)

        return {
            "burc": moon.sign,
            "derece": round(moon.lon, 2),
            "ev": moon.house
        }

    except Exception as e:
        return {"hata": str(e)}
