#!/bin/env python 

import configparser
import os 
from cdo import *
cdo = Cdo()

config = configparser.ConfigParser()
config.read('regridding.cfg')
domain_dir = config['Parameter Specs']['domain_file_dir']
domain_file = config['Parameter Specs']['domain_file']
domain = os.path.join(domain_dir, domain_file)
grid = config['Parameter Specs']['grid']
res = config['Parameter Specs']['res']
outdir = config['Parameter Specs']['output_dir']


filename = os.path.join(config['GTOPO']['dir'], 
			config['GTOPO']['filename'])
		
# crop file
crop_file = os.path.join(outdir, 'cropped_dem.nc')
cdo.sellonlatbox("100,280,-50,50", input="-selname,Band1 %s" %filename, output=crop_file)

# regrid file
tmp1 = os.path.join(outdir, 'sdat_10003_1_20180525_151136146_tmp.nc')
tmp2 = os.path.join(outdir, 'sdat_10003_1_20180525_151136146_%s_tmp.nc' %grid)
regrid_file = os.path.join(outdir, 'sdat_10003_1_20180525_151136146_%s.nc' %grid)

# set fillvalues to missing values to avoid incorrect remapping of coastal gridcells, 
# solution adapted from https://code.mpimet.mpg.de/boards/2/topics/6172?r=6199
cdo.setvrange('-1000,1000', input=crop_file, output=tmp1)
cdo.setmisstonn(input=tmp1, output=tmp2)

# remap both land and ocean gridcells so that coastal gridcells are assigned valid values
cdo.remapnn(domain, input=tmp2, output=regrid_file)
	
# remove temp files
rm_files = [crop_file, tmp1, tmp2]
for file_obj in rm_files:
	os.remove(file_obj)
