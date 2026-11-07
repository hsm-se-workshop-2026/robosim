import json
import unittest

from src import browser_api


class BrowserApiTests(unittest.TestCase):
    def setUp(self) -> None:
        browser_api.reset()

    def test_reset_includes_track_and_initial_robot_state(self) -> None:
        state = json.loads(browser_api.reset())

        self.assertEqual(len(state["track"]), 360)
        self.assertAlmostEqual(state["x"], state["track"][0]["x"])
        self.assertAlmostEqual(state["y"], state["track"][0]["y"])
        self.assertAlmostEqual(state["distance"], 0.0)

    def test_manual_key_moves_robot_and_release_stops_it(self) -> None:
        browser_api.set_mode("manual")
        browser_api.press_key("w")
        moving = json.loads(browser_api.step())
        browser_api.release_key()
        stopped = json.loads(browser_api.step())

        self.assertGreater(moving["y"], 0.0)
        self.assertAlmostEqual(stopped["x"], moving["x"])
        self.assertAlmostEqual(stopped["y"], moving["y"])

    def test_invalid_mode_and_manual_key_are_reported(self) -> None:
        with self.assertRaises(ValueError):
            browser_api.set_mode("unknown")
        with self.assertRaises(RuntimeError):
            browser_api.press_key("w")
        browser_api.set_mode("manual")
        with self.assertRaises(ValueError):
            browser_api.press_key("x")


if __name__ == "__main__":
    unittest.main()
