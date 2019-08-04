# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 14:39:38 2017

@author: huimin
create two plots of SST at 11 vs 23 NOV 2017
"""
import sys
import datetime as dt
import matplotlib.pyplot as plt
from pydap.client import open_url
import numpy as np
import time
from mpl_toolkits.basemap import Basemap

#HARDCODES
num_of_panels=2
datetime=[dt.datetime(2017,11,11,23,59,59,0),dt.datetime(2017,11,23,23,59,59,0)]
gbox=[-70.7,-69.9,41.7,42.15] 
latsize=[gbox[2],gbox[3]]
lonsize=[gbox[0],gbox[1]]
fig,axes=plt.subplots(1,2,figsize=(25,5))

for i in range(num_of_panels):
    #url1='http://basin.ceoe.udel.edu/thredds/dodsC/Aqua3DayAggregate.nc' # new address found in Nov 2017
    #url='http://basin.ceoe.udel.edu/thredds/dodsC/ModisAqua/2017/aqua.2017315.1111.235959.D.L3.modis.NAT.v09.1000m.nc4'
    url=['http://basin.ceoe.udel.edu/thredds/dodsC/ModisAqua/2017/aqua.2017315.1111.235959.D.L3.modis.NAT.v09.1000m.nc4','http://basin.ceoe.udel.edu/thredds/dodsC/ModisAqua/2017/aqua.2017327.1123.235959.D.L3.modis.NAT.v09.1000m.nc4']
    dataset=open_url(url[i])
    times=list(dataset['time'])
    #The first plot
    m1 = Basemap(projection='cyl',llcrnrlat=min(latsize)-0.01,urcrnrlat=max(latsize)+0.01,\
            llcrnrlon=min(lonsize)-0.01,urcrnrlon=max(lonsize)+0.01,resolution='h')
    m1.ax=axes[i]
    m1.drawparallels(np.arange(min(latsize),max(latsize)+1,0.1),labels=[1,0,0,0])
    m1.drawmeridians(np.arange(min(lonsize),max(lonsize)+1,0.2),labels=[0,0,0,1])
    m1.drawcoastlines()
    m1.fillcontinents(color='green')
    m1.drawmapboundary()
    #GET SST & PLOT    
    second=time.mktime(datetime[i].timetuple())

    # find the nearest image index
    index_second=int(round(np.interp(second,times,range(len(times)))))
    url=url[i]+'?lat[0:1:4499],lon[0:1:4999],'+'sst['+str(index_second)+':1:'+str(index_second)+'][0:1:4499][0:1:4999]'+',time['+str(index_second)+':1:'+str(index_second)+']'
    
    try:
        print url
        dataset1=open_url(url)
    except:
        print "please check your url!"
        sys.exit(0)   
    sst=dataset1['sst'].sst
    lat=dataset1['lat']
    lon=dataset1['lon']
    # find the index for the gbox
    index_lon11=int(round(np.interp(gbox[0],list(lon),range(len(list(lon))))))
    index_lon12=int(round(np.interp(gbox[1],list(lon),range(len(list(lon))))))
    index_lat11=int(round(np.interp(gbox[2],list(lat),range(len(list(lat))))))
    index_lat12=int(round(np.interp(gbox[3],list(lat),range(len(list(lat))))))
    # get part of the sst
    sst_part=sst[index_second,index_lat11:index_lat12,index_lon11:index_lon12]
    sst_part[(sst_part==-999)]=np.NaN # if sst_part=-999, convert to NaN
    X1,Y1=np.meshgrid(lon[index_lon11:index_lon12],lat[index_lat11:index_lat12])
    axes[i].set_title(str(datetime[i].strftime("%d-%b-%Y %H:%M")),loc='center')  
    a=axes[i].contourf(X1,Y1,sst_part[0],np.arange(7,12,0.05))
cb=plt.colorbar(a,ax=axes[1])
cb.set_ticks(np.linspace(7,12,6))
cb.set_label('Degree C')
plt.savefig('11 vs 23 NOV 2017new.png')
plt.show()   
