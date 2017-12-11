# -*- coding: utf-8 -*-
"""
Created on Thu Aug 03 20:55:51 2017

@author: xiaojian,huimin
plotting windspeed and SST in one panel

"""

import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import sys
from pydap.client import open_url
import time
from mpl_toolkits.basemap import Basemap
num_of_panels=2
temprange=np.arange(7,13,0.05)
colorticks=np.linspace(7,13,7)
fig,axes=plt.subplots(2,1,figsize=(10,10))
time_wanted=[dt.datetime(2014,11,3,23,59,59,0),dt.datetime(2014,11,19,23,59,59,0)]
gbox=[-70.7,-69.9,41.7,42.15] 
url=['http://basin.ceoe.udel.edu/thredds/dodsC/ModisAqua/2014/aqua.2014307.1103.235959.D.L3.modis.NAT.v09.1000m.nc4','http://basin.ceoe.udel.edu/thredds/dodsC/ModisAqua/2014/aqua.2014323.1119.235959.D.L3.modis.NAT.v09.1000m.nc4']
latsize=[gbox[2],gbox[3]]
lonsize=[gbox[0],gbox[1]]
def sh_bindata(x, y, z, xbins, ybins):
    """
    Bin irregularly spaced data on a rectangular grid.

    """
    ix=np.digitize(x,xbins)
    iy=np.digitize(y,ybins)
    xb=0.5*(xbins[:-1]+xbins[1:]) # bin x centers
    yb=0.5*(ybins[:-1]+ybins[1:]) # bin y centers
    zb_mean=np.empty((len(xbins)-1,len(ybins)-1),dtype=z.dtype)
    zb_median=np.empty((len(xbins)-1,len(ybins)-1),dtype=z.dtype)
    zb_std=np.empty((len(xbins)-1,len(ybins)-1),dtype=z.dtype)
    zb_num=np.zeros((len(xbins)-1,len(ybins)-1),dtype=int)    
    for iix in range(1,len(xbins)):
        for iiy in range(1,len(ybins)):
#            k=np.where((ix==iix) and (iy==iiy)) # wrong syntax
            k,=np.where((ix==iix) & (iy==iiy))
            zb_mean[iix-1,iiy-1]=np.mean(z[k])
            zb_median[iix-1,iiy-1]=np.median(z[k])
            zb_std[iix-1,iiy-1]=np.std(z[k])
            zb_num[iix-1,iiy-1]=len(z[k])
            
    return xb,yb,zb_mean,zb_median,zb_std,zb_num
lon=np.load('lon.npy')
lat=np.load('lat.npy')
num=np.load('numcope.npy')
#FNCL='necscoast_worldvec.dat'
#CL=np.genfromtxt(FNCL,names=['lon','lat'])

x=[]
y=[]
for a in np.arange(len(num)):
    x.append(lon[num[a]])
    y.append(lat[num[a]])
uwind=np.load('uwind_stress20141122.npy')
vwind=np.load('vwind_stress20141122.npy')

u=np.load('u20141122.npy')
v=np.load('v20141122.npy')

xi = np.arange(-70.75,-69.8,0.05)
yi = np.arange(41.5,42.23,0.05)

xb,yb,ub_mean,ub_median,ub_std,ub_num = sh_bindata(np.array(x), np.array(y), np.array(uwind), xi, yi)
xb,yb,vb_mean,vb_median,vb_std,vb_num = sh_bindata(np.array(x), np.array(y), np.array(vwind), xi, yi)

xb1,yb1,ub_mean1,ub_median1,ub_std1,ub_num1 = sh_bindata(np.array(x), np.array(y), np.array(u), xi, yi)
xb1,yb1,vb_mean1,vb_median1,vb_std1,vb_num1 = sh_bindata(np.array(x), np.array(y), np.array(v), xi, yi)
xxb,yyb = np.meshgrid(xb, yb)

ub = np.ma.array(ub_mean, mask=np.isnan(ub_mean))
vb = np.ma.array(vb_mean, mask=np.isnan(vb_mean))
Q=axes[0].quiver(xxb,yyb,ub.T,vb.T,scale=5.)
qk=axes[0].quiverkey(Q,0.9,0.6,0.5, r'$0.1pa$',fontproperties={'weight': 'bold'},zorder=1)

ub1 = np.ma.array(ub_mean1, mask=np.isnan(ub_mean))
vb1 = np.ma.array(vb_mean1, mask=np.isnan(vb_mean))
Q1=axes[1].quiver(xxb,yyb,ub1.T,vb1.T,scale=5.)
qk1=axes[1].quiverkey(Q1,0.9,0.6,0.5, r'$0.1m/s$', fontproperties={'weight': 'bold'},zorder=1)
for i in range(num_of_panels):
    #DRAW BASEMAP
    m1 = Basemap(projection='cyl',llcrnrlat=min(latsize)-0.01,urcrnrlat=max(latsize)+0.01,\
            llcrnrlon=min(lonsize)-0.01,urcrnrlon=max(lonsize)+0.01,resolution='h')
    m1.ax=axes[i]
    m1.drawparallels(np.arange(min(latsize),max(latsize)+1,0.1),labels=[1,0,0,0])
    if i==num_of_panels-1:
        m1.drawmeridians(np.arange(min(lonsize),max(lonsize)+1,0.2),labels=[0,0,0,1])
    else:
        m1.drawmeridians(np.arange(min(lonsize),max(lonsize)+1,0.2),labels=[0,0,0,0])
    m1.drawcoastlines()
    m1.fillcontinents(color='green')
    m1.drawmapboundary()
    #url1='http://basin.ceoe.udel.edu/thredds/dodsC/Aqua3DayAggregate.nc' # new address found in Nov 2017

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
    t=axes[i].set_title(str(time_wanted[i].strftime("%d-%b-%Y %H:%M")),loc='center')
    
    a=axes[i].contourf(X1,Y1,sst_part[0],temprange,zorder=0)

cb=plt.colorbar(a,ax=axes.ravel().tolist())
cb.set_ticks(colorticks)
cb.set_label('Degree C')
plt.savefig('speedwind & SST',dpi=300)
plt.show()