from fastapi import FastAPI, Query
from flatlib.geopos import GeoPos
from flatlib.datetime import Datetime
from flatlib.chart import Chart
from flatlib.const import MOON

app = FastAPI()

def hesapla_ay_burcu(yil, ay, gun, saat, dakika, enlem, boylam):
    pos = GeoPos(str(enlem), str(boylam))
    date = Datetime(f"{yil}-{ay:02d}-{gun:02d}", f"{saat:02d}:{dakika:02d}", '+03:00')  # Türkiye sabit saat dilimi
    chart = Chart(date, pos, hsys='PLACIDUS')
    moon = chart.get(MOON)
    return {
        "burc": moon.sign,
        "derece": round(moon.lon % 30, 2),
        "ev": moon.house
    }

@app.get("/ayburcu")
def ay_burcu_api(
    yil: int = Query(...),
    ay: int = Query(...),
    gun: int = Query(...),
    saat: int = Query(...),
    dakika: int = Query(...),
    enlem: float = Query(...),
    boylam: float = Query(...)
):
    return hesapla_ay_burcu(yil, ay, gun, saat, dakika, enlem, boylam)
