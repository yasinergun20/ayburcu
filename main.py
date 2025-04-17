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
        print("Gelen veri:")
        print(f"Tarih: {data.tarih}, Saat: {data.saat}, UTC: {data.utc}")
        print(f"Lat: {data.lat}, Lon: {data.lon}")

        dt = Datetime(data.tarih, data.saat, data.utc)
        print(f"Datetime objesi: {dt}")
        
        pos = GeoPos(str(data.lat), str(data.lon))
        chart = Chart(dt, pos)
        moon = chart.get(const.MOON)

        return {
            "burc": moon.sign,
            "derece": round(moon.lon, 2),
            "ev": moon.house
        }

    except Exception as e:
        print(f"HATA: {e}")
        return {"hata": str(e)}
