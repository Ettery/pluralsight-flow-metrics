import json

date_fmt = "%Y-%m-%d"

class Configuration:
    def __init__(self, config_obj):
        if config_obj != None:
            self.config_obj = config_obj
            self.token=str(config_obj['token'])
            self.week_count=config_obj['week-count']
            self.team=str(config_obj['team'])
            self.date_fmt=str(config_obj['date-format'])
            self.base_url=str(config_obj['base-url'])
            self.smtp_server=str(config_obj['smtp-server'])
            self.email_from=str(config_obj['email-from'])
            self.email_suppress= (False if str(config_obj['email-suppress'])=="N" else True)

            c_teams = str(config_obj['compare-teams'])
            self.compare_team_names = [] if c_teams == "" else c_teams.split(",")
            team_ls = str(config_obj['team-leads'])
            self.team_leads = [] if team_ls == "" else team_ls.split(",")

            self.initialised = True
        else:
            self.initialised = False


