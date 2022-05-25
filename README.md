# Python download google ical and write to org file.

A replacement for the nice ical-to-org-via-awk script,
https://github.com/msherry/ical2org/blob/master/ical2org.awk

ical2org.awk is nice, but it wasn't working for me for a few important
things:

* Wasn't correctly interpreting scheduled events with special rules
  (e.g., "repeat every 2 weeks on M, W, F")
* Wouldn't let me mark past events as DONE (at least, not easily!)
* Tricky/sometimes flaky processing of repeated events
* ... it's written in `awk`.  Which is great, but Python is easier to
  grok.  :-P

This script doesn't print all of the details that ical2org.awk does
(such as various properties), it prints out the bare minimum that I
needed for my calendar; namely, the calendar entry title, and the
start and end dates.

Sample schedule.org output:

```
* training
SCHEDULED: <2022-05-23 Mon 13:00-14:00>

* do that thing
SCHEDULED: <2022-05-24 Mon 17:30-18:00>

* Flight to Victoria
SCHEDULED: <2022-05-31 Tue 09:15-14:20>
```

# Install and Usage

This assumes you have python, venv, and pip (or something like venv
and pip).

## Get the code

git clone etc.

## Initial install

```
python3 -m venv .venv
source .venv/bin/activate
.venv/bin/pip3 install -r requirements.txt
deactivate
```

## Config

Copy `config.ini.example` to `config.ini`, and fill in your values.

## Usage

```
python3 -m venv .venv
source .venv/bin/activate
python main.py
deactivate
```

or ...

```
./update-schedule.sh
```

## Cron job

# Cron job

For example, sync things every hour.

```
* */1 * * * pushd /path/to/this/dir && ./update-schedule.sh && popd >> /tmp/cron.out 2>&1
```



# Dev notes

There are just a few tests:

```
python3 -m venv .venv
source .venv/bin/activate
python -m unittest discover -s test
deactivate
```
