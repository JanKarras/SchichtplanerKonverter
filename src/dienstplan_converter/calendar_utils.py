from .models import DayEntry, MonthSchedule

MONTH_NAMES = ("", "Januar", "Februar", "März", "April", "Mai", "Juni",
               "Juli", "August", "September", "Oktober", "November", "Dezember")
WEEKDAY_NAMES = ("Mo", "Di", "Mi", "Do", "Fr", "Sa", "So")


def splitMonth(days: tuple[DayEntry, ...]) -> tuple[tuple[DayEntry, ...], tuple[DayEntry, ...]]:
    midpoint = (len(days) + 1) // 2
    return days[:midpoint], days[midpoint:]


def outputFilename(schedule: MonthSchedule) -> str:
    return f"Dienstplan_Klein_{MONTH_NAMES[schedule.month]}_{schedule.year}.pdf"
