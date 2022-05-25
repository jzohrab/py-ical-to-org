import calendar
import datetime


# Ref https://stackoverflow.com/questions/4770297/
#   convert-utc-datetime-string-to-local-datetime
def to_local_datetime(utc_dt):
    """
    convert from utc datetime to a locally aware datetime according to the host timezone

    :param utc_dt: utc datetime
    :return: local timezone datetime
    """
    return datetime.datetime.fromtimestamp(calendar.timegm(utc_dt.timetuple()))


def org_scheduled_dates(start_utc, end_utc, all_day = False):

    def _parts(dt):
        local_dt = to_local_datetime(dt)
        dd, tt = f"{local_dt}".split(' ')
        hh, mm, ss = tt.split(':')
        dayname = local_dt.strftime("%A")[0:3]
        return {
            'utcdatepart': f"{dt}".split(' ')[0],
            'local_date': local_dt,
            'datepart': dd,
            'timepart': ':'.join([hh, mm]),
            'dayname': dayname
        }

    if not all_day:
        s = _parts(start_utc)
        e = _parts(end_utc)

        if s['datepart'] == e['datepart']:
            ret = [
                s['datepart'],
                s['dayname'],
                f"{s['timepart']}-{e['timepart']}"
            ]
            return f"<{' '.join(ret)}>"
        else:
            def _org_string_from_parts(p):
                ret = ' '.join([
                    p['datepart'],
                    p['dayname'],
                    p['timepart']
                ])
                return f'<{ret}>'

            return '-'.join([_org_string_from_parts(p) for p in [s, e]])

    else:
        # ical saves the end date as one past the *actual* end for all-day events.
        actual_end = end_utc + datetime.timedelta(days = -1)
        s = _parts(start_utc)
        e = _parts(actual_end)

        def _utc_to_org(p):
            return f"<{p['utcdatepart']} {p['dayname']}>"

        if s['utcdatepart'] == e['utcdatepart']:
            return _utc_to_org(s)
        else:
            return '-'.join([_utc_to_org(p) for p in [s, e]])
