# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 14:02:40 2017

@author: huimin
"""

import sys
import datetime as dt
import matplotlib.pyplot as plt
import pytz
from pydap.client import open_url
import numpy as np
import time
from mpl_toolkits.basemap import Basemap

def getsst(ask_input,gbox):
    #get the index of second from the url
    #time_tuple=time.gmtime(second[0])#calculate the year from the seconds
      #change the datetime to seconds
    ask_datetime=ask_input.replace(tzinfo=utc) # making sure the input time is in UTC
    timtzone_ask_datetime=ask_datetime.astimezone(utc) # gets the timezone
    second=time.mktime(timtzone_ask_datetime.timetuple())-17940
    #url1='http://basin.ceoe.udel.edu/thredds/dodsC/Aqua3DayAggregate.nc' # new address found in Nov 2017
    url1='http://basin.ceoe.udel.edu/thredds/dodsC/Aqua1DayAggregate.nc'
    dataset1=open_url(url1)
    times=list(dataset1['time'])
    # find the nearest image index
    index_second=int(round(np.interp(second,times,range(len(times)))))
    url='http://basin.ceoe.udel.edu/thredds/dodsC/Aqua1DayAggregate.nc?lat[0:1:4499],lon[0:1:4999],'+'sst['+str(index_second)+':1:'+str(index_second)+'][0:1:4499][0:1:4999]'+',time['+str(index_second)+':1:'+str(index_second)+']'
    
    try:
        print url
        dataset=open_url(url)
    except:
        print "please check your url!"
        sys.exit(0)
    #sst=dataset['mcsst'].mcsst
    sst=dataset['sst'].sst
    lat=dataset['lat']
    lon=dataset['lon']
     # find the index for the gbox
    index_lon1=int(round(np.interp(gbox[0],list(lon),range(len(list(lon))))))
    index_lon2=int(round(np.interp(gbox[1],list(lon),range(len(list(lon))))))
    index_lat1=int(round(np.interp(gbox[2],list(lat),range(len(list(lat))))))
    index_lat2=int(round(np.interp(gbox[3],list(lat),range(len(list(lat))))))
    # get part of the sst
    sst_part=sst[index_second,index_lat1:index_lat2,index_lon1:index_lon2]
    sst_part[(sst_part==-999)]=np.NaN # if sst_part=-999, convert to NaN
    X,Y=np.meshgrid(lon[index_lon1:index_lon2],lat[index_lat1:index_lat2])
  
    plt.contourf(X,Y,sst_part[0],np.arange(8,14,0.05))
    cb=plt.colorbar()
    cb.set_ticks(np.linspace(8,14,7))
    cb.set_label('Degree C')
#HARDCODES
utc = pytz.timezone('UTC')
datetime_wanted=dt.datetime(2017,11,23,0,0,0,0,pytz.UTC)
gbox=[-71.0,-69.9,41.4,42.15]     
#MAKE BASEMAP
latsize=[gbox[2],gbox[3]]
lonsize=[gbox[0],gbox[1]]
fig=plt.figure()
m = Basemap(projection='cyl',llcrnrlat=min(latsize)-0.01,urcrnrlat=max(latsize)+0.01,\
            llcrnrlon=min(lonsize)-0.01,urcrnrlon=max(lonsize)+0.01,resolution='h')#,fix_aspect=False)
m.drawparallels(np.arange(int(min(latsize)),int(max(latsize))+1,0.1),labels=[1,0,0,0])
m.drawmeridians(np.arange(int(min(lonsize)),int(max(lonsize))+1,0.2),labels=[0,0,0,1])
m.drawcoastlines()
m.fillcontinents(color='green')
m.drawmapboundary()
ask_input=datetime_wanted
#GET SST & PLOT
getsst(ask_input,gbox)

plt.title(str(datetime_wanted.strftime("%d-%b-%Y %H:%M")))
plt.savefig(datetime_wanted.strftime('%Y-%m-%d %H:%M')+'.png')
plt.show()
