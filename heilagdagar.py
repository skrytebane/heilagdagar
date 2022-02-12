#!/usr/bin/env python3

import time
import re
from datetime import timedelta, date, datetime

from dateutil.easter import easter
from ics import Calendar, Event


def generate_norwegian_holidays(year):
    easter_sunday = easter(year)

    return [
        # Fixed holidays
        (date(year, 1, 1), "Nyttårsdag"),
        (date(year, 12, 25), "Førstedag jul"),
        (date(year, 12, 26), "Annandag jul"),
        (date(year, 5, 1), "Internasjonal arbeidardag"),
        (date(year, 5, 17), "Grunnlovsdagen"),
        # Easter, pentecost, etc.
        (easter_sunday - timedelta(days=3), "Skjærtorsdag"),
        (easter_sunday - timedelta(days=2), "Langfredag"),
        (easter_sunday - timedelta(days=1), "Påskeaftan"),
        (easter_sunday, "Påskedagen"),
        (easter_sunday + timedelta(days=1), "Annandag påske"),
        (easter_sunday + timedelta(days=39), "Kristi himmelfartsdag"),
        (easter_sunday + timedelta(days=49), "Førstedag pinse"),
        (easter_sunday + timedelta(days=50), "Annandag pinse"),
    ]


def make_uid(name: str, year):
    clean = re.sub(r"\s+", "-", name).lower()
    return f"no-{clean}-{year}@example.com"


def make_holiday_event(created, name, dt):
    e = Event()
    e.uid = make_uid(name, dt.year)
    e.name = name
    e.begin = dt
    e.make_all_day()
    e.duration = timedelta(days=1)
    e.created = created
    return e


def make_ical_file(holidays):
    created = datetime.now().astimezone()
    return Calendar(
        events=[make_holiday_event(created, name, dt) for dt, name in holidays]
    )


def main():
    current_year = time.localtime().tm_year
    holidays = [
        holiday
        for year in range(current_year - 1, current_year + 6)
        for holiday in generate_norwegian_holidays(year)
    ]
    print(make_ical_file(holidays))


if __name__ == "__main__":
    main()
