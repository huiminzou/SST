# -*- coding: utf-8 -*-
"""
Created on Sat Dec 02 20:40:19 2017

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
datetime1=dt.datetime(2017,11,11,0,0,0,0)
datetime2=dt.datetime(2017,11,23,0,0,0,0)
gbox=[-70.7,-69.9,41.4,42.15] 
#MAKE BASEMAP
latsize=[gbox[2],gbox[3]]
lonsize=[gbox[0],gbox[1]]
fig,axes=plt.subplots(1,2,figsize=(15,5))
#url1='http://basin.ceoe.udel.edu/thredds/dodsC/Aqua3DayAggregate.nc' # new address found in Nov 2017
url='http://basin.ceoe.udel.edu/thredds/dodsC/ModisAqua/2017/aqua.2017315.1111.235959.D.L3.modis.NAT.v09.1000m.nc4'
dataset=open_url(url)
times=list(dataset['time'])

#The first plot
m1 = Basemap(projection='cyl',llcrnrlat=min(latsize)-0.01,urcrnrlat=max(latsize)+0.01,\
            llcrnrlon=min(lonsize)-0.01,urcrnrlon=max(lonsize)+0.01,resolution='h')
m1.ax=axes[0]
m1.drawparallels(np.arange(min(latsize),max(latsize)+1,0.1),labels=[1,0,0,0])
m1.drawmeridians(np.arange(min(lonsize),max(lonsize)+1,0.2),labels=[0,0,0,1])
m1.drawcoastlines()
m1.fillcontinents(color='green')
m1.drawmapboundary()

#GET SST & PLOT    
second1=time.mktime(datetime1.timetuple())

# find the nearest image index
index_second1=int(round(np.interp(second1,times,range(len(times)))))
url1='http://basin.ceoe.udel.edu/thredds/dodsC/ModisAqua/2017/aqua.2017315.1111.235959.D.L3.modis.NAT.v09.1000m.nc4?lat[0:1:4499],lon[0:1:4999],'+'sst['+str(index_second1)+':1:'+str(index_second1)+'][0:1:4499][0:1:4999]'+',time['+str(index_second1)+':1:'+str(index_second1)+']'

try:
    print url1
    dataset1=open_url(url1)
except:
    print "please check your url1!"
    sys.exit(0)
    
sst1=dataset1['sst'].sst
lat1=dataset1['lat']
lon1=dataset1['lon']
# find the index for the gbox
index_lon11=int(round(np.interp(gbox[0],list(lon1),range(len(list(lon1))))))
index_lon12=int(round(np.interp(gbox[1],list(lon1),range(len(list(lon1))))))
index_lat11=int(round(np.interp(gbox[2],list(lat1),range(len(list(lat1))))))
index_lat12=int(round(np.interp(gbox[3],list(lat1),range(len(list(lat1))))))
# get part of the sst
sst_part1=sst1[index_second1,index_lat11:index_lat12,index_lon11:index_lon12]
sst_part1[(sst_part1==-999)]=np.NaN # if sst_part=-999, convert to NaN
X1,Y1=np.meshgrid(lon1[index_lon11:index_lon12],lat1[index_lat11:index_lat12])
axes[0].set_title(str(datetime1.strftime("%d-%b-%Y %H:%M")),loc='center')  
a=axes[0].contourf(X1,Y1,sst_part1[0],np.arange(8,14,0.05))
"""
cb=plt.colorbar(a,ax=axes[0])
cb.set_ticks(np.linspace(8,14,7))
cb.set_label('Degree C')
"""

#The second plot
url0='http://basin.ceoe.udel.edu/thredds/dodsC/ModisAqua/2017/aqua.2017327.1123.235959.D.L3.modis.NAT.v09.1000m.nc4'
dataset0=open_url(url0)
times0=list(dataset0['time'])
m2 = Basemap(projection='cyl',llcrnrlat=min(latsize)-0.01,urcrnrlat=max(latsize)+0.01,\
            llcrnrlon=min(lonsize)-0.01,urcrnrlon=max(lonsize)+0.01,resolution='h')
m2.ax=axes[1]
m2.drawparallels(np.arange(min(latsize),max(latsize)+1,0.1),labels=[1,0,0,0])
m2.drawmeridians(np.arange(min(lonsize),max(lonsize)+1,0.2),labels=[0,0,0,1])
m2.drawcoastlines()
m2.fillcontinents(color='green')
m2.drawmapboundary()
#GET SST & PLOT    
second2=time.mktime(datetime2.timetuple())
# find the nearest image index
index_second2=int(round(np.interp(second2,times0,range(len(times0)))))
url2='http://basin.ceoe.udel.edu/thredds/dodsC/ModisAqua/2017/aqua.2017327.1123.235959.D.L3.modis.NAT.v09.1000m.nc4?lat[0:1:4499],lon[0:1:4999],'+'sst['+str(index_second2)+':1:'+str(index_second2)+'][0:1:4499][0:1:4999]'+',time['+str(index_second2)+':1:'+str(index_second2)+']'

try:
    print url2
    dataset2=open_url(url2)
except:
    print "please check your url2!"
    sys.exit(0)
    
sst2=dataset2['sst'].sst
lat2=dataset2['lat']
lon2=dataset2['lon']
# find the index for the gbox
index_lon21=int(round(np.interp(gbox[0],list(lon2),range(len(list(lon2))))))
index_lon22=int(round(np.interp(gbox[1],list(lon2),range(len(list(lon2))))))
index_lat21=int(round(np.interp(gbox[2],list(lat2),range(len(list(lat2))))))
index_lat22=int(round(np.interp(gbox[3],list(lat2),range(len(list(lat2))))))
# get part of the sst
sst_part2=sst2[index_second2,index_lat21:index_lat22,index_lon21:index_lon22]
sst_part2[(sst_part2==-999)]=np.NaN # if sst_part=-999, convert to NaN
X2,Y2=np.meshgrid(lon2[index_lon21:index_lon22],lat2[index_lat21:index_lat22])
axes[1].set_title(str(datetime2.strftime("%d-%b-%Y %H:%M")),loc='center') 
b=axes[1].contourf(X2,Y2,sst_part2[0],np.arange(8,14,0.05))
cb1=plt.colorbar(b,ax=axes[1])
cb1.set_ticks(np.linspace(8,14,7))
cb1.set_label('Degree C')
plt.savefig('11 vs 23 NOV 2017.png')
plt.show()

