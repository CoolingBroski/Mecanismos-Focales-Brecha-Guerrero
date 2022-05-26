import os
import re

response_dir = 'Respuesta_Instrumento/'
station_file = 'station_list.txt'

with open(station_file, 'w+') as f:
    for file in os.listdir(response_dir):
        match = re.match(r'.*_21001231\.RESP', file)
        if match:
            station = re.search(r'^([A-Z]+)', file).group()
            f.write(station+'\n')