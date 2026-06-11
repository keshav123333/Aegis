from __future__ import annotations

from dataclasses import dataclass, field
from math import asin, cos, radians, sin, sqrt
from time import time
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Location:
    latitude: float
    longitude: float
    timestamp: float = field(default_factory=time)


@dataclass(frozen=True)
class WearableDevice:
    device_id: str
    object_name: str
    discreet_trigger: str


@dataclass(frozen=True)
class SensorSnapshot:
    fall_g_force: float = 0.0
    distress_keyword_detected: bool = False
    heart_rate_anomaly: bool = False
    manual_override: bool = False


@dataclass(frozen=True)
class EmergencySignal:
    device: WearableDevice
    location: Location
    confidence: float
    reason: str


@dataclass(frozen=True)
class CommunityResponder:
    responder_id: str
    name: str
    latitude: float
    longitude: float


class EmergencyDetector:
    """Simple, explainable risk scoring for intelligent emergency detection."""

    def __init__(self, trigger_threshold: float = 0.7) -> None:
        self.trigger_threshold = trigger_threshold

    def evaluate(self, snapshot: SensorSnapshot) -> Optional[tuple[float, str]]:
        reasons: List[str] = []
        score = 0.0

        if snapshot.manual_override:
            return 1.0, "manual override"

        if snapshot.fall_g_force >= 2.2:
            score += 0.45
            reasons.append("high-impact fall")
        if snapshot.distress_keyword_detected:
            score += 0.35
            reasons.append("distress phrase")
        if snapshot.heart_rate_anomaly:
            score += 0.25
            reasons.append("heart-rate anomaly")

        if score >= self.trigger_threshold:
            return min(score, 1.0), ", ".join(reasons)
        return None


class SafetyNetwork:
    """Modular SOS dispatch network for family, authorities, and nearby responders."""

    def __init__(
        self,
        *,
        family_contacts: List[str],
        authority_contacts: List[str],
        community_responders: List[CommunityResponder],
        detector: Optional[EmergencyDetector] = None,
        responder_radius_km: float = 5.0,
    ) -> None:
        self.family_contacts = family_contacts
        self.authority_contacts = authority_contacts
        self.community_responders = community_responders
        self.detector = detector or EmergencyDetector()
        self.responder_radius_km = responder_radius_km
        self._devices: Dict[str, WearableDevice] = {}

    def register_device(self, device: WearableDevice) -> None:
        self._devices[device.device_id] = device

    def trigger_manual_sos(self, device_id: str, location: Location) -> dict:
        device = self._devices[device_id]
        signal = EmergencySignal(
            device=device,
            location=location,
            confidence=1.0,
            reason="manual trigger",
        )
        return self._dispatch(signal)

    def process_sensor_snapshot(
        self, *, device_id: str, location: Location, snapshot: SensorSnapshot
    ) -> Optional[dict]:
        device = self._devices[device_id]
        detected = self.detector.evaluate(snapshot)
        if not detected:
            return None
        confidence, reason = detected
        signal = EmergencySignal(
            device=device,
            location=location,
            confidence=confidence,
            reason=reason,
        )
        return self._dispatch(signal)

    def _dispatch(self, signal: EmergencySignal) -> dict:
        location_payload = {
            "latitude": signal.location.latitude,
            "longitude": signal.location.longitude,
            "timestamp": signal.location.timestamp,
        }
        nearby = self._nearby_responders(signal.location)
        return {
            "signal": {
                "device_id": signal.device.device_id,
                "object_name": signal.device.object_name,
                "reason": signal.reason,
                "confidence": signal.confidence,
            },
            "location": location_payload,
            "family": self.family_contacts,
            "authorities": self.authority_contacts,
            "community_responders": [responder.responder_id for responder in nearby],
        }

    def _nearby_responders(self, location: Location) -> List[CommunityResponder]:
        return [
            responder
            for responder in self.community_responders
            if _haversine_km(
                location.latitude,
                location.longitude,
                responder.latitude,
                responder.longitude,
            )
            <= self.responder_radius_km
        ]


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_km = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)
    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    return 2 * radius_km * asin(sqrt(a))
