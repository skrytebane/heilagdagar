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
        (date(year, 1, 1), "Nyttårsdag", "https://nn.wikipedia.org/wiki/Nytt%C3%A5r"),
        (date(year, 12, 25), "Førstedag jul", "https://nn.wikipedia.org/wiki/Juledag"),
        (
            date(year, 12, 26),
            "Annandag jul",
            "https://nn.wikipedia.org/wiki/Andre_juledag",
        ),
        (
            date(year, 5, 1),
            "Internasjonal arbeidardag",
            "https://nn.wikipedia.org/wiki/F%C3%B8rste_mai",
        ),
        (
            date(year, 5, 17),
            "Grunnlovsdagen",
            "https://nn.wikipedia.org/wiki/Den_norske_grunnlovsdagen",
        ),
        # Easter, pentecost, etc.
        (
            easter_sunday - timedelta(days=3),
            "Skjærtorsdag",
            "https://nn.wikipedia.org/wiki/Skj%C3%A6rtorsdag",
        ),
        (
            easter_sunday - timedelta(days=2),
            "Langfredag",
            "https://nn.wikipedia.org/wiki/Langfredag",
        ),
        (easter_sunday, "Påskedagen", "https://nn.wikipedia.org/wiki/P%C3%A5skedag"),
        (
            easter_sunday + timedelta(days=1),
            "Annandag påske",
            "https://nn.wikipedia.org/wiki/Andre_p%C3%A5skedag",
        ),
        (
            easter_sunday + timedelta(days=39),
            "Kristi himmelfartsdag",
            "https://nn.wikipedia.org/wiki/Kristi_himmelferdsdag",
        ),
        (
            easter_sunday + timedelta(days=49),
            "Førstedag pinse",
            "https://nn.wikipedia.org/wiki/Pinse",
        ),
        (
            easter_sunday + timedelta(days=50),
            "Annandag pinse",
            "https://nn.wikipedia.org/wiki/Andre_pinsedag",
        ),
    ]


def make_uid(name: str, year):
    clean = re.sub(r"\s+", "-", name).lower()
    return f"no-{clean}-{year}@example.com"


def make_holiday_event(created, holiday):
    dt, name, url = holiday
    e = Event()
    e.uid = make_uid(name, dt.year)
    e.name = name
    e.begin = dt
    e.make_all_day()
    e.duration = timedelta(days=1)
    e.created = created
    e.url = url
    return e


def make_ical_file(holidays):
    created = datetime.now().astimezone()
    return Calendar(
        events=[make_holiday_event(created, holiday) for holiday in holidays]
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
