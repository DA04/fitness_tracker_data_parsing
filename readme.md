# FIT files parsing

I have detailed tutorial article published in Russian here https://habr.com/ru/post/658675/

<h2>Changes to parse_fit.py file</h2>

There are few changes from the original [parse_fit.py](/parse_fit.py) file:
1. <b>get_dataframes()</b> function has been extended from Record and Lap dataframes to <i>Record, Lap, Activity, Session, File_ID</i> messages. They are main messages in FIT file according to [Garmin docs](https://developer.garmin.com/fit/file-types/activity/) 
2. <b> get_fit_other_data()</b> function added to extract the data from other FIT frames (<i>file_id, session and activity</i>). It copies the functionality of original <b>get_fit_lap_data()</b> and <b>get_fit_point_data()</b> functions. 
3. Extenstion for the attributes list from the <b>Record</b> message (<i>distance, cadence, power</i> and <i>temperature</i>) added. The <i>Points</i> reference from the original script is replaced with <i>Record</i> to align with established messages names.
4. New function <b>load_dataframe_to_postgres()</b> added in order to load parsed dataframes content to postgres tables.
5. Loop added to go through all the fit files in the directory. The files with the error will be printed out in <b>errors</b> list.

<h2>Postgres Schema</h2>

Postgres Schema for Record, Lap, Activity, Session and File_ID tables can be restored via the [backup file](/garmin_data.sql).
Generated ERD schema can be found here:
![ERD](/garmin_data_full_erd.png)

<h2> Summary chart for the trainings</h2>

I have created a stacked bar chart to check if loaded data is full enough. The python script based on <i>matplotlib</i> is available in [summary_chart.py](/summary_chart.py)
![Summary_chart](/summary_chart.png)