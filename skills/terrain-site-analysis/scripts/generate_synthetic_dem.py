#!/usr/bin/env python3
"""Create a deterministic fictional elevation raster for offline smoke tests only."""
from pathlib import Path
import numpy as np
import rasterio
from rasterio.transform import from_origin
from pyproj import Transformer

output = Path(__file__).resolve().parent.parent / 'examples' / 'synthetic_demo_dem.tif'
output.parent.mkdir(parents=True, exist_ok=True)
center_x, center_y = Transformer.from_crs('EPSG:4326','EPSG:32616',always_xy=True).transform(-85.6681,42.9634)
n=170
rows,cols=np.mgrid[:n,:n]
z=(240 + 0.06*(cols-n/2) + 8*np.exp(-((cols-90)**2+(rows-70)**2)/350) - 5*np.exp(-((cols-60)**2+(rows-125)**2)/550)).astype('float32')
with rasterio.open(output,'w',driver='GTiff',height=n,width=n,count=1,dtype='float32',crs='EPSG:32616',transform=from_origin(center_x-n,center_y+n,2,2),nodata=-9999) as dst:
    dst.write(z,1)
print(f'Wrote fictional elevation test raster: {output} (NOT real site data)')