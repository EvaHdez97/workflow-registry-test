#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 14:41:05 2023

@author: aguerrero
"""
import argparse
import os
import gfs_retrieve as gfs
from dtcv2_util import meteo_utils as mu  

resources_path="resources"
log_folder="log"

def read_arguments():
    global initial_log_folder
    global resources_path
    parser = argparse.ArgumentParser(description="Input data", 
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "-m",
        "--mode",
        default="a",
        help="Actions options: d (only download grib GFS) c (only concatenate and NetCDF conversion)  a (all functions: d+c). DEFAULT: a",
    )  
    parser.add_argument(
        "-i",
        "--input",
        default="examples/meteo.inp",
        help="Actions options: d (only download grib GFS) c (only concatenate and NetCDF conversion)  a (all functions: d+c). DEFAULT: a",
    )       
    args = parser.parse_args()
    mode = args.mode
    input= args.input
    absFilePath = os.path.abspath(__file__)
    

    script_path, filename = os.path.split(absFilePath)
    
    initial_log_folder=os.path.join(script_path,log_folder)
    resources_path=os.path.join(script_path,resources_path)
    if os.path.isfile(input):
        print("here")
        meteo=mu.init_meteo(input,mode,initial_log_folder,"default") 
    
    if mode=="d" or mode=="a":
     gfs.retrieve_gfs(meteo) 
    if mode=="c" or mode=="a": 
     gfs.grib2NC(meteo)
read_arguments()
