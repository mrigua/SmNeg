from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

import numpy as np


@dataclass
class FrameItem:
    index: int
    path: str
    base_positive: np.ndarray
    cyan: int = 0
    magenta: int = 0
    yellow: int = 0
    density: int = 0
    contrast: float = 1.0
    saturation: float = 1.0
    rotation: int = 0
    mirror: bool = False
    auto_crop: bool = False
    show_clipping: bool = False
    is_passed: bool = False
    manual_crop: tuple[float, float, float, float] | None = None
    sharpness: int = 0
    processed_date: str = field(default_factory=lambda: date.today().isoformat())
    straighten: float = 0.0
    tone_profile: str = "Natural"
