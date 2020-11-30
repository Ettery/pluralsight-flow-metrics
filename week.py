import datetime
from functools import reduce
from typing import List

from metric_week import WeekMetric

class Week:
    def __init__(self, start_date):
        self.week_start = start_date
        self.week_end = self.week_start + datetime.timedelta(days=6)
        self.label = start_date.strftime("%G.%V")
        self.metrics = []
    
    def add_metric(self, metric):
        self.metrics.append(metric)

    def build_week_metrics(self):
        if(len(self.metrics) > 0):
            days = self.date_count(self.metrics)
            commits = reduce(lambda acc, met: acc+met.id_count, self.metrics, 0)
            daycommits = float(commits)/float(days)
            impact = reduce(lambda a, m: a+m.impact, self.metrics, 0)
            sums = reduce(lambda a, m: (a[0]+m.churn, a[1]+m.haloc), self.metrics, (0,0))
            return WeekMetric(self, days, commits, daycommits, impact, sums[0], sums[1])
        else:
            return WeekMetric(self, 0, 0, 0, 0, 0, 0)


    def date_count(self, metrics):
        dates = []
        for metric in metrics:
            dates.append(metric.date_str)
        return len(set(dates))


    def clone(self):
        return Week(self.week_start)


def clone_weeks(weeks: List[Week]) -> List[Week]:
    clones = []
    for week in weeks:
        clones.append(week.clone())

    return clones        