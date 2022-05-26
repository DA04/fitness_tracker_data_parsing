"""Some functions for parsing a FIT files mandatory tables (activity, file_id, session, lap and record)
and creating a Pandas DataFrame with the data, bulk upload for dataframes to PostgreSQL DB
"""

from datetime import datetime, timedelta
from typing import Dict, Union, Optional,Tuple
import os

import pandas as pd
import psycopg2

import fitdecode

# The path to the folder with all FIT files to be processed
dir = r'*****'

# Connection details for Postgresql DB
conn = psycopg2.connect(host="localhost", database="garmin_data", user="postgres", password="*****")

# The names of the columns we will use in our points DataFrame. For the data we will be getting
# from the FIT data, we use the same name as the field names to make it easier to parse the data.
record = ['latitude', 'longitude', 'lap', 'altitude', 'timestamp', 'heart_rate', 'cadence', 'speed', 'distance', 'power', 'temperature']

# The names of the columns we will use in our laps DataFrame. 
lap = ['number', 'start_time', 'total_distance', 'total_elapsed_time', 'max_speed', 'max_heart_rate', 'avg_heart_rate']

# The names of the columns in file_id DataFrame
file_id = ['serial_number', 'tine_created', 'manufacturer', 'product', 'number', 'type']

# The names of the columns in activity DataFrame
activity = ['timestamp', 'total_timer_time', 'local_timestamp', 'num_sessions', 'type', 'event', 'event_type', 'event_group']

# The names of the columns in session DataFrame
session = ['timestamp', 'start_time', 'start_position_lat', 'start_position_long', 'total_elapsed_time', 'total_timer_time', 'total_distance',
'total_strokes', 'nec_lat', 'nec_long', 'swc_lat', 'swc_long', 'message_index', 'total_calories', 'total_fat_calories', 'enhanced_avg_speed',
'avg_speed', 'enhanced_max_speed', 'max_speed', 'avg_power', 'max_power', 'total_ascent', 'total_descent', 'first_lap_index',
'num_laps', 'event', 'event_type', 'sport', 'sub_sport', 'avg_heart_rate', 'max_heart_rate', 'avg_cadence', 'max_cadence', 'total_training_effect',
'event_group', 'trigger']


def get_user_activity_details(file):
    """Extract user_id and activity_id from the FIT file name
    in order to get unique instance for the activity
    """
    filename = os.path.basename(file)
    user_id, activity_id = filename.split('_')[0], filename.split('_')[1]
    if '.' in activity_id:
        activity_id = activity_id.split('.')[0]
    
    return user_id, activity_id

