from icalevents.icalevents import events
import configparser
import calendar
import datetime


def todate(s):
    format = '%Y-%m-%d'
    return datetime.datetime.strptime(s, format)

# Ref https://stackoverflow.com/questions/4770297/
#   convert-utc-datetime-string-to-local-datetime
def to_local_datetime(utc_dt):
    """
    convert from utc datetime to a locally aware datetime according to the host timezone

    :param utc_dt: utc datetime
    :return: local timezone datetime
    """
    return datetime.datetime.fromtimestamp(calendar.timegm(utc_dt.timetuple()))


def fetch_events(url, startdate, enddate):
    es  = events(url = url, start = startdate, end = enddate)
    for e in es:
        e.localstart = to_local_datetime(e.start)
        e.localend = to_local_datetime(e.end)
    es.sort(key=lambda x: x.localstart)
    return es


def print_all(es):
    for e in es:
        print('---')
        print(e.summary)
        # print(e)  !! don't do this, throws error
        keys = [
            'uid',
            'start', 'end', 'all_day',
            'localstart', 'localend'
        ]
        for k in keys:
            print(f'  {k}: {getattr(e, k)}')


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config = config['CONFIG']
    url = config['URL']
    startdate = todate(config['STARTDATE'])
    maxdays = int(config['MAXFUTUREDAYS'])
    enddate = datetime.date.today() + datetime.timedelta(days=maxdays)

    es = fetch_events(url, startdate, enddate)
    print_all(es)


if __name__ == '__main__':
    main()
