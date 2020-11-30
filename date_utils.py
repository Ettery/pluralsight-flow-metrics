import datetime

from week import Week

class DateHelper:
    def __init__(self, date_fmt, week_count):
        self.date_fmt = "%Y-%m-%d"
        self.week_count=week_count
        self.__last_month = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
        self.__start_of_week = self.__last_month - datetime.timedelta(days=self.__last_month.weekday())  # Monday
        self.end_date = self.__start_of_week + datetime.timedelta(days=6)  # Sunday
        self.__three_month_int = (self.end_date - datetime.timedelta(weeks=week_count))
        self.start_date = self.__three_month_int - datetime.timedelta(days=self.__three_month_int.weekday())

    def get_week_list(self):
        list = []
        list.append(Week(self.start_date))

        next_date = self.start_date + datetime.timedelta(days=7)
        while next_date < self.end_date:
            list.append(Week(next_date))
            next_date = next_date + datetime.timedelta(days=7)

        return list




