import random

# Approximate center coordinates covering HCMC districts + outlying rural districts.
# Large districts (Cu Chi, Binh Chanh, Can Gio, Thu Duc) get multiple sub-points
# since rain in Saigon is often very localized.
GRID_POINTS = [
    {"name": "Quan 1", "lat": 10.7769, "lon": 106.7009},
    {"name": "Quan 3", "lat": 10.7843, "lon": 106.6819},
    {"name": "Quan 4", "lat": 10.7578, "lon": 106.7038},
    {"name": "Quan 5", "lat": 10.7546, "lon": 106.6634},
    {"name": "Quan 6", "lat": 10.7462, "lon": 106.6353},
    {"name": "Quan 7 (trung tam)", "lat": 10.7340, "lon": 106.7220},
    {"name": "Quan 7 (Phu My Hung)", "lat": 10.7180, "lon": 106.7014},
    {"name": "Quan 8", "lat": 10.7231, "lon": 106.6285},
    {"name": "Quan 10", "lat": 10.7726, "lon": 106.6672},
    {"name": "Quan 11", "lat": 10.7631, "lon": 106.6520},
    {"name": "Quan 12 (trung tam)", "lat": 10.8672, "lon": 106.6414},
    {"name": "Quan 12 (Tan Thoi Nhat)", "lat": 10.8850, "lon": 106.6200},
    {"name": "Binh Thanh", "lat": 10.8106, "lon": 106.7091},
    {"name": "Binh Thanh (Landmark 81)", "lat": 10.7952, "lon": 106.7218},
    {"name": "Phu Nhuan", "lat": 10.7994, "lon": 106.6802},
    {"name": "Tan Binh", "lat": 10.8014, "lon": 106.6528},
    {"name": "Tan Phu", "lat": 10.7906, "lon": 106.6285},
    {"name": "Go Vap", "lat": 10.8386, "lon": 106.6652},
    {"name": "Binh Tan", "lat": 10.7652, "lon": 106.6027},
    {"name": "Binh Tan (An Lac)", "lat": 10.7365, "lon": 106.5762},
    {"name": "TP Thu Duc (Q2 cu - Thao Dien)", "lat": 10.8030, "lon": 106.7440},
    {"name": "TP Thu Duc (Q9 cu - Long Truong)", "lat": 10.8410, "lon": 106.7890},
    {"name": "TP Thu Duc (Cat Lai)", "lat": 10.7739, "lon": 106.7890},
    {"name": "TP Thu Duc (Linh Trung)", "lat": 10.8700, "lon": 106.7700},
    {"name": "TP Thu Duc (Suoi Tien)", "lat": 10.8622, "lon": 106.8034},
    {"name": "Nha Be", "lat": 10.6959, "lon": 106.7433},
    {"name": "Hoc Mon", "lat": 10.8843, "lon": 106.5953},
    {"name": "Hoc Mon (Nhi Xuan)", "lat": 10.9150, "lon": 106.5700},
    {"name": "Cu Chi (thi tran)", "lat": 10.9724, "lon": 106.4931},
    {"name": "Cu Chi (Phu Hoa Dong)", "lat": 10.9500, "lon": 106.5700},
    {"name": "Binh Chanh (trung tam)", "lat": 10.6890, "lon": 106.5940},
    {"name": "Binh Chanh (Vinh Loc)", "lat": 10.8280, "lon": 106.5860},
    {"name": "Binh Chanh (Le Minh Xuan)", "lat": 10.7280, "lon": 106.5230},
    {"name": "Can Gio (Binh Khanh)", "lat": 10.6209, "lon": 106.7911},
    {"name": "Can Gio (Can Thanh)", "lat": 10.4093, "lon": 106.9556},
]


def sample_points(min_count: int = 24, max_count: int = 30) -> list[dict]:
    """Randomly sample between min_count and max_count grid points."""
    count = random.randint(min_count, min(max_count, len(GRID_POINTS)))
    return random.sample(GRID_POINTS, count)
