#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Thu May  4 11:45:40 2023

@author: aguerrero
'''
import cfgrib
import xarray
import json
from dtcv2_util import log_management as logm 
import os 

location='NC_Functions'
nc_fil="resources/nc_default.json"
import warnings


def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()
def grib2netcdf(meteo):
    global log_file_path
    absFilePath = os.path.abspath(__file__)
    script_path, filename = os.path.split(absFilePath)
    nc_file_path=os.path.join(script_path,nc_fil)
    log_file_path=meteo.log_file
    data_all_levs={}
    data_all_surf={}
    data_all_aboveground={}
    for i in range(meteo.time[0],meteo.time[1]+1,meteo.step):
        local_filename = os.path.join(meteo.path,'{fh:03d}-{basename}'.format(basename = meteo.output,
                                                      fh       = i,
                                                      ))
        try:
            data_plevels0=xarray.open_dataset(local_filename,engine='cfgrib' ,filter_by_keys={'typeOfLevel': 'isobaricInhPa'})
            data_plevels1=xarray.open_dataset(local_filename,engine='cfgrib' ,filter_by_keys={'typeOfLevel': 'isobaricInPa'})
            data_surface=data = xarray.open_dataset(local_filename, engine='cfgrib',filter_by_keys={'typeOfLevel': 'surface','stepType': 'instant'})
            data_2maboveground=xarray.open_dataset(local_filename,engine='cfgrib' ,filter_by_keys={'typeOfLevel': 'heightAboveGround','level':2})
            data_10maboveground=xarray.open_dataset(local_filename,engine='cfgrib' ,filter_by_keys={'typeOfLevel': 'heightAboveGround','level':10})
            
        except Exception:
            try: 
                #If Python3
                data_plevels0=xarray.open_dataset(local_filename,engine='cfgrib' ,backend_kwargs={'filter_by_keys':{'typeOfLevel': 'isobaricInhPa'}})
                data_surface=data = xarray.open_dataset(local_filename, engine='cfgrib',backend_kwargs={'filter_by_keys':{'typeOfLevel': 'surface','stepType': 'instant'}})
                data_plevels1=xarray.open_dataset(local_filename,engine='cfgrib' ,backend_kwargs={'filter_by_keys':{'typeOfLevel': 'isobaricInPa'}})
                data_2maboveground=xarray.open_dataset(local_filename,engine='cfgrib' ,backend_kwargs={'filter_by_keys':{'typeOfLevel': 'heightAboveGround','level':2}})
                data_10maboveground=xarray.open_dataset(local_filename,engine='cfgrib' ,backend_kwargs={'filter_by_keys':{'typeOfLevel': 'heightAboveGround','level':10}})
                
            except Exception as e:
                logm.write_log(log_file_path, str(e), "ERROR", location,"406" )
        try:
            data_plevels1['isobaricInPa']=data_plevels1['isobaricInPa']/100
            data_plevels1=data_plevels1.rename({'isobaricInPa':'isobaricInhPa'})
            data_plevels=xarray.concat([data_plevels0,data_plevels1], dim='isobaricInhPa')
            
            
            data_aboveground=xarray.merge([data_2maboveground,data_10maboveground],compat='override')
            
            if len(data_all_levs)==0 and len(data_all_surf)==0 and len(data_all_aboveground)==0:
                data_all_levs=data_plevels
                data_all_surf=data_surface
                data_all_aboveground=data_aboveground
            else:
                data_all_levs=xarray.concat([data_all_levs,data_plevels],dim='time')
                data_all_surf=xarray.concat([data_all_surf,data_surface],dim='time')
                data_all_aboveground=xarray.concat([data_all_aboveground,data_aboveground],dim='time')
        except Exception as e:
             logm.write_log(log_file_path, str(e), "ERROR", location,"406" )
    try:
         
         data_all_aboveground=rename_GFS_variables(data_all_aboveground,nc_file_path,'heightAboveGround')
         data_all_levs=rename_GFS_variables(data_all_levs,nc_file_path,'isobaricInhPa')
         data_all_surf=rename_GFS_variables(data_all_surf,nc_file_path,'surface')
         data=xarray.merge([data_all_levs,data_all_surf,data_all_aboveground],compat='override')
         data.coords['time']=data.coords['valid_time']
         data=data.drop_vars('valid_time')
         data=data.drop_vars('step')
         data=data.drop_vars('surface')
         data=data.drop_vars('heightAboveGround')
         data_filename=os.path.join(meteo.path,'{base_name}.nc'.format(base_name=meteo.output))
         data.to_netcdf(data_filename)
         if os.path.isfile(data_filename):
             remove_gribs(meteo)
             logm.write_log(log_file_path, "The file is ready in"+data_filename , "SUCCESS", location,"201" )
             logm.write_log(log_file_path, "GFS completed." , "SUCCESS", location,"210" )
    except Exception as e:
        logm.write_log(log_file_path, str(e), "ERROR", location,"406" )

def remove_gribs(meteo):
    try:
        for i in range(meteo.time[0],meteo.time[1]+1,meteo.step):
            local_filename = os.path.join(meteo.path,'{fh:03d}-{basename}'.format(basename = meteo.output,
                                                      fh       = i,
                                                      ))
            os.remove(local_filename)
        for  root, dirs, files in os.walk(meteo.path):
           for currentFile in files:
               exts = ('.idx', '.idx*')
               if currentFile.lower().endswith(exts):
                   os.remove(os.path.join(meteo.path, currentFile))
    except Exception as e:
        logm.write_log(log_file_path, str(e), "ERROR", location,"406" )
        
def read_json(file_path): 
    
    try:
        with open (file_path) as json_file:
            file=json.load(json_file)
            return file
    except Exception as e:
        logm.write_log(log_file_path, 'Json file '+file_path+'  was not found or contains errors. Please check the path' +str(e), 'FATAL-ERROR', location, '500')
        
def rename_GFS_variables(dataset,filedefault,dimension):
    default=read_json(filedefault)
    
    try:
        for i in default['meteo']['GFS2NC'][dimension].keys():
            if i in dataset.keys():
                dataset=dataset.rename({str(i):str(default['meteo']['GFS2NC'][dimension][i]['short_name'])})
        return dataset
    except Exception as e:
        logm.write_log(log_file_path, str(e), "ERROR", location,"406" )
