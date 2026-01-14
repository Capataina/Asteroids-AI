import json
import os
import unittest
import uuid

from training.analytics.collection.models import AnalyticsData
from training.analytics.reporting.json_export import save_json


class TestJsonExportNumpyTypes(unittest.TestCase):
    def test_save_json_handles_numpy_scalars_and_arrays(self):
        class ScalarLike:
            def __init__(self, value):
                self._value = value

            def item(self):
                return self._value

        class ArrayLike:
            def __init__(self, values):
                self._values = list(values)

            def tolist(self):
                return list(self._values)

        data = AnalyticsData()
        data.set_config({
            "method": "test",
            "population_size": ScalarLike(5),
        })

        data.generations_data.append({
            "generation": 1,
            "best_fitness": ScalarLike(123.25),
            "sigma": ScalarLike(0.15),
            "some_array": ArrayLike([1.0, 2.0, 3.0]),
        })

        summary = {
            "all_time_best": ScalarLike(123.25),
            "flag": ScalarLike(True),
        }

        out_path = os.path.join(
            os.path.dirname(__file__),
            f"__tmp_training_data_{uuid.uuid4().hex}.json",
        )
        try:
            save_json(out_path, data, summary)
            with open(out_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
        finally:
            try:
                os.remove(out_path)
            except FileNotFoundError:
                pass

        self.assertEqual(loaded["config"]["population_size"], 5)
        self.assertAlmostEqual(loaded["summary"]["all_time_best"], 123.25, places=5)
        self.assertEqual(loaded["summary"]["flag"], True)
        self.assertEqual(loaded["generations"][0]["some_array"], [1.0, 2.0, 3.0])


if __name__ == "__main__":
    unittest.main()
