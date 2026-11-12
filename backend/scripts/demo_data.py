import math

import numpy as np



def demo_rows():
    rng = np.random.default_rng(1002)
    rows = []
    pairs = ["温度-湿度", "门磁-温度", "振动-电流", "回风-蒸发压力", "霜层-换热效率"]
    for index in range(4800):
        pair = pairs[index % len(pairs)]
        x = float(rng.normal(0, 1))
        rho = [.76, -.48, .62, .35, -.67][index % len(pairs)]
        y = float(rho * x + rng.normal(0, .75))
        rows.append({"pair": pair, "x": round(x, 5), "y": round(y, 5),
                     "warehouse": f"W{index % 18:02d}", "ts": f"2026-10-{index % 28 + 1:02d}T{(index // 28) % 24:02d}:00:00Z"})
    return rows

