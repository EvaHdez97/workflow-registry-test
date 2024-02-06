## Purpose
This script is designed to download and process meteorological data, specifically from the GFS (Global Forecast System) model.

## Functions



- Initiates a request to download GFS data
- Checks if the required GFS files are present in the specified folder.
- If necessary, attempts to download data from the previous cycle.
- Adjusts the date and cycle for the previous time step (cycle) if cycle is not available.
- Converts GFS files in GRIB format to NetCDF format.




## Logging
The script logs various messages using a logging utility from `dtcv2_util`.


# Installation
## Dependences
To run meteo is required
- [x] Python 3.8  or higher
- [x] ecCodes library (recomended version 2.27 or lower)

## Installing in Linux 

Can be installed using pip3 
```
pip3 install datetime eccodes ecmwflibs cfgrib xarray requests netcdf4 
pip3 install -i https://test.pypi.org/simple/ dtcv2-util==0.0.59
```

## Installing in Mac ARM64 (M1 M2 M3 Apple Chip)

For ARM64 architecture you can use CONDA or PIP

### Option 1 CONDA

For conda installation use
```
conda install  datetime eccodes ecmwflibs cfgrib xarray requests netcdf4 dtcv2_utils
```
### Option 2 PIP

You can also install the packages by using pip3
```
pip3 install datetime eccodes ecmwflibs cfgrib xarray requests netcdf4 dtcv2_utils
``` 
However the library ECCODES could be required after installing. 
_It's highly recomended to use HOMEBREW to install the package_.
```
brew install eccodes
```
## ecCodes version higher than 2.27 (hpbl unrecognized variable name)

If the version of your eccodes library is higher than **2.27.1** the variable _hpbl_ has been replaced by _hbl_.

You can check your version with the command

```
python -m cfgrib selfcheck
```
To make it possible to read that variable we need to add the **hpbl** variable to GFS2 dictionaries. 

The first step is identify where the package has been installed.

### Find ecCodes location on Linux

```
whereis eccodes
```
### Find ecCodes location on MacOS

_PIP and HOMEBREW_

```
pip3 show eccodes
```

If Homebrew was used the default library is _/opt/homebrew/Cellar/eccodes/[version]_ 

You can also get the information by using
```
brew info eccodes

```
## Updating ecCodes

Then run the script called update_eccodes.sh. _Make sure you are calling the path that contains a folder called_ **definitions**

### MacOS PIP and HOMEBREW


§In **MacOS** the folder can be something like 
_/opt/homebrew/Cellar/eccodes/2.30.0/share/eccodes_ 

### MacOS CONDA

If CONDA was used to install the cfgrib package the eccodes library is 
located inside the anaconda3 folder, and looks like this 
_<<path-to-anaconda3/anaconda3/pkgs/eccodes-<<version->>/share/eccodes_

### Linux

On **Linux** can be like something like _/usr/share/eccodes/definitions_

## RUNNING the script

The resources folder contains a script called update_eccodes.sh
This bash add the variable hpbl to the eccodes library dictionary. If 
general adding is needed it can be done by running the script and adding 
the path to the eccodes library. **However some center have their own 
dictionary**

To run to GFS it is **required** to add the center **kwbc** at the  
```

sh update_eccodes.sh <path_to_eccodes> kwbc
```
More information about definition of variables in 
https://confluence.ecmwf.int/display/UDOC/Creating+your+own+local+definitions+-+ecCodes+GRIB+FAQ  

## How to run Meteo
The script supports python or python3.

There are two possible arguments to be used:

- **-m** : d / c / a . Mode of running, d (only Download the data), c (only Concatenates the data to create the netCDF file ) and a (do All)

- **i** : path to the meteo.input

If there are not parameters given, the default ones are 
- -m a
- -i ./meteo.inp
```
python meteo.py
python3 meteo.py
python3 -m a -i <path_to_inp>
```
## Configure the input data

- PROJECT_PATH= (absolute path)  to the project path, folder Meteo will be created to download data)
- METEO SOURCE = [GFS/ERA5/OPEN_DATA/GFES]
- LOCATION SOURCE [MANUAL/FILE] = refers to source of area parameters. If source file you can use predefine json file with areas or define the path to a personal file with the same structure
- AREA_NAME (String) =Name of the area predefined in the file area.json(resources folder). Only used if LOCATION_SOURCE =FILE 
- AREA_FILE =(absolute Path) to file with areas
- LON_RANGE =(min_longitude max_longitude) : range of longitudes that define the area. Only used if LOCATION_SOURCE=MANUAL 
- LON_RANGE =(min_latitude max_latitude) : range of latitudes that define the area. Only used if LOCATION_SOURCE=MANUAL  
- RESOLUTION= (Float) Resolution if the grid in deg
- OUTPUT= (Str) if AUTO, files will be named with format FH-YYYYMMDD_HHz.grb, else FH-<OUTPUT>.grb
- TIME_SOURCE= [AUTO/MANUAL] Defines if date and cycles will be given by user or just take the last available 
- DATE= (DD/MM/YYYY): Specific date to download the data
- CYCLE = [0/6/12/18] : hour of model start
- TIME_STEP = [minhour maxhour] range of hours of forecast to be download
- TIME_RESOLUTION: (Int) hourly expressed is the step in range TIME step. If hourly forecast required = 1
