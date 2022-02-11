#!/usr/bin/env python3

import sys
import time
import re
from pprint import pprint
from datetime import timedelta, date, datetime

from dateutil.easter import easter
from ics import Calendar, Event


def generate_norwegian_holidays(year):
    easter_sunday = easter(year)

    return {
        # Fixed holidays
        "Nyttårsdag": date(year, 1, 1),
        "Førstedag jul": date(year, 12, 25),
        "Annandag jul": date(year, 12, 26),
        "Internasjonal arbeidardag": date(year, 5, 1),
        "Grunnlovsdagen": date(year, 5, 17),
        # Easter, pentecost, etc.
        "Skjærtorsdag": easter_sunday - timedelta(days=3),
        "Langfredag": easter_sunday - timedelta(days=2),
        "Påskeaftan": easter_sunday - timedelta(days=1),
        "Påskedagen": easter_sunday,
        "Annandag påske": easter_sunday + timedelta(days=1),
        "Kristi himmelfartsdag": easter_sunday + timedelta(days=39),
        "Førstedag pinse": easter_sunday + timedelta(days=49),
        "Annandag pinse": easter_sunday + timedelta(days=50),
    }


def make_uid(name: str, year):
    clean = re.sub(r"\s+", "-", name).lower()
    return f"no-{clean}-{year}@example.com"


def make_ical_file(holidays):
    cal = Calendar()
    created = datetime.now().astimezone()

    sorted_holidays = sorted(holidays.items(), key=lambda x: x[1])
    for name, dt in sorted_holidays:
        e = Event()
        e.uid = make_uid(name, dt.year)
        e.name = name
        e.begin = dt
        e.make_all_day()
        # e.duration = timedelta(days=1)
        e.created = created
        cal.events.add(e)

    return cal


def main():
    current_year = time.localtime().tm_year
    year = int(sys.argv[1]) if len(sys.argv) > 1 else current_year
    holidays = generate_norwegian_holidays(year)
    print(make_ical_file(holidays, 2022, 2024))


if __name__ == "__main__":
    main()
