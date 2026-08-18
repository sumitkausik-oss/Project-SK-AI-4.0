"""
SK Enterprises | Autonomous Data Analyst Suite
Founder, Inventor & Sole Architect: Sumit Kumar
Platform V5.0 — Domain Hub: Data Intelligence Engine
Zero external dependencies (stdlib + optional pandas fallback)
"""
import json
import csv
import math
import statistics
import io
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    import pandas as pd
    import numpy as np
    _PANDAS_AVAILABLE = True
except ImportError:
    _PANDAS_AVAILABLE = False


def _safe_float(v: Any) -> Optional[float]:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


class DataAnalystEngine:
    """
    SK Enterprises — Autonomous Data Analyst Suite
    Stdlib-first with pandas fallback for richer EDA.
    Inventor: Sumit Kumar
    """

    @staticmethod
    def parse_csv_text(csv_text: str) -> Dict:
        """Parse raw CSV string into structured column data."""
        reader = csv.DictReader(io.StringIO(csv_text.strip()))
        rows = list(reader)
        if not rows:
            return {"error": "Empty CSV payload"}
        columns = {col: [] for col in rows[0].keys()}
        for row in rows:
            for col, val in row.items():
                columns[col].append(val.strip())
        return {"row_count": len(rows), "columns": list(columns.keys()), "data": columns}

    @staticmethod
    def profile_dataset(csv_text: str) -> Dict:
        """
        Full EDA profiling: types, nulls, numeric summary stats,
        outlier flags, top 5 values per column.
        """
        parsed = DataAnalystEngine.parse_csv_text(csv_text)
        if "error" in parsed:
            return parsed

        columns = parsed["data"]
        profile = {}

        for col, values in columns.items():
            numeric_vals = [_safe_float(v) for v in values if _safe_float(v) is not None]
            null_count = sum(1 for v in values if v in ("", "null", "NULL", "None", "NA", "N/A"))
            col_type = "numeric" if len(numeric_vals) > len(values) * 0.7 else "categorical"

            entry: Dict[str, Any] = {
                "type": col_type,
                "total_count": len(values),
                "null_count": null_count,
                "null_pct": round(null_count / len(values) * 100, 2)
            }

            if col_type == "numeric" and numeric_vals:
                mean = statistics.mean(numeric_vals)
                stdev = statistics.stdev(numeric_vals) if len(numeric_vals) > 1 else 0.0
                q1 = statistics.quantiles(numeric_vals, n=4)[0] if len(numeric_vals) >= 4 else min(numeric_vals)
                q3 = statistics.quantiles(numeric_vals, n=4)[2] if len(numeric_vals) >= 4 else max(numeric_vals)
                iqr = q3 - q1
                outliers = [v for v in numeric_vals if v < (q1 - 1.5 * iqr) or v > (q3 + 1.5 * iqr)]

                entry.update({
                    "min": round(min(numeric_vals), 4),
                    "max": round(max(numeric_vals), 4),
                    "mean": round(mean, 4),
                    "median": round(statistics.median(numeric_vals), 4),
                    "std_dev": round(stdev, 4),
                    "q1": round(q1, 4),
                    "q3": round(q3, 4),
                    "iqr": round(iqr, 4),
                    "outlier_count": len(outliers),
                    "outlier_values": outliers[:5]
                })
            else:
                from collections import Counter
                freq = Counter(values).most_common(5)
                unique = len(set(values))
                entry.update({
                    "unique_count": unique,
                    "top_5_values": [{"value": v, "count": c} for v, c in freq]
                })

            profile[col] = entry

        return {
            "row_count": parsed["row_count"],
            "column_count": len(columns),
            "profile": profile,
            "pandas_available": _PANDAS_AVAILABLE,
            "generated_by": "Data Analyst Engine — Sumit Kumar (SK Enterprises)"
        }

    @staticmethod
    def correlation_matrix(csv_text: str) -> Dict:
        """Pearson correlation between numeric columns."""
        parsed = DataAnalystEngine.parse_csv_text(csv_text)
        if "error" in parsed:
            return parsed

        numeric_cols = {}
        for col, vals in parsed["data"].items():
            floats = [_safe_float(v) for v in vals]
            if all(f is not None for f in floats):
                numeric_cols[col] = floats

        if len(numeric_cols) < 2:
            return {"error": "Need at least 2 numeric columns for correlation"}

        col_names = list(numeric_cols.keys())
        matrix = {}
        for c1 in col_names:
            matrix[c1] = {}
            for c2 in col_names:
                x = numeric_cols[c1]
                y = numeric_cols[c2]
                n = len(x)
                if n < 2:
                    matrix[c1][c2] = None
                    continue
                mean_x = statistics.mean(x)
                mean_y = statistics.mean(y)
                num = sum((a - mean_x) * (b - mean_y) for a, b in zip(x, y))
                den_x = math.sqrt(sum((a - mean_x) ** 2 for a in x))
                den_y = math.sqrt(sum((b - mean_y) ** 2 for b in y))
                corr = round(num / (den_x * den_y), 4) if den_x * den_y != 0 else 0.0
                matrix[c1][c2] = corr

        return {
            "columns": col_names,
            "correlation_matrix": matrix,
            "interpretation": "Values close to 1 = strong positive, -1 = strong negative, 0 = no correlation",
            "generated_by": "Data Analyst Engine — Sumit Kumar (SK Enterprises)"
        }

    @staticmethod
    def detect_outliers(csv_text: str, column: str) -> Dict:
        """IQR-based outlier detection for a single column."""
        parsed = DataAnalystEngine.parse_csv_text(csv_text)
        if "error" in parsed:
            return parsed
        vals = [_safe_float(v) for v in parsed["data"].get(column, [])]
        nums = [v for v in vals if v is not None]
        if len(nums) < 4:
            return {"error": f"Insufficient data in column '{column}'"}
        q1 = statistics.quantiles(nums, n=4)[0]
        q3 = statistics.quantiles(nums, n=4)[2]
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outliers = [(i, v) for i, v in enumerate(nums) if v < lower or v > upper]
        return {
            "column": column,
            "total_rows": len(nums),
            "outlier_count": len(outliers),
            "outlier_bounds": {"lower": round(lower, 4), "upper": round(upper, 4)},
            "outliers": [{"row_index": r, "value": v} for r, v in outliers[:20]],
            "generated_by": "Data Analyst Engine — Sumit Kumar (SK Enterprises)"
        }

    @staticmethod
    def generate_chart_spec(csv_text: str, chart_type: str = "bar", x_col: str = None,
                             y_col: str = None) -> Dict:
        """
        Generate Chart.js-compatible JSON spec for cyberpunk frontend rendering.
        Supports: bar, line, scatter, pie.
        """
        parsed = DataAnalystEngine.parse_csv_text(csv_text)
        if "error" in parsed:
            return parsed

        cols = parsed["data"]
        col_names = list(cols.keys())
        x = x_col or col_names[0]
        y = y_col or (col_names[1] if len(col_names) > 1 else col_names[0])

        labels = cols.get(x, [])[:50]
        data_vals = [_safe_float(v) or 0.0 for v in (cols.get(y, [])[:50])]

        cyberpunk_colors = [
            "rgba(0, 245, 212, 0.8)", "rgba(0, 180, 255, 0.8)",
            "rgba(255, 165, 0, 0.8)", "rgba(220, 38, 127, 0.8)"
        ]

        spec = {
            "type": chart_type,
            "data": {
                "labels": labels,
                "datasets": [{
                    "label": y,
                    "data": data_vals,
                    "backgroundColor": cyberpunk_colors[0],
                    "borderColor": cyberpunk_colors[1],
                    "borderWidth": 2,
                    "fill": chart_type == "line"
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {"legend": {"display": True, "position": "top"}},
                "scales": {"x": {"grid": {"color": "rgba(0,245,212,0.1)"}},
                           "y": {"grid": {"color": "rgba(0,245,212,0.1)"}}}
            },
            "meta": {
                "x_column": x,
                "y_column": y,
                "row_count": parsed["row_count"],
                "generated_by": "Data Analyst Engine — Sumit Kumar (SK Enterprises)"
            }
        }
        return spec

    @staticmethod
    def generate_summary_report(csv_text: str) -> Dict:
        """Executive summary combining profile + correlation for admin reporting."""
        profile = DataAnalystEngine.profile_dataset(csv_text)
        corr = DataAnalystEngine.correlation_matrix(csv_text)
        return {
            "executive_summary": {
                "dataset_rows": profile.get("row_count"),
                "dataset_columns": profile.get("column_count"),
                "data_quality": "GOOD" if all(
                    p.get("null_pct", 0) < 10 for p in profile.get("profile", {}).values()
                ) else "MODERATE",
                "high_correlation_pairs": [
                    f"{c1}↔{c2}: {corr['correlation_matrix'][c1][c2]}"
                    for c1 in corr.get("correlation_matrix", {})
                    for c2 in corr.get("correlation_matrix", {}).get(c1, {})
                    if c1 != c2 and abs(corr['correlation_matrix'][c1][c2] or 0) > 0.7
                ][:5]
            },
            "column_profile": profile.get("profile"),
            "correlation_matrix": corr.get("correlation_matrix"),
            "generated_by": "Data Analyst Engine — Sumit Kumar (SK Enterprises)"
        }
