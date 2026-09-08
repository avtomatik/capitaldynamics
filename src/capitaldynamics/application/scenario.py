from dataclasses import dataclass
from pathlib import Path

import yaml

from ..domain.schedule import GammaSchedule, GammaSpan


@dataclass(frozen=True)
class Scenario:
    name: str
    analysis_start: int
    gamma: GammaSchedule

    @classmethod
    def from_yaml(cls, path: str | Path) -> "Scenario":
        payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        gamma = tuple(
            GammaSpan(
                int(item["start"]), int(item["end"]), float(item["value"])
            )
            for item in payload["gamma"]
        )
        return cls(
            name=str(payload.get("name", Path(path).stem)),
            analysis_start=int(payload["analysis_start"]),
            gamma=GammaSchedule(gamma),
        )
