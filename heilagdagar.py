#!/usr/bin/env python3

import sys
import time
from pprint import pprint
from datetime import timedelta, date

from dateutil.easter import easter


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


def main():
    current_year = time.localtime().tm_year
    year = int(sys.argv[1]) if len(sys.argv) > 1 else current_year
    pprint(generate_norwegian_holidays(year))


if __name__ == "__main__":
    main()
