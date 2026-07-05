import random

# Diem "nong" cua TP.HCM: trung tam thuong mai, khu vui choi, dau moi giao thong,
# khu dan cu dong duc, benh vien. Thay cho luoi toa do ngau nhien truoc day vi day
# la nhung noi tap trung dong nguoi can canh bao mua som nhat.
GRID_POINTS = [
    {"name": "Aeon Mall Tan Phu Celadon", "lat": 10.8007, "lon": 106.6194},
    {"name": "Aeon Mall Binh Tan", "lat": 10.7434, "lon": 106.6134},
    {"name": "SC VivoCity (Q7)", "lat": 10.7295, "lon": 106.7219},
    {"name": "Vincom Center Dong Khoi (Q1)", "lat": 10.7773, "lon": 106.7030},
    {"name": "Vincom Landmark 81 (Binh Thanh)", "lat": 10.7949, "lon": 106.7218},
    {"name": "Vinhomes Grand Park (TP Thu Duc)", "lat": 10.8433, "lon": 106.8390},
    {"name": "Crescent Mall (Q7)", "lat": 10.7285, "lon": 106.7188},
    {"name": "Gigamall (TP Thu Duc)", "lat": 10.8496, "lon": 106.7719},
    {"name": "Van Hanh Mall (Q10)", "lat": 10.7724, "lon": 106.6667},
    {"name": "Diamond Plaza (Q1)", "lat": 10.7815, "lon": 106.6970},
    {"name": "Ben xe Mien Tay (Binh Tan)", "lat": 10.7401, "lon": 106.6198},
    {"name": "Ben xe Mien Dong moi (TP Thu Duc)", "lat": 10.8617, "lon": 106.7772},
    {"name": "San bay Tan Son Nhat (Tan Binh)", "lat": 10.8188, "lon": 106.6520},
    {"name": "Ga Sai Gon (Q3)", "lat": 10.7823, "lon": 106.6785},
    {"name": "Ben Bach Dang (Q1)", "lat": 10.7745, "lon": 106.7057},
    {"name": "Cong vien Dam Sen (Q11)", "lat": 10.7632, "lon": 106.6367},
    {"name": "Khu du lich Suoi Tien (TP Thu Duc)", "lat": 10.8622, "lon": 106.8034},
    {"name": "Thao Cam Vien (Q1)", "lat": 10.7878, "lon": 106.7053},
    {"name": "Pho di bo Nguyen Hue (Q1)", "lat": 10.7745, "lon": 106.7020},
    {"name": "Celadon City (Tan Phu)", "lat": 10.8010, "lon": 106.6187},
    {"name": "Cho Ben Thanh (Q1)", "lat": 10.7725, "lon": 106.6981},
    {"name": "Cho Binh Tay (Q6)", "lat": 10.7495, "lon": 106.6493},
    {"name": "Emart Go Vap", "lat": 10.8386, "lon": 106.6652},
    {"name": "BV Dai hoc Y Duoc TP.HCM (Q5)", "lat": 10.7545, "lon": 106.6631},
    {"name": "BV Cho Ray (Q5)", "lat": 10.7565, "lon": 106.6602},
]


def sample_points(min_count: int = 24, max_count: int = 30) -> list[dict]:
    """Randomly sample between min_count and max_count grid points."""
    count = random.randint(min_count, min(max_count, len(GRID_POINTS)))
    return random.sample(GRID_POINTS, count)
