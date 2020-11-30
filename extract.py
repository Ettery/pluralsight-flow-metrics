"""
   PluralSight Flow metrics extract
   Peter Wood, 2020/01/22
"""
import datetime
import json
import os
from pathlib import Path
from pathlib import PureWindowsPath
from sys import argv

from configuration import Configuration, date_fmt
from contributor import Contributor
from date_utils import DateHelper
from delivery import send_outlook_mail
import export
from team import Team
import rest_calls as api


print("Command line: " + str(argv))

config_file_name = argv[1]
config_file =  PureWindowsPath(config_file_name)

with open(config_file, 'r') as configfile:
    data = configfile.read()
    config_obj = json.loads(data)
    cf = Configuration(config_obj)
    date_fmt = cf.date_fmt

# Change working directory to the location of the config file
os.chdir(config_file.parent)

if cf.initialised:
    dh = DateHelper(cf.date_fmt, cf.week_count)
    api.base_url = cf.base_url

    team = Team(cf.team, cf, dh, cf.token)
    team.build()

    # Load teams for comparison
    compare_team_metrics = []
    for team_name in cf.compare_team_names:
        comp_team = Team(team_name, cf, dh, cf.token)
        comp_team.build()
        compare_team_metrics.append(comp_team.period_metric)

    contributor: Contributor
    for contributor in team.team_members:
        print(contributor.print_period())

        # Build Excel workbook
        file_name = export.write_contributor_to_excel(contributor, team.period_metric, compare_team_metrics)

        # Email workbook to each team member
        subject="Latest Pluralsight Flow stats"
        body="Weekly stats for the last {} weeks to the last month end (adjusted to whole weeks)...".format(cf.week_count)
        send_outlook_mail(cf.email_from, contributor.email, subject, body, [file_name], cf.email_suppress)
        print("Sent {} to {}".format(file_name, contributor.name))

    if(len(cf.team_leads) > 0):
        file_name = export.write_team_to_excel(team, compare_team_metrics)

        # Email workbook to each team member
        subject="Latest Pluralsight Flow stats for the team"
        body="Team stats for the period".format(cf.week_count)

        for mail_to in cf.team_leads:
            send_outlook_mail(cf.email_from, mail_to, subject, body, [file_name], cf.email_suppress)
            print("Sent {} to {}".format(file_name, mail_to))


print("Complete.")

