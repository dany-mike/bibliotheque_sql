import datetime

def get_date(date):
    return str(date[0]) + '-' + str(date[1]) + '-' + str(date[2])

def get_next_month_date(date):
    return date + datetime.timedelta(days=30)