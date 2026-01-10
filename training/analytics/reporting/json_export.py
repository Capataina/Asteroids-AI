"""
JSON export functionality.

Handles saving raw training data as JSON.
"""

import json
from datetime import datetime
from typing import Dict, Any

from training.analytics.collection.models import AnalyticsData


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

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2)

    print(f"[OK] Raw training data saved to: {output_path}")
    return output_path
