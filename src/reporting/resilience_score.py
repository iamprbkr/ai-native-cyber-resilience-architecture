from typing import Any


class ResilienceScoreCalculator:
    DETECTION_WEIGHT = 0.25
    RESPONSE_WEIGHT = 0.30
    RECOVERY_WEIGHT = 0.20
    COVERAGE_WEIGHT = 0.15
    COMPLIANCE_WEIGHT = 0.10

    def calculate(
        self,
        detection_score: float,
        response_score: float,
        recovery_score: float,
        coverage_score: float,
        compliance_score: float,
    ) -> dict[str, Any]:
        overall = (
            detection_score * self.DETECTION_WEIGHT
            + response_score * self.RESPONSE_WEIGHT
            + recovery_score * self.RECOVERY_WEIGHT
            + coverage_score * self.COVERAGE_WEIGHT
            + compliance_score * self.COMPLIANCE_WEIGHT
        )
        return {
            "overall": round(overall),
            "detection": round(detection_score),
            "response": round(response_score),
            "recovery": round(recovery_score),
            "coverage": round(coverage_score),
            "compliance": round(compliance_score),
            "weights": {
                "detection": self.DETECTION_WEIGHT,
                "response": self.RESPONSE_WEIGHT,
                "recovery": self.RECOVERY_WEIGHT,
                "coverage": self.COVERAGE_WEIGHT,
                "compliance": self.COMPLIANCE_WEIGHT,
            },
        }
