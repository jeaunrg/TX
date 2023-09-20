import calendar
import datetime

MONTHS = calendar.month_name[1:]


def year_choices():
    return [(r, r) for r in range(1970, datetime.date.today().year + 100)]


def current_year():
    return datetime.date.today().year


def get_next_month(month: str, year: int) -> str:
    index = MONTHS.index(month)
    if index + 1 == len(MONTHS):
        return MONTHS[0], year + 1
    else:
        return MONTHS[index + 1], year


def current_month():
    month_num = datetime.date.today().month
    return calendar.month_name[month_num]
