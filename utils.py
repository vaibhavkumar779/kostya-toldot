from datetime import date, timedelta
import re

date_patterns = ['(?P<date>\d{1,2}) (?P<month>\w*)( (?P<year>\d{4}) года)?',
                 '(?P<month>\w*) (?P<date>\d{1,2}), (?P<year>\d{4})']
month2int = {
    'января': 1,
    'февраля': 2,
    'марта': 3,
    'апреля': 4,
    'мая': 5,
    'июня': 6,
    'июля': 7,
    'августа': 8,
    'сентября': 9,
    'октября': 10,
    'ноября': 11,
    'декабря': 12,
    'january': 1,
    'february': 2,
    'march': 3,
    'april': 4,
    'may': 5,
    'june': 6,
    'july': 7,
    'august': 8,
    'september': 9,
    'october': 10,
    'november': 11,
    'december': 12
}


def string2date(date_string: str) -> date:
    date_string = date_string.lower().strip()
    today = date.today()

    if date_string == 'сегодня':
        day = today
    elif date_string == 'вчера':
        day = today - timedelta(days=1)
    else:
        for date_pattern in date_patterns:
            m = re.match(date_pattern, date_string)
            if m is None:
                continue
            mg = m.groupdict()

            day = mg.get('date')
            month = mg.get('month')
            year = mg.get('year')

            if None in [day, month]:
                continue

            day = int(day)
            month_int = month2int[month]

            if year is None:
                year = today.year
            else:
                year = int(year)

            day = today.replace(year, month_int, day)
            break
        else:
            day = today

    return day

