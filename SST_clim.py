# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 19:18:40 2017

@author: huimin

"""
from datetime import *
import sys
from pydap.client import open_url
import numpy as np
import matplotlib.pyplot as plt
import pytz
from mpl_toolkits.basemap import Basemap

def getsst_clim(mth,day,gbox):# where "day_of_year" is month and day (for example, for June 1st, we have "6,1"
    print 'Using new UDELAWARE Climatology server'
    yd=datetime(2017,mth,day,0,0,0).timetuple().tm_yday#convert datetime to a yearday
    #get sst, time, lat, lon from the url
    url='http://basin.ceoe.udel.edu/thredds/dodsC/AquaClimatology1Day.nc?lat[0:1:2991],lon[0:1:4499],'+'sst['+str(yd)+':1:'+str(yd)+'][0:1:2991][0:1:4499]'+',day['+str(yd)+':1:'+str(yd)+']'
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
    sst_part=sst[yd,index_lat1:index_lat2,index_lon1:index_lon2]
    print np.shape(sst_part)

    sst_part[(sst_part==-999)]=np.NaN # if sst_part=-999, convert to NaN
    X,Y=np.meshgrid(lon[index_lon1:index_lon2],lat[index_lat1:index_lat2])
    plt.contourf(X,Y,sst_part[0],np.arange(6,24,0.25))
    cb=plt.colorbar()
    cb.set_ticks(np.linspace(6,24,10))
    cb.set_label('temp')
#HARDCODES
utc = pytz.timezone('UTC') 
mth=6
day=25
gbox=[-71.0,-69.9,41.5,42.5]     
#MAKE BASEMAP
latsize=[gbox[2],gbox[3]]
lonsize=[gbox[0],gbox[1]]
#fig,axes=plt.subplots(1,1,figsize=(6,8))
m = Basemap(projection='cyl',llcrnrlat=min(latsize)-0.01,urcrnrlat=max(latsize)+0.01,\
            llcrnrlon=min(lonsize)-0.01,urcrnrlon=max(lonsize)+0.01,resolution='h')#,fix_aspect=False)
m.drawparallels(np.arange(int(min(latsize)),int(max(latsize))+1,0.3),labels=[1,0,0,0])
m.drawmeridians(np.arange(int(min(lonsize)),int(max(lonsize))+1,0.2),labels=[0,0,0,1])
m.drawcoastlines()
m.fillcontinents(color='green')
m.drawmapboundary()
#GET SST & PLOT
getsst_clim(mth,day,gbox)

plt.title("SST_clim-"+repr(mth)+"-"+repr(day))
plt.savefig("SST_clim-"+repr(mth)+"-"+repr(day)+'.png')
plt.show()
