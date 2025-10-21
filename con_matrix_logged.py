import geopandas as gpd 
import numpy as np
from datetime import timedelta as delta
import xarray as xr
import shapefile
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
import matplotlib.pyplot as plt
from matplotlib import colormaps
from matplotlib.ticker import PercentFormatter
import pandas as pd
import time
from datetime import datetime
startTime = datetime.now()

#load dataset
data_xarray = xr.open_zarr('../Trajectory_swain_scaled_25.zarr')

#grab start point coordinates
start_lat = data_xarray["lat"][:,0].values #go to lat and pull all particles, first value
start_lon = data_xarray["lon"][:,0].values                                                                 

#grab end point coordinates
end_lat = data_xarray["lat"][:,-1].values #go to lat and pull all particles, last value                   
end_lon = data_xarray["lon"][:,-1].values                                                                  

#combine start coordinates 
start_points = np.stack([start_lon, start_lat], axis=1) # had to change lat and lon around
end_points = np.stack([end_lon, end_lat], axis=1) # had to change lat and lon around
#print(end_points)

#save startpoints as shapefile
w = shapefile.Writer('start_points')
w.field('name', 'C')
i = 0
for p in start_points:
    w.point(p[0],p[1])
    w.record('point'+str(i))
    i = i+1

w.close()

#save endpoints as shapefile
w = shapefile.Writer('end_points')
w.field('name', 'C')
i = 0
for p in end_points:
    w.point(p[0],p[1])
    w.record('point'+str(i))
    i = i+1

w.close()

################ import in the new shape files

#import end points shapefiles
endpoints = gpd.read_file("end_points.shp")
endpoints.crs = "EPSG:32756"

#import start points shp file
startpoints = gpd.read_file("start_points.shp")
startpoints.crs = "EPSG:32756"

#import reef polygon shp file
polys = gpd.read_file("../../../../GBR_reef_names/Swain_reef/swain_reef.shp")

# Create 10 m buffer of each poly = copy poly but with area 10 m bigger
# create shp file to see the buffer if needed
#reefs_buffer = "reef_buffer.shp"

# Create a new column for the enlarged geometries
polys['geometry_buffer'] = polys['geometry'].buffer(10)

#which particles start in which reef
joined = gpd.sjoin(left_df=polys, right_df=startpoints, how='left')
joined['Number']=range(0,len(joined)+0)
joined_start = joined[['LOC_NAME_S','Number']] # dataframe --- puts reefs in wrong order
start = joined_start.groupby('LOC_NAME_S', sort=False)['Number'].agg(list).to_dict() #dictionary

# which particles finish in which reef - not needed
#joined_end = gpd.sjoin(left_df=endpoints, right_df=polys, how='left')
#joined_end['Number']=range(0,len(joined)+0)
#joined_end = joined_end[['LOC_NAME_S','Number']] # dataframe
#end = joined_end.groupby('LOC_NAME_S')['Number'].agg(list).to_dict() # dictionary

    
# connectivity matrix
matrix = np.zeros((len(polys),len(polys)))
for p in range(0,len(polys)): # loop through polys
    particle_list = start[polys["LOC_NAME_S"][p]] #pulls the particle numbers that started in the poly
    for pp in range(0,len(polys)): #loop over all of the polys again
        for particle in particle_list: #for the particles which started in our "first" polygon
            if (polys['geometry_buffer'][pp].contains(endpoints['geometry'][particle])): # which ones finish in our "second" poly
                matrix[pp][p] = matrix[pp][p] + 1 # and add them up - this controls sink source dimesion

# turn matrix into dataframe
column_names = polys['LOC_NAME_S']
row_names = polys['LOC_NAME_S']
con_matrix = pd.DataFrame(matrix, index=row_names, columns=column_names) #convert to pandas
con_matrix.to_csv('swain_scaled.csv') # save to csv
print(con_matrix)

######### calulate connectivity as decimals
# create list of total number of released particles for each reef  
start_particles = []
for i in start.keys():
    start_particles+=[[i,len(start[i])]]

#turn into dataframe
start_particles = pd.DataFrame(start_particles, columns=['reef_name', 'particles_released'])
start_particles.to_csv('start_particles_swain.csv')

# read in matrix as csv
df = pd.read_csv("swain_scaled.csv", header=0, index_col=['LOC_NAME_S'])
# read in start_particles as csv
sp = pd.read_csv("start_particles_swain.csv", usecols=['reef_name','particles_released'])
sp_list = sp['particles_released'].to_list()

# calculate connectivity in decimals
connectivity = df / sp_list
connectivity = connectivity.round(2)
connectivity.to_csv('connectivity_decimal.csv')

# this is where log scale can be done
connectivity_log = connectivity.apply(np.log10)

print(datetime.now() - startTime)
# plot connectivity matrix
f = plt.figure(figsize=(19, 15))
plt.matshow(connectivity_log, fignum=f.number)
cb = plt.colorbar()
cb.ax.set_ylabel('Connectivity', size=14)
plt.ylabel('Sink Reefs', size=14)
plt.xlabel('Source Reefs', size=14)
plt.title('Swain Area', fontsize=18);
plt.savefig('swain_scaled', bbox_inches='tight')
plt.show()
