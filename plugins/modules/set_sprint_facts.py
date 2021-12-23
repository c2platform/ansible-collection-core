#!/usr/bin/python

from ansible.module_utils.basic import *
from datetime import date
from datetime import datetime
from datetime import timedelta


def get_start_end_dates(year, week):
    d = date(year, 1, 1)
    if(d.weekday() <= 3):
        d = d - timedelta(d.weekday())
    else:
        d = d + timedelta(7 - d.weekday())
    dlt = timedelta(days=(week - 1) * 7)
    return d + dlt, d + dlt + timedelta(days=6)


def sprints(year):
    fcts = []
    for no in range(1, 26):
        wks = [(no * 2) - 1, no * 2]
        s1, e1 = get_start_end_dates(int(year), wks[0])
        s2, e2 = get_start_end_dates(int(year), wks[1])
        sprint_no = str(int(no)).zfill(2)
        sn = '-'.join((str(year), sprint_no))
        sprint = {}
        sprint['weeks'] = wks
        sprint['name'] = sn
        sprint['start'] = s1
        sprint['end'] = e2
        fcts.append(sprint)
    return fcts


def sprint_no_wks_year_from_name(data):
    year, sprint_no = data['name'].split('-')
    wks = [(int(sprint_no) * 2) - 1, int(sprint_no) * 2]
    return sprint_no, wks, year


def sprint_no_wks_year_from_date(data):
    if data['date'] is not None:
        sdate = datetime.strptime(data['date'], '%Y-%m-%d')
    else:
        sdate = date.today()
    isoc = sdate.isocalendar()
    wk = isoc[1]
    if (wk % 2) == 0:
        no = wk / 2
    else:
        no = (wk + 1) / 2
    wks = [(int(no) * 2) - 1, int(no) * 2]
    sprint_no = str(int(no)).zfill(2)
    year = isoc[0]
    return sprint_no, wks, year


def sprint(data):
    fcts = {}
    fcts['sprint'] = {}
    if data['name'] is not None:
        sprint_no, wks, year = sprint_no_wks_year_from_name(data)
    else:
        sprint_no, wks, year = sprint_no_wks_year_from_date(data)
    fcts['sprint']['year'] = year  # REMOVE
    s1, e1 = get_start_end_dates(int(year), wks[0])
    s2, e2 = get_start_end_dates(int(year), wks[1])
    fcts['sprint']['weeks'] = wks
    fcts['sprint']['start'] = s1
    fcts['sprint']['end'] = e2
    fcts['sprint']['name'] = '-'.join((str(year), sprint_no))
    fcts['sprints'] = sprints(year)
    fcts['sprint']['days'] = []
    delta = fcts['sprint']['end'] - fcts['sprint']['start']
    for i in range(delta.days + 1):
        day = (s1 + timedelta(days=i)).strftime("%Y-%m-%d")
        fcts['sprint']['days'].append(day)
    return False, fcts, "Sprint facts set"


def main():
    fields = {
        "date": {"required": False, "type": "str"},
        "name": {"required": False, "type": "str"}
    }

    module = AnsibleModule(argument_spec=fields)
    has_changed, fcts, tr = sprint(module.params)
    module.exit_json(changed=False, ansible_facts=fcts, msg=tr)


if __name__ == '__main__':
    main()
