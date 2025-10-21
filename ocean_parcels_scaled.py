import math
from datetime import timedelta
from operator import attrgetter
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from shapely.geometry import Point
import shapefile
from shapely.geometry import shape
import random

from parcels import (
    AdvectionRK4,
    FieldSet,
    JITParticle,
    ParticleSet,
    Variable,
)

filenames = {'U': "hdf5/swain_vel/4000m/Velocity2d_U.nc", #change this name
             'V': "hdf5/swain_vel/4000m/Velocity2d_V.nc"} #change this name too


shp_file = "../GBR_reef_names/Swain_reef/swain_reef.shp"
#shp_file = "../GBR_reef_names/swain_sample/GBR_names_swain_sample.shp"
shp = shapefile.Reader(shp_file)

# x number of particles per km
particles_per_km = 11

def generate_random(number, polygon):
    points = []
    minx, miny, maxx, maxy = polygon.bounds
    while len(points) < number:
        pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if polygon.contains(pnt):
            points.append(pnt)
    return points

#calculate area in square kilometers
shp_area = gpd.read_file(shp_file)
area = shp_area.area/10**6
# round areas to nearest whole number
area_r = area.round()
# if area = 0, change to 1
area_r.replace(0.0, 1.0, inplace=True)

# list of number of particles for each polygon
points_per_feature = []

# list of number of particles for each polygon
for i in area_r:
    points_per_feature.append(i*particles_per_km)


# generate our random points
all_points_x = []
all_points_y = []
# loop through all features and add the points to our master list
#for j in points_per_feature:
for i in range(0,len(shp.shapeRecords())):
    feature = shp.shapeRecords()[i]
    feat = feature.shape.__geo_interface__
    shp_geom = shape(feat)
    points = generate_random(points_per_feature[i], shp_geom)
    for p in points:
        all_points_x.append(p.coords.xy[0][0])
        all_points_y.append(p.coords.xy[1][0])

variables = {'U': 'Band1',
             'V': 'Band1'}
dimensions = {'lat': 'y',
              'lon': 'x',
              'time': 'time'}

def DeleteErrorParticle(particle, fieldset, time):
    if particle.state >= 40:  # deletes every particle that throws an error
        particle.delete()

#print(sorted(all_points_x))
#print(sorted(all_points_y))
fieldset = FieldSet.from_netcdf(filenames, variables, dimensions, mesh="flat")

pset = ParticleSet.from_list(fieldset=fieldset, pclass=JITParticle,
                             time=432000, # start after 5 days
                             lon=all_points_x,   # releasing on a line: the start longitude and latitude
                             lat=all_points_y)  # releasing on a line: the end longitude and latitude


output_file = pset.ParticleFile(name="Trajectory_swain_scaled_4.zarr", outputdt=timedelta(hours=0.2))
pset.execute([AdvectionRK4,DeleteErrorParticle],
             runtime=timedelta(days=2),#, 16000, 171900, 1255885
             dt=timedelta(minutes=10),
             output_file=output_file)

#output_file.export()
#output_file.close()
ds = xr.open_zarr("Trajectory_swain_scaled_500_4.zarr")

plt.plot(ds.lon.T, ds.lat.T, ".-")
plt.xlabel("Zonal distance [m]")
plt.ylabel("Meridional distance [m]")
plt.show()
