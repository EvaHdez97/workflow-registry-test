#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 16:13:40 2023

@author: aguerrero
"""


from grib_filter import GFS
from dtcv2_util import log_management as logf #this has to be called from library
import os
import nc_functions as nc2
import datetime


def check_files(meteo):
    flag_files=True
    for i in range(meteo.time[0],meteo.time[1]+1,meteo.step):

        local_filename = os.path.join(meteo.path,"{fh:03d}-{basename}".format(basename = meteo.output,
                                                      fh       = i))
        if not os.path.isfile(local_filename):
            flag_files=False
    return flag_files
def previous_cicle(meteo):
    if meteo.cycle==0:
        meteo.date=meteo.date-datetime.timedelta(days=1)
        meteo.cycle=18
    else:
        meteo.cycle=meteo.cycle-6
    strt=""
    for x in range(len(meteo.time)-1):
        strt+=" "+str(meteo.time[x-1]+6)
        meteo.time[x-1]= meteo.time[x-1]+6
    return meteo,strt

def check_download(meteo,request,identifier):
    flag_st=0
    if request.status>=200 and request.status<300:
      flag_f=check_files(meteo) 
      if flag_f:
          logf.write_log(meteo.log_file, "Download completed. The Meteo GFS files are ready in folder "+ str(meteo.path), "SUCESS", identifier, "201")
          
      else:
         logf.write_log(meteo.log_file, "ERROR. One or more files required are not in the Meteo folder", "ERROR", identifier, "406")
         flag_st=1
    else:
        #In case that the data is not available for the cycle yet, the preceeding cycle will be taken by adding 6 hours to the download  
        if request.status>=400 and request.status<500:
            if request.status==403:
                logf.write_log(meteo.log_file, "ERROR. The information to be downloaded can not be available. Please check date and cycle. Date: "+str(meteo.date)+" Cycle: "+str(meteo.cycle), "ERROR", identifier, "404")
                flag_st=1
            else:
               [meteo,strt]=previous_cicle(meteo)
               flag_st=2 
               logf.write_log(meteo.log_file, "WARNING. Trying to get the preceeding cycle data... Downloading information. Day: "+str(meteo.date)+" Cycle: "+str(meteo.cycle)+ " Time: "+strt, "WARNING", identifier, "301")    
    return flag_st,meteo
def grib2NC(meteo):
    #Check if all files are in the path  
    nc2.grib2netcdf(meteo)
def retrieve_gfs(meteo):
    request = GFS(meteo)
    request.save_data()
    identifier="Download validation"
    [flag_st,meteo]=check_download(meteo, request, identifier)
    if flag_st==2:
            request = GFS(meteo)
            request.save_data()
            [flag_st1,meteo1]=check_download(meteo, request, identifier) 
            if flag_st1==1 or flag_st1==2:
                logf.write_log(meteo.log_file, "ERROR. The information to be downloaded can not be available. Please check date and cycle. Date: "+str(meteo.date)+" Cycle: "+str(meteo.cycle), "FATAL-ERROR", identifier, "405")
    
        