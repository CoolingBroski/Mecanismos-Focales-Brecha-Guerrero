import os
import re
import shutil
import datetime
from pathlib import Path

import pandas as pd

from preprocessing_tools import *

catalog_file = 'catalogSSN.dat'
data = 'Datos/'

catalog = read_catalog(catalog_file)

for i, ev in catalog.iterrows():
    datetime = datetime_to_dotformat(ev.date_time-10)
    ev_path = Path(data+ev.date_time_id)

    ev_path.mkdir(parents=True, exist_ok=True)
    
    for file in os.listdir(data):
        match = re.match(r'^%s\..*'%(''.join(datetime.split('.'))), file)
        if match:
            sta = re.findall(r'IG\.([A-Z]+)\.', file)[0]
            ch = re.findall(r'([A-Z]+)\.sac', file)[0]
            shutil.move(data+file, os.path.join(ev_path,sta+'.'+ch))
            
    