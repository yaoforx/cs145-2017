import sqlite3
from prettytable import from_db_cursor

# copy and paste your SQL queries into each of the below variables
# note: do NOT rename variables

Q1 = '''
SELECT AVG(arr_delay) as avg_delay FROM flight_delays
WHERE year = 2017 AND month = 7
'''

Q2 = '''
SELECT MAX(arr_delay) as max_delay FROM flight_delays
WHERE year = 2017 AND month = 7

'''

Q3 = '''
SELECT carrier, fl_num, origin_city_name, dest_city_name, fl_date
    FROM flight_delays
    WHERE arr_delay = (SELECT MAX(arr_delay) FROM flight_delays WHERE year = 2017 AND month = 7)
'''

Q4 = '''
SELECT weekday_name,sub.avg_delay
FROM weekdays
INNER JOIN (SELECT AVG(arr_delay) AS avg_delay,day_of_week
      FROM flight_delays
    GROUP BY day_of_week)sub
ON weekdays.weekday_id = sub.day_of_week
ORDER BY avg_delay DESC
'''

Q5 = '''
SELECT airline_name, avg_delay
FROM
(
    SELECT AVG(arr_delay) as avg_delay, airline_id
    FROM flight_delays
    GROUP BY airline_id
)sub1
INNER JOIN
(
    SELECT airline_id
    FROM flight_delays
    WHERE origin_city_name = 'San Francisco, CA' AND year = 2017 AND month  = 7 
    GROUP BY airline_id
)sub2
ON sub1.airline_id = sub2.airline_id
INNER JOIN
airlines
ON sub1.airline_id = airlines.airline_id
ORDER BY avg_delay DESC
'''

Q6 = '''
SELECT COUNT(t2. down)*1.0/COUNT(t1.up) as late_proportion
FROM(SELECT carrier as up FROM flight_delays GROUP BY carrier)t1
LEFT JOIN
(SELECT carrier as down FROM flight_delays GROUP BY carrier HAVING AVG(arr_delay)>=10)t2
on t1.up = t2. down
'''

Q7 = '''
SELECT SUM(arr*dep-arr*dd-dep*ad+ad*dd)/COUNT(*) as cov
FROM (SELECT arr_delay as arr, dep_delay as dep 
    FROM flight_delays
    --WHERE dep_delay > 0
)t1
CROSS JOIN(
    SELECT AVG(arr_delay) as ad, AVG(dep_delay) as dd
    FROM flight_delays
    --WHERE dep_delay > 0
)t2
'''

Q8 = '''
select airline_name, MAX(sub2.after - sub1.before) as delay_increase

FROM (
    select AVG(arr_delay) as before, airline_id, day_of_month
    FROM flight_delays
    WHERE month = 7 AND day_of_month <= 23 
    GROUP BY carrier
    )sub1
INNER JOIN (
    select AVG(arr_delay) as after,airline_id
    FROM flight_delays
  WHERE month = 7 AND day_of_month > 23
   GROUP BY carrier
)sub2
ON sub1.airline_id = sub2.airline_id
INNER JOIN
airlines
ON sub1.airline_id = airlines.airline_id
'''

Q9 = '''
select airline_name
FROM (
    select airline_id
    FROM flight_delays
    WHERE month = 7 AND dest = 'PDX' AND origin = 'SFO'
    GROUP BY carrier
    )sub1
INNER JOIN (
    select airline_id
    FROM flight_delays
    WHERE month = 7 AND dest = 'EUG' AND origin = 'SFO'
    GROUP BY carrier
)sub2
ON sub1.airline_id = sub2.airline_id
INNER JOIN
airlines
ON sub1.airline_id = airlines.airline_id
'''

Q10 = '''
select origin, dest, AVG(arr_delay) AS avg_delay
FROM flight_delays
WHERE (origin = 'MDW' OR origin = 'ORD') AND (dest = 'SFO' OR dest = 'SJC' OR dest = 'OAK') AND (crs_dep_time > 1400)
GROUP BY origin, dest
ORDER BY avg_delay DESC
'''

#################################
# do NOT modify below this line #
#################################

# open a database connection to our local flights database
def connect_database(database_path):
    global conn
    conn = sqlite3.connect(database_path)

def get_all_query_results(debug_print = True):
    all_results = []
    for q, idx in zip([Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10], range(1, 11)):
        result_strings = ("The result for Q%d was:\n%s\n\n" % (idx, from_db_cursor(conn.execute(q)))).splitlines()
        all_results.append(result_strings)
        if debug_print:
            for string in result_strings:
                print string
    return all_results

if __name__ == "__main__":
    connect_database('flights.db')
    query_results = get_all_query_results()
