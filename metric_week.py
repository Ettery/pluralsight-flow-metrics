from configuration import date_fmt
from metric_period import get_recommended_period_metrics

class WeekMetric:
    def __init__(self, week, days: int, commits: int, daycommits: float, impact: float, churnsum: float, locsum: float):
        self.week = week
        self.days = days
        self.commits = commits
        self.daycommits = daycommits
        self.impact = impact
        self.churnsum = churnsum
        self.locsum = locsum
        self.efficiency = 0 if locsum == 0 else 100 * (1-(self.churnsum/self.locsum))  
        recomend = get_recommended_period_metrics()
        self.rank_val = (((self.days/recomend.days) + (self.daycommits/recomend.daycommits) + (self.efficiency/recomend.efficiency) + (self.impact/recomend.impact))/4)*100

    def to_dict(self):
        return {"WeekStart": self.week.week_start.strftime(date_fmt), "Week":self.week.label, "Days": round(self.days, 1), "Commits/Day": round(self.daycommits, 1), "Impact": round(self.impact, 1), "Efficiency": round(self.efficiency, 1), "Commits": self.commits, "% Recommended": round(self.rank_val, 1)}
