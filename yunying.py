import postgresql

db = postgresql.open('pq://root:123456@localhost:5432/ddqc')


def create_collect_data_sql(start_date, end_date):
    return "select * from state_charging t where t.ending_time>=to_date('%s','yyyy-mm-dd') and t.ending_time<to_date('%s','yyyy-mm-dd') " % (
    start_date, end_date)

def create_non_holiday_sql(start_date, end_date):
    return  """
select holiday.week_day, count(*) as day_times
from holiday
where holiday.state <> '2'
  and holiday.date > '%s'
  and holiday.date < '%s'
group by holiday.week_day
""" % (start_date, end_date)

def create_station_daily_charging_sql():
    return """
    select from  ;
"""

def run():
    sql1 = create_collect_data_sql("201801", "201812")
    b.execute("create table tmp01 as (%s)" % (sql1))
    
    

