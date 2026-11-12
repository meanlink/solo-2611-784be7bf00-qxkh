import itertools
import math
from datetime import datetime, timedelta, timezone

import numpy as np
from scipy import stats
from sklearn.cluster import DBSCAN, KMeans
from sklearn.ensemble import IsolationForest
from sklearn.feature_selection import mutual_info_classif
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve, silhouette_score
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer


def _metric(label, value, unit="", tone="neutral"):
    if isinstance(value, (np.floating, np.integer)):
        value = value.item()
    return {"label": label, "value": value, "unit": unit, "tone": tone}


def _series(label, value):
    return {"label": str(label), "value": float(value)}


def _envelope(headline, narrative, metrics, series, table, method, caveat):
    return {
        "headline": headline,
        "narrative": narrative,
        "metrics": metrics,
        "series": series,
        "table": table,
        "method": method,
        "caveat": caveat,
    }


def run_primary(rows: list[dict], config: dict) -> dict:
    pairs: dict[str, list[tuple[float, float]]] = {}
    for row in rows:
        pair = str(row.get("pair", "温度-湿度"))
        try:
            pairs.setdefault(pair, []).append((float(row["x"]), float(row["y"])))
        except (KeyError, TypeError, ValueError):
            continue
    records = []
    for pair, values in pairs.items():
        if len(values) < 8:
            continue
        x = np.asarray([item[0] for item in values])
        y = np.asarray([item[1] for item in values])
        pearson = stats.pearsonr(x, y)
        spearman = stats.spearmanr(x, y)
        records.append({
            "pair": pair, "pearson": pearson.statistic, "spearman": spearman.statistic,
            "p_value": pearson.pvalue, "n": len(values)
        })
    if not records:
        raise ValueError("没有足够的相关分析数据")
    p_values = np.asarray([item["p_value"] for item in records])
    order = np.argsort(p_values)
    adjusted = np.empty_like(p_values)
    running = 1.0
    for rank in range(len(order) - 1, -1, -1):
        idx = order[rank]
        running = min(running, p_values[idx] * len(p_values) / (rank + 1))
        adjusted[idx] = running
    for record, q_value in zip(records, adjusted):
        record["q_value"] = float(q_value)
    records.sort(key=lambda item: abs(item["pearson"]), reverse=True)
    top = records[0]
    return _envelope(
        f"{top['pair']} 的相关最强，Pearson r={top['pearson']:.3f}",
        f"在 {len(records)} 组候选传感器对中完成 BH 校正，q={top['q_value']:.4f}。",
        [
            _metric("最强 Pearson", top["pearson"], "", "negative" if abs(top["pearson"]) > .8 else "neutral"),
            _metric("Spearman", top["spearman"], "", "neutral"),
            _metric("BH q 值", top["q_value"], "", "positive" if top["q_value"] < .05 else "neutral"),
            _metric("候选组合", len(records), "组", "neutral"),
        ],
        [_series(item["pair"], round(item["pearson"] * 100, 2)) for item in records[:8]],
        [
            {"label": item["pair"], "pearson": round(item["pearson"], 4),
             "spearman": round(item["spearman"], 4), "q": round(item["q_value"], 5), "n": item["n"]}
            for item in records
        ],
        "pearson_spearman + benjamini_hochberg",
        "相关不代表因果；传感器时钟偏移需在上游同步后才能做实时告警。",
    )



def run_algorithm(rows: list[dict], config: dict) -> dict:
    return run_primary(rows or [], config or {})
