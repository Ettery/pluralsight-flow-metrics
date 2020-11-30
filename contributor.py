from typing import List

from metric_period import PeriodMetric
from week import Week, clone_weeks
class Contributor:
    def __init__(self, id, name, email, last_activity_at):
        self.id = id
        self.name = name
        self.email = email
        self.last_activity_at = last_activity_at
        self.metrics = []
        self.week_metrics = []
        self.period_metric = PeriodMetric()

    def __str__(self):
        return self.name + " [" + str(self.id) + "]; metrics: " + str(len(self.metrics))
    
    def get_metrics_count(self):
         return len(self.metrics)

    def build_weekly_aggs(self, weeks: List[Week]):
        week: Week
        weeks = clone_weeks(weeks)
        for metric in self.metrics:
            week = list(filter(lambda w: w.label == metric.week, weeks))[0]
            week.add_metric(metric)

        self.week_metrics = []
        for week in weeks:
            self.week_metrics.append(week.build_week_metrics())

        self.period_metric.build(self.week_metrics)
        self.period_metric.set_label(self.name)

    def to_dict(self):
        return {}

    def print_period(self):
        return "{} : {} - {} \nDays: {}  DayCommits: {}  Impact: {}  Efficiency: {}".format(self.name, self.period_metric.start_date, self.period_metric.end_date, self.period_metric.days, self.period_metric.daycommits, self.period_metric.impact, self.period_metric.efficiency)
