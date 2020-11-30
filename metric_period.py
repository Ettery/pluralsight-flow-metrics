import datetime
from functools import reduce
# from metric_utils import get_recommended_period_metrics

class PeriodMetric:
    def __init__(self):
        self.start_date = datetime.date.today()
        self.end_date = datetime.date(2000,1,1)
        self.days = 0.0
        self.daycommits = 0.0
        self.impact = 0.0
        self.efficiency = 0.0
        self.label = "not set"
        self.rank_val = 0

    # Assumes that all weeks for the period will be added
    def build(self, week_metrics):
        self.start_date = reduce(lambda acc, met: acc if (acc < met.week.week_start) else met.week.week_start, week_metrics, datetime.date.today())
        self.end_date = reduce(lambda acc, met: acc if (acc > met.week.week_end) else met.week.week_end, week_metrics, datetime.date(2000,1,1))

        sums = reduce(lambda a, m: (a[0]+m.days, a[1]+m.daycommits, a[2]+m.impact, a[3]+m.efficiency), week_metrics, (0.0, 0.0, 0.0, 0.0))
        self.days = float(sums[0])/float(len(week_metrics))
        self.daycommits = sums[1]/len(week_metrics)
        self.impact = sums[2]/len(week_metrics)
        self.efficiency = sums[3]/len(week_metrics)

        recomend = get_recommended_period_metrics()
        self.rank_val = (((self.days/recomend.days) + (self.daycommits/recomend.daycommits) + (self.efficiency/recomend.efficiency) + (self.impact/recomend.impact))/4)*100

        #print("{}:{} {} {} {} {} {}".format(self.start_date, self.end_date, self.days, self.daycommits, self.impact, self.efficiency, len(week_metrics)))


    def set_label(self, label):
        self.label = label

    def to_list(self):
        return (
            ["", self.label],
            ["Days/Week", self.days],
            ["Commits/Day", self.daycommits],
            ["Impact", self.impact],
            ["Efficiency", self.efficiency],
            ["% of Recommended", self.rank_val]
        )


def get_recommended_period_metrics() -> PeriodMetric:
    metric = PeriodMetric()
    metric.days = 3.5
    metric.daycommits = 4.5
    metric.impact = 214
    metric.efficiency = 70
    metric.label = "recommended"
    metric.rank_val = 100
    return metric

