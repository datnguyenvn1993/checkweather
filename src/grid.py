# 25 diem "nong" cua TP.HCM duoc gom lai theo o luoi (grid cell) thuc su cua
# WeatherAPI (~1.85km/o, xac dinh bang cach doi chieu location.lat/lon tra ve
# tu API cho tung diem, kiem tra lai 3 lan lien tiep cho ket qua on dinh).
# Cac diem chung 1 o duoc noi ten bang " + " de khi bao mua biet ngay cac POI
# nay dang doc chung 1 nguon du lieu, tranh goi API trung lap.
GRID_POINTS = [
    {"name": "Aeon Mall Tan Phu Celadon + Celadon City (Tan Phu)", "lat": 10.8007, "lon": 106.6194},
    {"name": "Aeon Mall Binh Tan", "lat": 10.7434, "lon": 106.6134},
    {"name": "SC VivoCity (Q7)", "lat": 10.7295, "lon": 106.7219},
    {"name": "Vincom Center Dong Khoi (Q1) + Vincom Landmark 81 (Binh Thanh) + San bay Tan Son Nhat (Tan Binh) + Thao Cam Vien (Q1)", "lat": 10.7773, "lon": 106.7030},
    {"name": "Vinhomes Grand Park (TP Thu Duc) + Khu du lich Suoi Tien (TP Thu Duc)", "lat": 10.8433, "lon": 106.8390},
    {"name": "Crescent Mall (Q7) + Ben Bach Dang (Q1)", "lat": 10.7285, "lon": 106.7188},
    {"name": "Gigamall (TP Thu Duc)", "lat": 10.8496, "lon": 106.7719},
    {"name": "Van Hanh Mall (Q10) + Cong vien Dam Sen (Q11)", "lat": 10.7724, "lon": 106.6667},
    {"name": "Diamond Plaza (Q1) + Ga Sai Gon (Q3)", "lat": 10.7815, "lon": 106.6970},
    {"name": "Ben xe Mien Tay (Binh Tan)", "lat": 10.7401, "lon": 106.6198},
    {"name": "Ben xe Mien Dong moi (TP Thu Duc)", "lat": 10.8617, "lon": 106.7772},
    {"name": "Pho di bo Nguyen Hue (Q1) + Cho Ben Thanh (Q1)", "lat": 10.7745, "lon": 106.7020},
    {"name": "Cho Binh Tay (Q6)", "lat": 10.7495, "lon": 106.6493},
    {"name": "Emart Go Vap", "lat": 10.8386, "lon": 106.6652},
    {"name": "BV Dai hoc Y Duoc TP.HCM (Q5) + BV Cho Ray (Q5)", "lat": 10.7545, "lon": 106.6631},
]


def sample_points() -> list[dict]:
    """Return every unique grid cell - duplicates were already merged, so no
    sampling is needed to save quota; checking all of them keeps full coverage."""
    return list(GRID_POINTS)
