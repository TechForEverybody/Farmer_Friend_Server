from .connection import *

realtime_data=mongodb_connection['realtime-data']

iot_modules=realtime_data['iot_modules']
sensors_data=realtime_data['sensors_data']
users=realtime_data['users']
stats=realtime_data['stats']
site_controls=realtime_data['sitecontrols']