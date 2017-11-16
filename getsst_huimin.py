# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 14:02:40 2017

@author: huimin
"""

import sys
import datetime as dt
import matplotlib.pyplot as plt
#sys.path.append("/usr/local/lib/python2.7/dist-packages/Pydap-3.0.1-py2.7.egg")
#from sst_functions_huanxin import  plot_getsst
import pytz
from pydap.client import open_url
import numpy as np
import time
from mpl_toolkits.basemap import Basemap

def getsst(ask_input):
    #get the index of second from the url
    #time_tuple=time.gmtime(second[0])#calculate the year from the seconds
      #change the datetime to seconds
    ask_datetime=ask_input.replace(tzinfo=utc) # making sure the input time is in UTC
    timtzone_ask_datetime=ask_datetime.astimezone(utc) # gets the timezone
    second=time.mktime(timtzone_ask_datetime.timetuple())-17940
    #print second
    time_tuple=time.gmtime(second)#calculate the year from the seconds
    year=time_tuple.tm_year
    print "year="+str(year)
    #print 'Using new RUTGERS server for '+str(year)
    #url1='http://tds.maracoos.org/thredds/dodsC/SST-One-Agg.nc'
    #url1='http://tds.maracoos.org/thredds/dodsC/SST-'+str(year)+'-Agg.nc'
    #url1='http://basin.ceoe.udel.edu/thredds/dodsC/Aqua3DayAggregate.nc' # new address found in Nov 2017
    url1='http://basin.ceoe.udel.edu/thredds/dodsC/AquaClimatology8Day.nc'
    #url1='http://tds.marine.rutgers.edu:8080/thredds/dodsC/cool/avhrr/bigbight/'+str(year)+'?time[0:1:3269]'
    #http://tds.marine.rutgers.edu:8080/thredds/dodsC/cool/avhrr/bigbight/2010?lat[0:1:1221],mcsst[1998:1:1999][0:1:1010][0:1:1100]
    dataset1=open_url(url1)
    times=list(dataset1['time'])
    # find the nearest image index
    index_second=int(round(np.interp(second,times,range(len(times)))))
    #print index_second
    #get sst, time, lat, lon from the url
    #if (year>=1999) and (year<=2011):
    #    url='http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/avhrr/bigbight/'+str(year)+'?lat[0:1:3660],lon[0:1:4499],'+'mcsst['+str(index_second)+':1:'+str(index_second)+'][0:1:3660][0:1:4499]'+',time['+str(index_second)+':1:'+str(index_second)+']'
    #else:
    #url='http://tds.maracoos.org/thredds/dodsC/SST-'+str(year)+'-Agg.nc?lat[0:1:2991],lon[0:1:4499],'+'mcsst['+str(index_second)+':1:'+str(index_second)+'][0:1:2991][0:1:4499]'+',time['+str(index_second)+':1:'+str(index_second)+']'
    #url='http://basin.ceoe.udel.edu/thredds/dodsC/Aqua3DayAggregate.nc?lat[0:1:2991],lon[0:1:4499],'+'sst['+str(index_second)+':1:'+str(index_second)+'][0:1:2991][0:1:4499]'+',time['+str(index_second)+':1:'+str(index_second)+']'
    url='http://basin.ceoe.udel.edu/thredds/dodsC/AquaClimatology8Day.nc?lat[0:1:2991],lon[0:1:4499],'+'sst['+str(index_second)+':1:'+str(index_second)+'][0:1:2991][0:1:4499]'+',time['+str(index_second)+':1:'+str(index_second)+']'    
    #url='http://tds.marine.rutgers.edu:8080/thredds/dodsC/cool/avhrr/bigbight/'+str(year)+'?lat[0:1:1221],lon[0:1:1182],'+'mcsst['+str(index_second)+':1:'+str(index_second)+'][0:1:1221][0:1:1182]'+',time['+str(index_second)+':1:'+str(index_second)+']'
    try:
        print url
        dataset=open_url(url)
    except:
        print "please check your url!"
        sys.exit(0)
    #sst=dataset['mcsst'].mcsst
    sst=dataset['sst'].sst
    time1=dataset['time']
    lat=dataset['lat']
    lon=dataset['lon']
    return sst,time1,lat,lon,index_second

def plot_getsst(ask_input,utc,gbox):
  # where ask_imput is day you want(the format is 2009-08-01 18:34:00)
  # where utc is usually 'utc'
  # where gbox is, for example, [-71, -70.5, 41.25, 41.75]
  
  sst,time1,lat,lon,index_second=getsst(ask_input)

  # find the index for the gbox
  index_lon1=int(round(np.interp(gbox[0],list(lon),range(len(list(lon))))))
  print index_lon1
  index_lon2=int(round(np.interp(gbox[1],list(lon),range(len(list(lon))))))
  print index_lon2
  index_lat1=int(round(np.interp(gbox[2],list(lat),range(len(list(lat))))))
  print index_lat1
  index_lat2=int(round(np.interp(gbox[3],list(lat),range(len(list(lat))))))
  print index_lat2
  # get part of the sst
  
  sst_part=sst[index_second,index_lat1:index_lat2,index_lon1:index_lon2]
  print np.shape(sst_part)

  sst_part[(sst_part==-999)]=np.NaN # if sst_part=-999, convert to NaN
  #sst_part[numpy.isnan(sst_part)]=0 # then change NaN to 0
  X,Y=np.meshgrid(lon[index_lon1:index_lon2],lat[index_lat1:index_lat2])
  
  mi=np.nanmin(sst_part[0])
  ma=np.nanmax(sst_part[0])
  rg=ma-mi
  CS = plt.contourf(X,Y,sst_part[0],np.arange(6,20,2.0))
  

#HARDCODES
utc = pytz.timezone('UTC')
png_num=0 # for saving picture  
#datetime_wanted,url,model_option,lat_max,lon_max,lat_min,lon_min,num,interval_dtime,arrow_percent=getcodar_ctl_file_edge(inputfilename)  #get data from ctl file
#gbox=[lon_min, lon_max, lat_min, lat_max]# , get edge box for sst
datetime_wanted=dt.datetime(2014,11,8,9,11,0,0,pytz.UTC)
#gbox=[-76.0,-60.0,35.0,47.0]  #lon_min, lon_max, lat_min, lat_max
gbox=[-71.0,-69.9,41.5,42.5]     
#MAKE BASEMAP
latsize=[gbox[2],gbox[3]]
lonsize=[gbox[0],gbox[1]]
fig=plt.figure(figsize=(6,8))
ax=fig.add_subplot(211)
m = Basemap(projection='cyl',llcrnrlat=min(latsize)-0.01,urcrnrlat=max(latsize)+0.01,\
            llcrnrlon=min(lonsize)-0.01,urcrnrlon=max(lonsize)+0.01,resolution='h')#,fix_aspect=False)
m.drawparallels(np.arange(int(min(latsize)),int(max(latsize))+1,0.3),labels=[1,0,0,0])
m.drawmeridians(np.arange(int(min(lonsize)),int(max(lonsize))+1,0.2),labels=[0,0,0,1])
m.drawcoastlines()
m.fillcontinents(color='green')
m.drawmapboundary()
ask_input=datetime_wanted

#GET SST & PLOT
plot_getsst(ask_input,utc,gbox)
#pylab.ylim([gbox[2]+0.01,gbox[3]-0.01])
#pylab.xlim([gbox[0]+0.01,gbox[1]-0.01])
bathy=True

#plt.xlim([-70,-69])
#plt.ylim([41,42])
plt.title(str(datetime_wanted.strftime("%d-%b-%Y %H"))+'h')
plt.savefig(dt.datetime.now().strftime('%Y-%m-%d %H:%M')+'.png')
cb=plt.colorbar()
cb.set_label('temp')
plt.show()
