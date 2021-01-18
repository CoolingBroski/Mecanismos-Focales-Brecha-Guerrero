import re
import pandas as pd
import obspy
from pathlib import Path
import os

def read_catalog(catalog):
    f = open(catalog, 'r')
    data = {'date_time' : [], 'lat' : [], 'lon' : [], 'depth' : [], 'mag' : [], 'corr' : [], 'date_time_id' : []}
    stations_meta = []
    for i, line in enumerate(f):
        event = line.split()
        date_str = re.sub(r'\/',r'-', event[1])
        time_str = event[2]
        date_time = date_str+'T'+time_str
        date_timeUTC = obspy.UTCDateTime(date_time)
        data['date_time_id'].append(datetime_to_dotformat(date_timeUTC))
        data['date_time'].append(date_timeUTC)
        data['lat'].append(float(event[3]))
        data['lon'].append(float(event[4]))
        data['depth'].append(float(event[5]))
        data['mag'].append(float(event[6]))
        data['corr'].append(list(map(float, event[7:])))
    return pd.DataFrame(data)

def datetime_to_dotformat(datetime):
    dotformat = str(datetime.year)+'.'+'%02d'%datetime.month+'.'+'%02d'%datetime.day+'.'+'%02d'%datetime.hour+'.'+'%02d'%datetime.minute+'.'+'%02d'%datetime.second
    return dotformat

def get_tr_meta(directorio):
    # Usar con algun directorio de traces
    # Devuelve dataframe de datos de la grabacion y dataframe de relacion entre estacion-canal y grabacion
    # Este sera antecedente de la base de datos
    
    A=obspy.read(directorio+'*')
    traces=[]
    trace_stations=[]
    i=0
    for tr in A:
        dic_tr = {'starttime' : tr.stats.starttime, 'endtime' : tr.stats.endtime, 'sampling_rate' : tr.stats.sampling_rate, 'id' : i}
        traces.append(dic_tr)
        
        dic_tr_st = {'station' : tr.stats.station, 'channel' : tr.stats.channel, 'tr_id' : i}
        trace_stations.append(dic_tr_st)
        
        i+=1
        
    traces_df = pd.DataFrame(traces)
    tr_st_df = pd.DataFrame(trace_stations)
    return traces_df, tr_st_df

def get_meta_data(directorio_completo):
    # Solo usar con el directorio completo
    # Obtiene metadatos de las estaciones
    
    A=obspy.read(directorio_completo+'1S*')
    #B=A.copy()
    stations=[]
    for tr in A:
        #print(tr.stats)
        stations.append(tr.stats.sac)

    raw_df = pd.DataFrame(stations)
    raw_df.to_csv('station.csv')
    return raw_df

def add_vals_to_dic(dic, vals):
    for i, key in enumerate(dic.keys()):
        dic[key].append(vals[i])

def link_ev_st(directorio_recortado):
    # Usar con algun directorio producido por Trim_Org() y dataframes ev de eventos y st de datos de estaciones
    # Devuelve dataframe de datos de la grabacion y dataframe de relacion entre estacion-canal y grabacion
    # Este sera antecedente de la base de datos
    
    traces_df = None
    tr_st_df = None
    dic_ev_st = {'starttime' : [], 'endtime' : [], 'sampling_rate' : [], 'st' : [], 'ch' : [], 'date_time_id' : []}

    for root, dirs, files in os.walk(directorio_recortado):
        if root!=directorio_recortado and root.count('/') == 1:
            A=obspy.read(root+'/1S*')
            for j, tr in enumerate(A):
                vals = [tr.stats.starttime, tr.stats.endtime, tr.stats.sampling_rate, tr.stats.sac['kstnm'], tr.stats.sac['kcmpnm'], root.split('/')[-1]]
                add_vals_to_dic(dic_ev_st, vals)
    ev_st_df = pd.DataFrame(dic_ev_st)
    return ev_st_df

def Trim(directorio_completo, directorio_recortado, t0, tf):
    # t0 y tf son clases obspy.UTCDateTime
    
    A=obspy.read(directorio_completo+'1S*')
    B=A.copy()

    B.trim(starttime=t0, endtime=tf)

    for tr in B:
        #print(tr.stats)
        filename = str(t0.year) + '%02d'%t0.month + '%02d'%t0.day + \
               '%02d'%t0.hour + '%02d'%t0.minute + '%02d'%t0.second +  \
               '.OB.' + tr.stats.sac.kstnm + '.' + tr.stats.sac.kcmpnm + '.sac'
        tr.write(directorio_recortado+filename, format="SAC")
        

def Trim_Org(outdir, directorio_completo, t_interval, event_catalog, stations_meta):
    event_paths = []
    for i, event in event_catalog.iterrows():
        event_path = Path(outdir+'/'+datetime_to_dotformat(event.date_time))
                 
        event_path.mkdir(parents=True, exist_ok=True)
        event_paths.append(event_path)
        
    for i, station_channel in stations_meta.iterrows():
        A=obspy.read(directorio_completo+station_channel.kstnm+'.'+station_channel.kcmpnm)
        for j, event in event_catalog.iterrows():
            event_path = event_paths[j]
            path2 = station_channel.kstnm + '.' + station_channel.kcmpnm
            B=A.copy()
            B.trim(starttime=event.date_time, endtime=event.date_time+t_interval)
            final_path = os.path.join(event_path, path2)
            B[0].write(final_path, format='SAC')