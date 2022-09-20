from matplotlib import projections
import numpy as np
import netCDF4 as nc
from PIL import Image
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from scipy.interpolate import interp1d
import pyresample as pr
from pyresample.geometry import AreaDefinition

def readNcFile(nc_file):
    dd=nc.Dataset(ff)
    lat=dd.variables['latitude'][:]
    lon=dd.variables['longitude'][:]
    temp=dd.variables['brightness_temp'][:]
    return lat,lon,temp

def findCentralPosition(lat,lon):
    x,y=lat.shape
    return lat[int(x/2),int(y/2)],lon[int(x/2),int(y/2)]

def plotTemp(lat,lon,lat_array,lon_array,temp):
    image_def=imageArea(lat,lon)
    swath_def=pr.SwathDefinition(lons=lon_array,lats=lat_array)
    temp_new=pr.kd_tree.resample_nearest(swath_def,temp,image_def,radius_of_influence=50000)
    crs=image_def.to_cartopy_crs()
    fig=plt.figure()
    ax=plt.axes(projection=crs)
    setGridAndCoastline(ax)
    ax.imshow(temp_new,cmap='viridis_r',extent=crs.bounds)
    fig.savefig('test.png')

def floatToCnt(temp):
    max_value=np.max(temp)
    min_value=np.min(temp)
    f=interp1d([min_value,max_value],[0,255])
    return np.array(f(temp),dtype='uint8')

def imageArea(lat,lon):
    #p=pyproj.Proj(proj='eqc',lat_0=lat,lon_0=lon)
    x1,y1=-1000000,-1000000
    x2,y2=1000000,1000000
    area_id='ADT Area'
    description='Typhoon Image '
    proj_id='Typhoon'
    projection={'proj':'eqc','lat_0':lat,'lon_0':lon,'a':6371228.0,'units':'m'}
    return AreaDefinition(area_id,description,proj_id,projection,1000,1000,(x1,y1,x2,y2))

def setGridAndCoastline(ax):
    ax.gridlines(draw_labels=True,)
    ax.coastlines(resolution='10m',color='black',linewidth=1.3)   

if __name__ == '__main__':
    ff="D:\ADTPython\HS_H08_20210911_0400_B14_19W_TY.nc"
    lat,lon,temp=readNcFile(ff)
    central_lat,central_lon=findCentralPosition(lat,lon)
    plotTemp(central_lat,central_lon,lat,lon,temp)

