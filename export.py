from configuration import date_fmt
from contributor import Contributor
from metric_week import WeekMetric
from metric_period import PeriodMetric
from metric_period import get_recommended_period_metrics
from team import Team

import os
from pathlib import PureWindowsPath
from typing import List
import xlsxwriter
from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet
from xlsxwriter.utility import xl_rowcol_to_cell

def get_file_path(contributor: Contributor, ext: str) -> str:
    file_name = "{}\\{} {} - {}.{}".format(os.getcwd(), contributor.name, contributor.period_metric.start_date, contributor.period_metric.end_date, ext)
    try:
        os.remove(file_name)
    except OSError:
        pass
    return file_name

def get_file_path2(file_name: str, ext: str) -> str:
    file_name = "{}\\{}.{}".format(os.getcwd(), file_name, ext)
    try:
        os.remove(file_name)
    except OSError:
        pass
    return file_name

def setup_workbook(file_name: str) -> (str, Workbook, Worksheet, object):
    file_path = get_file_path2(file_name, "xlsx")
    workbook = xlsxwriter.Workbook(file_path)
    bold = workbook.add_format({'bold': True})
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0,0,18)
    worksheet.set_column(1,20,12)

    return (file_path, workbook, worksheet, bold)


def write_period_metrics(row: int, metrics: [], worksheet, with_header: bool, bold, title: str) -> int:
    metric: PeriodMetric
    col = 0
    header_done = False

    if title != "" and len(metrics) > 0:
        worksheet.write(row, 0, title, bold)
        row += 1

    for metric in metrics:
        if with_header and not header_done:
            for item, val in metric.to_list():
                worksheet.write(row, col, item, bold)
                col += 1
            row += 1
            header_done = True

        col = 0
        for item, val in metric.to_list():
            worksheet.write(row, col, round(val, 1) if isinstance(val, (int, float)) else val)
            col= col+1
        row += 1
    
    return row


def write_weekly_metrics(row: int, metrics: [], worksheet, bold, title: str) -> int:
    metric: WeekMetric
    col = 0

    if title != "":
        worksheet.write(row, 0, title, bold)
        row += 1

    first = True
    row += 1
    for metric in metrics:
        row += 1
        col = 0
        values = metric.to_dict()
        for key in values:
            if first:
                worksheet.write(row-2, col, key, bold)
                if col > 1:
                    range = "{}:{}".format(xl_rowcol_to_cell(row, col), xl_rowcol_to_cell(row+len(metrics)-1, col))
                    worksheet.add_sparkline(row-1, col, {'range': range})

            worksheet.write(row, col, values[key])
            col += 1
        
        first = False

    return row

def write_contributor_to_excel(contributor: Contributor, team_metrics: PeriodMetric, compare_teams: []) -> str:

    file_name = "{} {} - {}".format(contributor.name, contributor.period_metric.start_date, contributor.period_metric.end_date)
    (file_path, workbook, worksheet, bold) = setup_workbook(file_name)

    worksheet.write("A1", contributor.name, bold)
    worksheet.write("A2", "From:", bold)
    worksheet.write("B2", contributor.period_metric.start_date.strftime(date_fmt))
    worksheet.write("C2", "To:", bold)
    worksheet.write("D2", contributor.period_metric.end_date.strftime(date_fmt))

    row: int = 3
    row = write_period_metrics(row, [contributor.period_metric, team_metrics, get_recommended_period_metrics()], worksheet, True, bold, "")

    row += 1
    compare_metrics = [m for m in compare_teams]
    compare_metrics.append(team_metrics)
    compare_metrics = sorted(compare_metrics, key=lambda m: m.rank_val, reverse=True)    
    row = write_period_metrics(row, compare_metrics, worksheet, False, bold, "Comparative Teams - Ranked")

    row += 2
    row = write_weekly_metrics(row, contributor.week_metrics, worksheet, bold, "Weekly Metrics for {}".format(contributor.name))

    workbook.close()
    
    return file_path


def write_team_to_excel(team: Team, compare_teams: []) -> str:

    file_name = "{} {} - {}".format(team, team.start_date, team.end_date)
    (file_path, workbook, worksheet, bold) = setup_workbook(file_name)

    worksheet.write("A1", "{} team".format(team.team_name.capitalize()) , bold)
    worksheet.write("A2", "From:", bold)
    worksheet.write("B2", team.start_date)
    worksheet.write("C2", "To:", bold)
    worksheet.write("D2", team.end_date)

    row: int = 3
    compare_metrics = [m for m in compare_teams]
    compare_metrics.extend([team.period_metric, get_recommended_period_metrics()])
    compare_metrics = sorted(compare_metrics, key=lambda m: m.rank_val, reverse=True)    
    row = write_period_metrics(row, compare_metrics, worksheet, True, bold, "Team Rankings")

    contributor_metrics = list(map(lambda member: member.period_metric, team.team_members))
    contributor_metrics = sorted(contributor_metrics, key=lambda m: m.rank_val, reverse=True)
    row += 2
    row = write_period_metrics(row, contributor_metrics, worksheet, True, bold, "Team Members")

    workbook.close()
    
    return file_path