def load_dataframe_to_postgres(df, tabl):
    """Takes a dataframe and it's source FIT file type,
    if dataframe is not empty then it is filled up with 0 for NaN values,
    dataframe is checked against the general schema per FIT file type - proper data types are assigned to the columns,
    through the iterations rows are sent to postgres DB with the use of INSERT INTO statement
    """
    if not df.empty:
        df = df.fillna(0)
        cursor = conn.cursor()
        if tabl == 'activity':
            df = df.astype({'activity_id': 'int64','timestamp': 'datetime64[ns, UTC]', 'total_timer_time': 'float64', 'local_timestamp': 'datetime64[ns]', 'num_sessions': 'int64', 'type': 'object', 'event': 'object', 'event_type': 'object', 'event_group': 'object'})
            for index, row in df.iterrows():
                cursor.execute("""insert into activity(activity_id, timestamp, total_timer_time, local_timestamp, num_sessions, type, event, event_type, event_group)
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", [row.activity_id, row.timestamp, row.total_timer_time, row.local_timestamp, row.num_sessions, row.type, row.event, row.event_type, row.event_group])
        elif tabl == 'file_id':
            df.rename(columns = {'product': 'product_name'}, inplace=True)
            df = df.astype({'activity_id': 'int64', 'serial_number': 'int64', 'tine_created': 'float64', 'manufacturer': 'object', 'product_name': 'object', 'number' : 'float64', 'type': 'object'})
            for index, row in df.iterrows():
                cursor.execute("""insert into file_id(activity_id, serial_number, tine_created, manufacturer, product, number, type)
                values (%s, %s, %s, %s, %s, %s, %s)""", [row.activity_id, row.serial_number, row.tine_created, row.manufacturer, row.product_name, row.number, row.type])
        elif tabl == 'lap':
            df = df.astype({'activity_id': 'int64', 'number': 'int64', 'start_time': 'datetime64[ns, UTC]', 'total_distance': 'float64', 'total_elapsed_time': 'float64', 'max_speed': 'float64', 'max_heart_rate': 'int64', 'avg_heart_rate': 'int64'})
            for index, row in df.iterrows():
                cursor.execute("""insert into lap(activity_id, number, start_time, total_distance, total_elapsed_time, max_speed, max_heart_rate, avg_heart_rate)
                values (%s, %s, %s, %s, %s, %s, %s, %s)""", [row.activity_id, row.number, row.start_time, row.total_distance, row.total_elapsed_time, row.max_speed, row.max_heart_rate, row.avg_heart_rate])
        elif tabl == 'record':
            df = df.astype({'activity_id': 'int64', 'latitude': 'float64', 'longitude' : 'float64', 'lap': 'int64', 'altitude': 'float64',\
                            'timestamp': 'datetime64[ns, UTC]', 'heart_rate': 'int64', 'cadence': 'int64', 'speed': 'int64', \
                            'distance': 'float64', 'power': 'int64', 'temperature': 'int64'})
            for index, row in df.iterrows():
                cursor.execute("""insert into record(activity_id, latitude, longitude, lap, altitude, timestamp, heart_rate, cadence, speed, distance, power, temperature)
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", [row.activity_id, row.latitude, row.longitude, row.lap, row.altitude, row.timestamp, row.heart_rate, row.cadence, row.speed, row.distance, row.power, row.temperature])
        elif tabl == 'session':
            df = df.astype({'activity_id': 'int64', 'timestamp': 'datetime64[ns, UTC]', 'start_time': 'datetime64[ns, UTC]', 'start_position_lat': 'int64', 'start_position_long': 'int64', 'total_elapsed_time':'float64', \
                            'total_timer_time': 'float64', 'total_distance': 'float64', 'total_strokes': 'float64', 'nec_lat': 'int64', 'nec_long': 'int64', 'swc_lat': 'int64', \
                            'swc_long': 'int64', 'message_index': 'int64', 'total_calories': 'int64', 'total_fat_calories': 'float64', 'enhanced_avg_speed': 'float64',\
                            'avg_speed': 'float64', 'enhanced_max_speed': 'float64', 'max_speed': 'float64', 'avg_power': 'float64', 'max_power':'float64', 'total_ascent': 'int64', \
                            'total_descent': 'int64', 'first_lap_index': 'int64', 'num_laps': 'int64', 'event': 'object', 'event_type': 'object', 'sport': 'object', 'sub_sport': 'object', \
                            'avg_heart_rate': 'int64', 'max_heart_rate': 'int64', 'avg_cadence': 'int64', 'max_cadence': 'int64', 'total_training_effect': 'float64', \
                            'event_group': 'float64', 'trigger': 'object'})
            for index, row in df.iterrows():
                cursor.execute("""insert into session(activity_id, timestamp, start_time, start_position_lat, 
                start_position_long, total_elapsed_time, total_timer_time, total_distance, total_strokes, nec_lat, 
                nec_long, swc_lat, swc_long, message_index, total_calories, total_fat_calories, enhanced_avg_speed,
                avg_speed, enhanced_max_speed, max_speed, avg_power, max_power, total_ascent, total_descent, first_lap_index,
                num_laps, event, event_type, sport, sub_sport, avg_heart_rate, max_heart_rate, avg_cadence, max_cadence, 
                total_training_effect, event_group, trigger) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",\
                [row.activity_id, row.timestamp, row.start_time, row.start_position_lat, row.start_position_long, \
                 row.total_elapsed_time, row.total_timer_time, row.total_distance, row.total_strokes, row.nec_lat, \
                 row.nec_long, row.swc_lat, row.swc_long, row.message_index, row.total_calories, row.total_fat_calories, \
                 row.enhanced_avg_speed, row.avg_speed, row.enhanced_max_speed, row.max_speed, row.avg_power, \
                 row.max_power, row.total_ascent, row.total_descent, row.first_lap_index, row.num_laps, row.event, \
                 row.event_type, row.sport, row.sub_sport, row.avg_heart_rate, row.max_heart_rate, row.avg_cadence, \
                 row.max_cadence, row.total_training_effect, row.event_group, row.trigger])
        conn.commit()
        cursor.close()

def get_fit_lap_data(frame: fitdecode.records.FitDataMessage) -> Dict[str, Union[float, datetime, timedelta, int]]:
    """Extract some data from a FIT frame representing a lap and return
    it as a dict.
    """
    
    data: Dict[str, Union[float, datetime, timedelta, int]] = {}
    
    for field in lap[1:]:  # Exclude 'number' (lap number) because we don't get that
                                        # from the data but rather count it ourselves
        if frame.has_field(field):
            data[field] = frame.get_value(field)
    
    return data

def get_fit_point_data(frame: fitdecode.records.FitDataMessage) -> Optional[Dict[str, Union[float, int, str, datetime]]]:
    """Extract some data from an FIT frame representing a track point
    and return it as a dict.
    """
    
    data: Dict[str, Union[float, int, str, datetime]] = {}
    
    if not (frame.has_field('position_lat') and frame.has_field('position_long')):
        # Frame does not have any latitude or longitude data. We will ignore these frames in order to keep things
        # simple, as we did when parsing the TCX file.
        return None
    else:
        data['latitude'] = frame.get_value('position_lat') / ((2**32) / 360)
        data['longitude'] = frame.get_value('position_long') / ((2**32) / 360)
    
    for field in record[3:]:
        if frame.has_field(field):
            data[field] = frame.get_value(field)
    
    return data

def get_fit_other_data(col, frame: fitdecode.records.FitDataMessage) -> Optional[Dict[str, Union[float, int, str, datetime]]]:
    """Extract the data point from other FIT frames(file_id, session, activity)
    with the use of column names and return a relevant Pandas DataFrame
    """
    
    data: Dict[str, Union[float, int, str, datetime]] = {}
       
    for field in col:
        if frame.has_field(field):
            data[field] = frame.get_value(field)
    return data


def get_dataframes(fname: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Takes the path to a FIT file (as a string) and returns two Pandas
    DataFrames: one containing data about the laps, and one containing
    data about the individual points.
    """

    record_data = []
    lap_data = []
    lap_no = 1
    file_id_data = []
    activity_data = []
    session_data = []
    
    with fitdecode.FitReader(fname) as fit_file:
        for frame in fit_file:
            if isinstance(frame, fitdecode.records.FitDataMessage):
                if frame.name == 'record':
                    single_point_data = get_fit_point_data(frame)
                    if single_point_data is not None:
                        single_point_data['lap'] = lap_no
                        record_data.append(single_point_data)
                elif frame.name == 'lap':
                    single_lap_data = get_fit_lap_data(frame)
                    single_lap_data['number'] = lap_no
                    lap_data.append(single_lap_data)
                    lap_no += 1
                elif frame.name == 'file_id':
                    file_id_data.append(get_fit_other_data(file_id, frame))
                elif frame.name == 'activity':
                    activity_data.append(get_fit_other_data(activity, frame))
                elif frame.name == 'session':
                    session_data.append(get_fit_other_data(session, frame))
    
    # Create DataFrames from the data we have collected. If any information is missing from a particular lap or track
    # point, it will show up as a null value or "NaN" in the DataFrame.
    
    lap_df = pd.DataFrame(lap_data, columns=lap)
#     lap_df.set_index('number', inplace=True)
    record_df = pd.DataFrame(record_data, columns=record)
    file_id_df = pd.DataFrame(file_id_data, columns = file_id)
    activity_df = pd.DataFrame(activity_data, columns = activity)
    session_df = pd.DataFrame(session_data, columns = session)
    
    for df in (lap_df, record_df, file_id_df, activity_df, session_df):
        df['activity_id'] = activity_id
    if activity_df.empty:
        activity_df = activity_df.append({'activity_id':activity_id}, ignore_index=True)
      
    return lap_df, record_df, file_id_df, activity_df, session_df

if __name__ == '__main__':
    
    from sys import argv
    import random
    from os import listdir
    from os.path import isfile, join
    
    files = [f for f in listdir(dir) if isfile(join(dir, f))]
    errors = []
    for file in files:
        try:
            fname = dir+"\\"+file
            user_id, activity_id = get_user_activity_details(fname)
            lap_df, record_df, file_id_df, activity_df, session_df = get_dataframes(fname)
            print('user_activity:', user_id, activity_id)
            # load to DB
                load_dataframe_to_postgres(activity_df, 'activity')
                load_dataframe_to_postgres(file_id_df, 'file_id')
                load_dataframe_to_postgres(lap_df, 'lap')
                load_dataframe_to_postgres(record_df, 'record')
                load_dataframe_to_postgres(session_df, 'session')
        except:
            errors.append(activity_id)
    print('finished')
    print('errors')
    print(errors)