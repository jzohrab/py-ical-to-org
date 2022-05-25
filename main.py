from icalevents.icalevents import events
import configparser
import calendar
import datetime

from utils import org_scheduled_dates, to_local_datetime


def fetch_events(url, startdate, enddate):
    """Fetch events and add data to assist."""
    es  = events(url = url, start = startdate, end = enddate)
    for e in es:
        e.localstart = to_local_datetime(e.start)
        e.localend = to_local_datetime(e.end)
        e.orgschedule = org_scheduled_dates(e.start, e.end, e.all_day)
    es.sort(key=lambda x: x.localstart)
    return es


def print_all(es):
    """Debugging method only."""
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

def writeorgfile(orgfile,
                 headers,
                 events):

    def __entry(event):
        return f"""* {e.summary}
SCHEDULED: {e.orgschedule}

"""

    with open(orgfile, 'w') as f:
        f.write(headers)
        for e in events:
            f.write(__entry(e))


def orgfile_header(config):
    """String to write at top of file."""
    return f"""#+TITLE:       {config['title']}
#+UPDATED:     {datetime.datetime.now()}
#+CATEGORY:    {config['category']}
#+FILETAGS:    {config['filetags']}
"""


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config = config['CONFIG']

    # Ensure have all config values before fetching/writing.
    url = config['url']
    startdate = config['start_date']
    startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    maxdays = int(config['max_future_days'])
    enddate = datetime.date.today() + datetime.timedelta(days=maxdays)
    headers = orgfile_header(config)
    orgfile = config['org_file']

    events = fetch_events(url, startdate, enddate)
    # print_all(events)

    markpastasDONE = config.get('mark_past_as_done', False)
    if markpastasDONE:
        now = datetime.datetime.now()
        done = [e for e in events if e.localend < now]
        for e in done:
            e.summary = f"DONE {e.summary}"

    writeorgfile(orgfile = orgfile,
                 headers = headers,
                 events = events)


if __name__ == '__main__':
    main()
