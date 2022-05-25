from icalevents.icalevents import events
import configparser
import calendar
import datetime

from utils import org_scheduled_dates, to_local_datetime


def todate(s):
    format = '%Y-%m-%d'
    return datetime.datetime.strptime(s, format)


def fetch_events(url, startdate, enddate):
    es  = events(url = url, start = startdate, end = enddate)
    for e in es:
        e.localstart = to_local_datetime(e.start)
        e.localend = to_local_datetime(e.end)
        e.orgschedule = org_scheduled_dates(e.start, e.end, e.all_day)
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
            'localstart', 'localend',
            'orgschedule'
        ]
        for k in keys:
            print(f'  {k}: {getattr(e, k)}')

def writeorgfile(events,
                 orgfile,
                 title,
                 category,
                 filetags):

    headings = f"""#+TITLE:       {title}
#+UPDATED:     {datetime.datetime.now()}
#+CATEGORY:    {category}
#+FILETAGS:    {filetags}

"""

    def __entry(event):
        return f"""* {e.summary}
{e.orgschedule}

"""

    with open(orgfile, 'w') as f:
        f.write(headings)
        for e in events:
            f.write(__entry(e))


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config = config['CONFIG']
    url = config['URL']
    startdate = todate(config['STARTDATE'])
    maxdays = int(config['MAXFUTUREDAYS'])
    enddate = datetime.date.today() + datetime.timedelta(days=maxdays)

    title = config['TITLE']
    category = config['CATEGORY']
    filetags = config['FILETAGS']
    orgfile = config['ORGFILE']

    events = fetch_events(url, startdate, enddate)
    # print_all(events)

    writeorgfile(events,
                 orgfile = orgfile,
                 title = title,
                 category = category,
                 filetags = filetags)


if __name__ == '__main__':
    main()
