import unittest

from aegis.network import (
    CommunityResponder,
    Location,
    SafetyNetwork,
    SensorSnapshot,
    WearableDevice,
)


class SafetyNetworkTests(unittest.TestCase):
    def setUp(self) -> None:
        self.network = SafetyNetwork(
            family_contacts=["mother", "sister"],
            authority_contacts=["police-control-room"],
            community_responders=[
                CommunityResponder(
                    responder_id="r-near", name="Nearby Helper", latitude=12.9717, longitude=77.5940
                ),
                CommunityResponder(
                    responder_id="r-far", name="Far Helper", latitude=13.2000, longitude=77.9000
                ),
            ],
            responder_radius_km=5.0,
        )
        self.device = WearableDevice(
            device_id="bracelet-01",
            object_name="bracelet",
            discreet_trigger="double-tap clasp",
        )
        self.network.register_device(self.device)
        self.location = Location(latitude=12.9716, longitude=77.5946, timestamp=1710000000.0)

    def test_manual_trigger_notifies_all_core_channels(self) -> None:
        payload = self.network.trigger_manual_sos("bracelet-01", self.location)

        self.assertEqual(payload["family"], ["mother", "sister"])
        self.assertEqual(payload["authorities"], ["police-control-room"])
        self.assertEqual(payload["community_responders"], ["r-near"])
        self.assertEqual(payload["location"]["latitude"], 12.9716)
        self.assertEqual(payload["signal"]["object_name"], "bracelet")
        self.assertEqual(payload["signal"]["reason"], "manual trigger")

    def test_intelligent_detection_dispatches_on_high_risk_signals(self) -> None:
        snapshot = SensorSnapshot(
            fall_g_force=2.5,
            distress_keyword_detected=True,
            heart_rate_anomaly=True,
        )

        payload = self.network.process_sensor_snapshot(
            device_id="bracelet-01",
            location=self.location,
            snapshot=snapshot,
        )

        self.assertIsNotNone(payload)
        self.assertGreaterEqual(payload["signal"]["confidence"], 0.7)
        self.assertIn("high-impact fall", payload["signal"]["reason"])

    def test_intelligent_detection_ignores_low_risk_signals(self) -> None:
        snapshot = SensorSnapshot(fall_g_force=1.2, distress_keyword_detected=False)

        payload = self.network.process_sensor_snapshot(
            device_id="bracelet-01",
            location=self.location,
            snapshot=snapshot,
        )

        self.assertIsNone(payload)


if __name__ == "__main__":
    unittest.main()
