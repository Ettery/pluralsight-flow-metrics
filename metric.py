from datetime import datetime
from decimal import Decimal
from typing import List

from contributor import Contributor
from week import Week

class Metric:
    def __init__(self, churn, haloc, id_count, local_date, impact, date_fmt):
        self.churn = churn
        self.haloc = haloc
        self.id_count = id_count
        self.date_str = local_date
        self.date = datetime.strptime(local_date, date_fmt)
        self.week = self.date.strftime("%G.%V")
        self.impact = impact




