import numpy as np
import netCDF4 as nc
from PIL import Image
import matplotlib.pyplot as plt
import pyproj
import cartopy.crs as ccrs
from scipy.interpolate import interp1d
import pyresample as pr
from pyresample.geometry import AreaDefinition
from pycoast import ContourWriterAGG
import aggdraw


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
    cnt=floatToCnt(np.array(temp))
    image_def=imageArea(lat,lon)
    swath_def=pr.SwathDefinition(lons=lon_array,lats=lat_array)
    image_con=pr.image.ImageContainerNearest(cnt,swath_def,radius_of_influence=50000)
    image_new=image_con.resample(image_def)
    ImageS=Image.fromarray(image_new.image_data,'L')
    setGridAndCoastline(ImageS,image_def)
    ImageS.show()
    
def floatToCnt(temp):
    max_value=np.max(temp)
    min_value=np.min(temp)
    f=interp1d([min_value,max_value],[255,0])
    return np.array(f(temp),dtype='uint8')

def imageArea(lat,lon):
    #p=pyproj.Proj(proj='eqc',lat_0=lat,lon_0=lon)
    x1,y1=-1000000*2,-1000000*2
    x2,y2= 1000000*2, 1000000*2
    area_id='ADT Area'
    description='Typhoon Image '
    proj_id='Typhoon'
    projection={'proj':'eqc','lat_0':lat,'lon_0':lon,'a':6371228.0,'units':'m'}
    return AreaDefinition(area_id,description,proj_id,projection,1000,1000,(x1,y1,x2,y2))

def setGridAndCoastline(ImageS,image_def):
    ShapePath = 'D:\ADTPython\Table\gshhg-shp-2.3.7'
    ttfFile = 'D:\ADTpython\Table\LiberationMono-Regular.ttf'
    cw = ContourWriterAGG(ShapePath)
    cw.add_coastlines(ImageS,image_def,resolution='l',outline=(255,0,0),width=2)
    font = aggdraw.Font('white',ttfFile)
    cw.add_grid(ImageS,image_def,(20,20),(10,10),font,outline=(0,0,255),width=3)

if __name__ == '__main__':
    ff="D:\ADTPython\HS_H08_20210911_0400_B14_19W_TY.nc"
    lat,lon,temp=readNcFile(ff)
    central_lat,central_lon=findCentralPosition(lat,lon)
    plotTemp(central_lat,central_lon,lat,lon,temp)

