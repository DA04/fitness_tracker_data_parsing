# Stacked Histogram with minutes spent on training type from monthly perspective
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
from matplotlib.pyplot import figure

# get session data summary with sport split
conn = psycopg2.connect(host="localhost", database="garmin_data", user="postgres", password="*****")
df = pd.read_sql_query("""select to_char(timestamp, 'YYYY-MM') as stamp, sum(total_timer_time / 60) as minutes_spent, sport 
                        from session
                        group by to_char(timestamp, 'YYYY-MM'), sport
                        having sum(total_timer_time / 60) > 0
                        order by to_char(timestamp, 'YYYY-MM') desc""", conn)

# get min and max dates from the dataframe
min_date = datetime.strptime(min(df.stamp), '%Y-%m')
max_date = datetime.strptime(max(df.stamp), '%Y-%m')
n_max_date = max_date + pd.DateOffset(months=1)

# create a table with all months from min to max date
data = pd.DataFrame()
data['Dates'] = pd.date_range(start=min_date, end=n_max_date, freq='M')
data['Dates'] = data['Dates'].dt.strftime('%Y-%m')

# merge datasets
df_main = pd.merge(data, df, left_on='Dates', right_on='stamp', how='left', indicator=True)
df_main = df_main[['Dates', 'minutes_spent','sport']]
df_main = df_main.fillna(0)

# pivot table
df_pivot = pd.pivot_table(df_main, index='Dates', columns='sport', values='minutes_spent').reset_index()
df_pivot = df_pivot.fillna(0)
df_pivot = df_pivot[['Dates', 'cross_country_skiing', 'cycling', 'running', 'swimming', 'walking']]

# create stacked bar chart for monthly sports
df_pivot.plot(x='Dates', kind='bar', stacked=True, color=['r', 'y', 'g', 'b', 'k'])
 
# labels for x & y axis
plt.xlabel('Months', fontsize=20)
plt.ylabel('Minutes Spent', fontsize=20)
plt.legend(loc='upper left', fontsize=20)

for num in [69, 57, 45, 33, 21, 9]:
    plt.axvline(linewidth=2, x=num, linestyle=':', color = 'grey') 
# title of plot
plt.title('Minutes spent by Sport', fontsize=20)
plt.rcParams['figure.figsize'] = [24, 10]