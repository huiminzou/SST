# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 11:07:58 2017

@author: huimin
create  plots of SST at 11 vs 23 NOV 2017 & “climatology” of the average day
"""
import sys
import datetime as dt
import matplotlib.pyplot as plt
from pydap.client import open_url
import numpy as np
import time
from mpl_toolkits.basemap import Basemap

#HARDCODES
num_of_panels=3
mth=11
day=16
temprange=np.arange(7,12,0.05)
colorticks=np.linspace(7,12,6)
datetime=[dt.datetime(2017,11,11,23,59,59,0),dt.datetime(2017,11,23,23,59,59,0),dt.datetime(2017,mth,day,0,0,0)]
gbox=[-70.7,-69.9,41.7,42.15] 
latsize=[gbox[2],gbox[3]]
lonsize=[gbox[0],gbox[1]]
fig,axes=plt.subplots(2,2,figsize=(15,8))
axes[1,1].remove()#don't display this axes
#fig=plt.figure()
#ax1=fig.add_subplots(2,2,1)
#ax2=fig.add_subplots(2,2,2)
#ax3=fig.add_subplots(2,2,3)
for i in range(num_of_panels):
    if i==0:
        m=0;k=0
    elif i==1:
        m=0;k=1
    else:
        m=1;k=0
    #DRAW BASEMAP
    m1 = Basemap(projection='cyl',llcrnrlat=min(latsize)-0.01,urcrnrlat=max(latsize)+0.01,\
            llcrnrlon=min(lonsize)-0.01,urcrnrlon=max(lonsize)+0.01,resolution='h')
    m1.ax=axes[m,k]
    m1.drawparallels(np.arange(min(latsize),max(latsize)+1,0.1),labels=[1,0,0,0])
    m1.drawmeridians(np.arange(min(lonsize),max(lonsize)+1,0.2),labels=[0,0,0,1])
    m1.drawcoastlines()
    m1.fillcontinents(color='green')
    m1.drawmapboundary()
    #url1='http://basin.ceoe.udel.edu/thredds/dodsC/Aqua3DayAggregate.nc' # new address found in Nov 2017
    url=['http://basin.ceoe.udel.edu/thredds/dodsC/ModisAqua/2017/aqua.2017315.1111.235959.D.L3.modis.NAT.v09.1000m.nc4','http://basin.ceoe.udel.edu/thredds/dodsC/ModisAqua/2017/aqua.2017327.1123.235959.D.L3.modis.NAT.v09.1000m.nc4','http://basin.ceoe.udel.edu/thredds/dodsC/AquaClimatology1Day.nc']
    if i==2:
        index=datetime[i].timetuple().tm_yday#convert datetime to a yearday
        url=url[i]+'?lat[0:1:4499],lon[0:1:4999],'+'sst['+str(index)+':1:'+str(index)+'][0:1:4499][0:1:4999]'+',day['+str(index)+':1:'+str(index)+']'
    else:
        dataset=open_url(url[i])
        times=list(dataset['time'])  
        second=time.mktime(datetime[i].timetuple())
        index=int(round(np.interp(second,times,range(len(times)))))
        url=url[i]+'?lat[0:1:4499],lon[0:1:4999],'+'sst['+str(index)+':1:'+str(index)+'][0:1:4499][0:1:4999]'+',time['+str(index)+':1:'+str(index)+']'
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
    sst_part=sst[index,index_lat11:index_lat12,index_lon11:index_lon12]
    sst_part[(sst_part==-999)]=np.NaN # if sst_part=-999, convert to NaN
    X1,Y1=np.meshgrid(lon[index_lon11:index_lon12],lat[index_lat11:index_lat12])
    axes[m,k].set_title(str(datetime[i].strftime("%d-%b-%Y %H:%M")),loc='center')  
    a=axes[m,k].contourf(X1,Y1,sst_part[0],temprange)
cb=plt.colorbar(a,ax=axes[1,0])
cb.set_ticks(colorticks)
cb.set_label('Degree C')
plt.savefig('11 vs 23 NOV 2017&clim.png')
plt.show()   
