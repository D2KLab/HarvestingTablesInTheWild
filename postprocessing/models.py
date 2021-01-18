# pylint: disable=invalid-name
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class OrangeProbabilisticItem:
    confidence: float


@dataclass
class OrangeKeyColumn(OrangeProbabilisticItem):
    keyColumn: int


@dataclass
class OrangeOrientation(OrangeProbabilisticItem):
    orientation: str


@dataclass
class OrangeHeader(OrangeProbabilisticItem):
    header: List[str]


@dataclass
class OrangeTyping(OrangeProbabilisticItem):
    type: str


@dataclass
class OrangePreprocessLight:
    orientation: OrangeOrientation
    header: OrangeHeader
    keyColumn: OrangeKeyColumn
    primitiveTyping: Dict[str, OrangeTyping]
    dataType: Dict[str, OrangeTyping]


@dataclass
class OrangePreprocessHeavy(OrangePreprocessLight):
    raw_table: List[List[str]]
    restructured_table: List[List[str]]
