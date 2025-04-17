from fastapi import FastAPI
from pydantic import BaseModel
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const

app = FastAPI()

class AyBurcuIstek(BaseModel):
    tarih: str
    saat: str
    utc: str
    lat: float
    lon: float

@app.post("/ayburcu")
def hesapla(data: AyBurcuIstek):
    try:
        # Tarihi sayısal olarak ayır
        yil, ay, gun = [int(i) for i in data.tarih.split("-")]
        saat, dakika = [int(i) for i in data.saat.split(":")]

        # Tarihi düzgün string olarak ver
        tarih_str = f"{yil:04d}-{ay:02d}-{gun:02d}"
        saat_str = f"{saat:02d}:{dakika:02d}"

        dt = Datetime(tarih_str, saat_str, data.utc)
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
