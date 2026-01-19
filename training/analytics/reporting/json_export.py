"""
JSON export functionality.

Handles saving raw training data as JSON.
"""

import json
import math
from datetime import datetime
from typing import Dict, Any, Tuple

from training.analytics.collection.models import AnalyticsData


try:
    import numpy as np  # type: ignore
except Exception:  # pragma: no cover - numpy should be present, but keep exporter resilient
    np = None


def _json_default(obj: Any):
    """
    JSON serializer for objects not supported by default json code.

    Primarily handles NumPy scalar/array types (e.g., float32) which appear in
    analytics operator stats and distributions.
    """
    if np is not None:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.bool_):
            return bool(obj)

    if isinstance(obj, datetime):
        return obj.isoformat()

    tolist = getattr(obj, "tolist", None)
    if callable(tolist):
        return tolist()

    # Common scalar-like objects (including some non-numpy types) can expose .item().
    item = getattr(obj, "item", None)
    if callable(item):
        return item()

    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


def save_json(output_path: str, data: AnalyticsData, summary: Dict[str, Any]) -> str:
    """Save raw training data as JSON.

    Args:
        output_path: Path to write the JSON file
        data: AnalyticsData instance containing training data
        summary: Summary statistics dictionary

    Returns:
        Path to the saved file
    """
    export_data = {
        'schema_version': data.SCHEMA_VERSION,
        'config': data.config,
        'start_time': data.start_time.isoformat(),
        'end_time': datetime.now().isoformat(),
        'summary': summary,
        'generations': data.generations_data,
        'fresh_game_data': data.fresh_game_data,
        'distributions_data': data.distributions_data,
    }

    def _sanitize(obj: Any) -> Tuple[Any, int]:
        """
        Recursively sanitize non-finite floats (NaN/Inf) to keep JSON strict.

        Returns:
            (sanitized_object, replacements_count)
        """
        if obj is None:
            return None, 0

        if isinstance(obj, float):
            if not math.isfinite(obj):
                return None, 1
            return obj, 0

        if np is not None and isinstance(obj, np.floating):
            value = float(obj)
            if not math.isfinite(value):
                return None, 1
            return value, 0

        if isinstance(obj, (str, int, bool)):
            return obj, 0

        if np is not None and isinstance(obj, np.integer):
            return int(obj), 0

        if np is not None and isinstance(obj, np.bool_):
            return bool(obj), 0

        if isinstance(obj, datetime):
            return obj.isoformat(), 0

        if isinstance(obj, list):
            out = []
            count = 0
            for item in obj:
                sanitized_item, c = _sanitize(item)
                out.append(sanitized_item)
                count += c
            return out, count

        if isinstance(obj, tuple):
            sanitized_list, count = _sanitize(list(obj))
            return sanitized_list, count

        if isinstance(obj, dict):
            out = {}
            count = 0
            for key, value in obj.items():
                sanitized_value, c = _sanitize(value)
                out[key] = sanitized_value
                count += c
            return out, count

        sanitized = _json_default(obj)
        return _sanitize(sanitized)

    export_data, nonfinite_replacements = _sanitize(export_data)
    if nonfinite_replacements:
        export_data["export_nonfinite_replacements"] = nonfinite_replacements

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, default=_json_default, allow_nan=False)

    print(f"[OK] Raw training data saved to: {output_path}")
    return output_path
