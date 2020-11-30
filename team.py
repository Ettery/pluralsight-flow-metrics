from contributor import Contributor
from metric_period import PeriodMetric
import rest_calls as api


class Team:
    def __init__(self, team_name, config, date_helper, token):
        self.team_name = team_name
        self.token = token
        self.dh = date_helper
        self.cf = config
        self.date_fmt = config.date_fmt
        self.start_date = self.dh.start_date.strftime(self.date_fmt)
        self.end_date = self.dh.end_date.strftime(self.date_fmt)
        self.team = {}
        self.team_members = []
        self.period_metric = PeriodMetric()

    def load_data(self):
        self.team = api.get_team(self.team_name, self.token)
        print("Successfully retrieved team: "+self.team["name"]+", ID = "+str(self.team["id"]))

        self.team_members = api.get_contributors(self.team, self.token)
        print(str(len(self.team_members)) + " team members retrieved.")

        # Get the commit metrics for the defined period
        api.add_metrics_to_all(self.team_members, self.start_date, self.end_date, self.token, self.date_fmt)


    def calculate(self):
        all_aggs = []
        weeks = self.dh.get_week_list()

        contributor: Contributor
        for contributor in self.team_members:
            contributor.build_weekly_aggs(weeks)
            all_aggs.extend(contributor.week_metrics)

        # Reduce the all_aggs metric collection to a single period metric
        self.period_metric.build(all_aggs)
        self.period_metric.set_label(self.team_name)

    def build(self):
        self.load_data()
        self.calculate()        
        
    def __str__(self):
        return self.team_name