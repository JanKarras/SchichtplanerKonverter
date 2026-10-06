from dataclasses import dataclass


@dataclass(frozen=True)
class DayEntry:
    day: int
    weekday: str
    primaryValue: str | None
    secondaryValue: str | None


@dataclass(frozen=True)
class MonthSchedule:
    employee: str
    year: int
    month: int
    days: tuple[DayEntry, ...]
