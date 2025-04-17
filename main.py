from fastapi import FastAPI
from pydantic import BaseModel
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const

app = FastAPI()

class AyBurcuIstek(BaseModel):
    tarih: str  # "1995-04-15"
    saat: str   # "10:45"
    utc: str    # "+03:00"
    lat: float  # 39.92
    lon: float  # 32.85

@app.post("/ayburcu")
def hesapla(data: AyBurcuIstek):
    try:
        # Flatlib için tarih formatını düzelt
        tarih = data.tarih.replace("-", "/")  # Flatlib 'yyyy/mm/dd' ister

        # Koordinatları string'e çevir
        lat_str = "{:.6f}".format(data.lat)  # örn: "39.920000"
        lon_str = "{:.6f}".format(data.lon)

        # Flatlib nesneleri
        dt = Datetime(tarih, data.saat, data.utc)
        pos = GeoPos(lat_str, lon_str)

        chart = Chart(dt, pos)
        moon = chart.get(const.MOON)

        return {
            "burc": moon.sign,
            "derece": round(moon.lon, 2),
            "ev": moon.house
        }

    except Exception as e:
        return {"hata": str(e)}
