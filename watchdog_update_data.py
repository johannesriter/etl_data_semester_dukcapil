#!/home/arcgis/miniconda3/bin/python

import arcpy
import csv
import datetime
import logging
import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
from watchdog.observers.polling import PollingObserver

monitor_folder = r'\\otomasi.dukcapil.kemendagri.go.id\otomasi'

class ExampleHandler(FileSystemEventHandler):
    def on_created(self, event): # when file is created
        fullstring =  event.src_path
        substring = '.csv'
        print("Current file: {}".format(fullstring))
        namafile = os.path.basename(fullstring)
        
        if substring in os.path.basename(namafile):
            print('Process data...')
            print('Now processing data {}'.format(fullstring))
            try :
                txt_file = open("current_file.txt", "w")
                txt_file.write(fullstring)
                txt_file.close()
                python_path = r'C:\Users\Administrator\AppData\Local\ESRI\conda\envs\arcgispro-py3-clone\python.exe'
                script_arcgis = r'D:\etl_data_semester_dukcapil\ETL_update_data_semester.py'
                arguments = ('%s %s'%(python_path, script_arcgis))
                os.system(arguments)
                print('Complete, waiting for next data')
            except Exception as e:
                print(e)
                sys.exit(1)

        else:
            print ('it is not the exact data')
            pass
        
        # os.remove(fullstring)
        
logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
path = monitor_folder #(ORIGINAL)
# path = sys.argv[1] if len(sys.argv) > 1 else '.'
observer = PollingObserver() #Observer()
event_handler = ExampleHandler() # create event handler (ORIGINAL)
# event_handler = LoggingEventHandler() # create event handler

# set observer to use created handler in 
print ('Start monitoring folder ...')
observer.schedule(event_handler, path, recursive=True)
observer.start()

# sleep until keyboard interrupt, then stop + rejoin the observer
try:
    while True:
        time.sleep(0.00000001) #(ORIGINAL)
        # time.sleep(5)
except KeyboardInterrupt:
    print ('Shutting down monitoring folder system')
    observer.stop()
observer.join()
