# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 14:02:40 2017

@author: huimin
"""

import sys
import datetime as dt
import matplotlib.pyplot as plt
from pydap.client import open_url
import numpy as np
import time
from mpl_toolkits.basemap import Basemap

#HARDCODES
datetime_wanted=dt.datetime(2017,11,18,8,0,0,0)
gbox=[-70.7,-69.9,41.4,42.15] 

def getsst(datetime_wanted,gbox):
    
    second=time.mktime(datetime_wanted.timetuple())
    #url1='http://basin.ceoe.udel.edu/thredds/dodsC/Aqua3DayAggregate.nc' # new address found in Nov 2017
    url1='http://basin.ceoe.udel.edu/thredds/dodsC/Aqua8DayAggregate.nc'
    dataset1=open_url(url1)
    times=list(dataset1['time'])
    # find the nearest image index
    index_second=int(round(np.interp(second,times,range(len(times)))))
    url='http://basin.ceoe.udel.edu/thredds/dodsC/Aqua8DayAggregate.nc?lat[0:1:4499],lon[0:1:4999],'+'sst['+str(index_second)+':1:'+str(index_second)+'][0:1:4499][0:1:4999]'+',time['+str(index_second)+':1:'+str(index_second)+']'
    
    try:
        print url
        dataset=open_url(url)
    except:
        print "please check your url!"
        sys.exit(0)
    
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
#MAKE BASEMAP
latsize=[gbox[2],gbox[3]]
lonsize=[gbox[0],gbox[1]]
fig=plt.figure()
m = Basemap(projection='cyl',llcrnrlat=min(latsize)-0.01,urcrnrlat=max(latsize)+0.01,\
            llcrnrlon=min(lonsize)-0.01,urcrnrlon=max(lonsize)+0.01,resolution='h')
m.drawparallels(np.arange(min(latsize),max(latsize)+1,0.1),labels=[1,0,0,0])
m.drawmeridians(np.arange(min(lonsize),max(lonsize)+1,0.2),labels=[0,0,0,1])
m.drawcoastlines()
m.fillcontinents(color='green')
m.drawmapboundary()
#GET SST & PLOT
getsst(datetime_wanted,gbox)

plt.title(str(datetime_wanted.strftime("%d-%b-%Y %H:%M")))
plt.savefig(datetime_wanted.strftime('%Y-%m-%d %H:%M')+'8.png')
plt.show()
