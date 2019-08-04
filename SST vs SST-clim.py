# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 09:26:54 2017

@author: huimin
multi-plots,comparing SST & SST-clim
under the plot of SST is the plot of SST-clim on the same day
the data is raw data
the last url is climatology
"""
import sys
import datetime as dt
import matplotlib.pyplot as plt
from pydap.client import open_url
import numpy as np
import time
from mpl_toolkits.basemap import Basemap

#HARDCODES
temprange=np.arange(7,12,0.05)
colorticks=np.linspace(7,12,6)
time_wanted=[dt.datetime(2017,11,11,23,59,59,0),dt.datetime(2017,11,23,23,59,59,0),dt.datetime(2017,12,1,23,59,59,0)]
url=['http://basin.ceoe.udel.edu/thredds/dodsC/ModisAqua/2017/aqua.2017315.1111.235959.D.L3.modis.NAT.v09.1000m.nc4','http://basin.ceoe.udel.edu/thredds/dodsC/ModisAqua/2017/aqua.2017327.1123.235959.D.L3.modis.NAT.v09.1000m.nc4','http://basin.ceoe.udel.edu/thredds/dodsC/ModisAqua/2017/aqua.2017335.1201.235959.D.L3.modis.NAT.v09.1000m.nc4','http://basin.ceoe.udel.edu/thredds/dodsC/AquaClimatology1Day.nc']
gbox=[-70.7,-69.9,41.7,42.15] 
latsize=[gbox[2],gbox[3]]
lonsize=[gbox[0],gbox[1]]
rows=3
cols=2
fig,axes=plt.subplots(rows,cols,figsize=(10,8))
#axes[1,1].remove()#don't display this axes
for i in range(rows):
    for k in range(cols):
        #DRAW BASEMAP
        m1 = Basemap(projection='cyl',llcrnrlat=min(latsize)-0.01,urcrnrlat=max(latsize)+0.01,\
                llcrnrlon=min(lonsize)-0.01,urcrnrlon=max(lonsize)+0.01,resolution='h')
        m1.ax=axes[i,k]
        if k==0:
            m1.drawparallels(np.arange(min(latsize),max(latsize)+1,0.1),labels=[1,0,0,0])
        else:
            m1.drawparallels(np.arange(min(latsize),max(latsize)+1,0.1),labels=[0,0,0,0])
        if i==rows-1:
            m1.drawmeridians(np.arange(min(lonsize),max(lonsize)+1,0.2),labels=[0,0,0,1])
        else:
            m1.drawmeridians(np.arange(min(lonsize),max(lonsize)+1,0.2),labels=[0,0,0,0])
        m1.drawcoastlines()
        m1.fillcontinents(color='green')
        m1.drawmapboundary()
        #url1='http://basin.ceoe.udel.edu/thredds/dodsC/Aqua3DayAggregate.nc' # new address found in Nov 2017
        
        if k==1:
            index=time_wanted[i].timetuple().tm_yday#convert datetime to a yearday
            url1=url[3]+'?lat[0:1:4499],lon[0:1:4999],'+'sst['+str(index)+':1:'+str(index)+'][0:1:4499][0:1:4999]'+',day['+str(index)+':1:'+str(index)+']'
        else:
            dataset=open_url(url[i])
            times=list(dataset['time'])  
            second=time.mktime(time_wanted[i].timetuple())
            index=int(round(np.interp(second,times,range(len(times)))))
            url1=url[i]+'?lat[0:1:4499],lon[0:1:4999],'+'sst['+str(index)+':1:'+str(index)+'][0:1:4499][0:1:4999]'+',time['+str(index)+':1:'+str(index)+']'
        try:
            print url1
            dataset1=open_url(url1)
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
        if k==1:
            t=axes[i,k].set_title(str(time_wanted[i].strftime("%d-%b"))+'-clim',loc='center')
        else:
            t=axes[i,k].set_title(str(time_wanted[i].strftime("%d-%b-%Y %H:%M")),loc='center')
        a=axes[i,k].contourf(X1,Y1,sst_part[0],temprange)
plt.subplots_adjust(wspace=0.15,hspace=0.02)
#cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
cb=plt.colorbar(a,ax=axes.ravel().tolist())
cb.set_ticks(colorticks)
cb.set_label('Degree C')
plt.savefig('SST vs SST-clim.png')
plt.show() 