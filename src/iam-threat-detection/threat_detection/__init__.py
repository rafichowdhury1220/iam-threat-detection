"""Threat detection engine for identifying suspicious behaviors"""

from datetime import datetime, timedelta
from typing import Optional, List
from uuid import UUID

from ..core.logger import get_logger
from ..models import ThreatType, ThreatLevel

logger = get_logger(__name__)


class ImpossibleTravelDetector:
    """Detects impossible travel based on geographic distance and time"""

    def __init__(self, threshold_km: float, threshold_minutes: int):
        self.threshold_km = threshold_km
        self.threshold_minutes = threshold_minutes

    def calculate_distance(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
    ) -> float:
        """
        Calculate distance between two coordinates using Haversine formula
        Returns distance in kilometers
        """
        from math import radians, sin, cos, sqrt, atan2

        R = 6371  # Earth radius in kilometers

        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c

    def detect(
        self,
        prev_lat: float,
        prev_lon: float,
        prev_time: datetime,
        curr_lat: float,
        curr_lon: float,
        curr_time: datetime,
    ) -> Optional[dict]:
        """
        Detect impossible travel
        Returns threat details if detected, None otherwise
        """
        distance = self.calculate_distance(prev_lat, prev_lon, curr_lat, curr_lon)
        time_diff = (curr_time - prev_time).total_seconds() / 60  # minutes

        if time_diff <= 0:
            return None

        required_speed_kmh = distance / (time_diff / 60)
        max_speed_kmh = (self.threshold_km / self.threshold_minutes) * 60

        if required_speed_kmh > max_speed_kmh:
            logger.warning(
                "Impossible travel detected",
                distance_km=distance,
                time_minutes=time_diff,
                required_speed=required_speed_kmh,
            )
            return {
                "type": ThreatType.IMPOSSIBLE_TRAVEL,
                "level": ThreatLevel.HIGH,
                "distance_km": round(distance, 2),
                "time_minutes": round(time_diff, 2),
                "required_speed_kmh": round(required_speed_kmh, 2),
                "description": f"User traveled {distance:.0f}km in {time_diff:.0f}m "
                              f"(required speed: {required_speed_kmh:.0f}km/h)",
            }
        return None


class FailedLoginDetector:
    """Detects multiple failed login attempts"""

    def __init__(self, threshold: int, window_minutes: int):
        self.threshold = threshold
        self.window_minutes = window_minutes

    def detect(
        self,
        failed_attempts: List[datetime],
        current_time: datetime,
    ) -> Optional[dict]:
        """
        Detect multiple failed logins
        Returns threat details if threshold exceeded
        """
        # Filter attempts within the time window
        cutoff_time = current_time - timedelta(minutes=self.window_minutes)
        recent_attempts = [
            attempt for attempt in failed_attempts
            if attempt >= cutoff_time
        ]

        if len(recent_attempts) >= self.threshold:
            logger.warning(
                "Multiple failed logins detected",
                count=len(recent_attempts),
                window_minutes=self.window_minutes,
            )
            return {
                "type": ThreatType.MULTIPLE_FAILED_LOGINS,
                "level": ThreatLevel.HIGH,
                "attempt_count": len(recent_attempts),
                "window_minutes": self.window_minutes,
                "description": f"{len(recent_attempts)} failed login attempts "
                              f"within {self.window_minutes} minutes",
            }
        return None


class PrivilegeEscalationDetector:
    """Detects unauthorized or suspicious privilege escalations"""

    @staticmethod
    def detect(
        user_id: UUID,
        current_role: str,
        target_role: str,
        escalation_reason: Optional[str] = None,
    ) -> Optional[dict]:
        """
        Detect suspicious privilege escalation
        """
        from .auth import RBACService

        role_level_map = {
            "guest": 10,
            "user": 20,
            "manager": 50,
            "security_officer": 80,
            "admin": 100,
        }

        current_level = role_level_map.get(current_role, 0)
        target_level = role_level_map.get(target_role, 0)

        # Flag if escalating to higher privilege
        if target_level > current_level:
            logger.warning(
                "Privilege escalation detected",
                user_id=str(user_id),
                from_role=current_role,
                to_role=target_role,
            )
            return {
                "type": ThreatType.PRIVILEGE_ESCALATION,
                "level": ThreatLevel.CRITICAL,
                "from_role": current_role,
                "to_role": target_role,
                "description": f"User escalated from {current_role} to {target_role}",
            }
        return None


class ThreatDetectionEngine:
    """Main threat detection orchestrator"""

    def __init__(
        self,
        impossible_travel_threshold_km: float,
        impossible_travel_time_minutes: int,
        failed_login_threshold: int,
        failed_login_window: int,
    ):
        self.impossible_travel_detector = ImpossibleTravelDetector(
            impossible_travel_threshold_km,
            impossible_travel_time_minutes,
        )
        self.failed_login_detector = FailedLoginDetector(
            failed_login_threshold,
            failed_login_window,
        )
        self.privilege_escalation_detector = PrivilegeEscalationDetector()

    def analyze_login(
        self,
        user_id: UUID,
        prev_location: Optional[tuple],  # (lat, lon, datetime)
        curr_location: tuple,  # (lat, lon, datetime)
        ip_address: str,
    ) -> List[dict]:
        """Analyze login event for threats"""
        threats = []

        # Check for impossible travel
        if prev_location and curr_location:
            threat = self.impossible_travel_detector.detect(
                prev_location[0],
                prev_location[1],
                prev_location[2],
                curr_location[0],
                curr_location[1],
                curr_location[2],
            )
            if threat:
                threats.append(threat)

        return threats

    def analyze_failed_logins(
        self,
        user_id: UUID,
        recent_failures: List[datetime],
    ) -> Optional[dict]:
        """Analyze failed login attempts"""
        return self.failed_login_detector.detect(
            recent_failures,
            datetime.utcnow(),
        )

    def analyze_privilege_escalation(
        self,
        user_id: UUID,
        current_role: str,
        target_role: str,
    ) -> Optional[dict]:
        """Analyze privilege escalation request"""
        return self.privilege_escalation_detector.detect(
            user_id,
            current_role,
            target_role,
        )
