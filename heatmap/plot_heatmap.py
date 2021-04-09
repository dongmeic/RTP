import rasterio, fiona, os
import contextily as ctx
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
from matplotlib.ticker import ScalarFormatter
from rasterio.plot import show, show_hist
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.mask import mask
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

path = r'T:\Models\Heatmap'
MPObd = gpd.read_file("V:/Data/Transportation/MPO_Bound.shp")

def plotHeatmap(year = 2045, data = "jobs", dataName = 'Employment', method = 'Kernel',  
                cellSize = 100, colormap = 'Reds', export = False):
    fileName = method + data + str(year)[2:4] + "_" + str(cellSize)
    file = os.path.join(path, fileName + ".tif")
    src = rasterio.open(file)
    fig, ax = plt.subplots(1, figsize=(28, 24))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("bottom", size="5%", pad="2%")
    data = src.read(1)
    ndata = np.where(data == data.min(), np.nan, data)
    data_ex = data[data != data.min()]
    image = show(ndata,  
                 transform=src.transform,
                 ax=ax,
                 cmap=colormap)
    MPObd.plot(ax=ax, facecolor="none", edgecolor="black", linestyle='--')
    ctx.add_basemap(ax, source=ctx.providers.Stamen.TonerLite, alpha=0.3)
    ax.set_title(dataName + " " + method + " Heatmap in " + str(year) + " Size: " + str(cellSize), 
                 fontsize=50, fontname="Palatino Linotype", color="grey", loc = 'center')
    image_hidden = ax.imshow(ndata,cmap=colormap)
    fmt = mpl.ticker.ScalarFormatter(useMathText=True)
    fmt.set_powerlimits((0, 0))
    cbar = plt.colorbar(image_hidden, format=fmt, ax=ax, cax=cax, orientation="horizontal")
    mpl.rcParams.update({'font.size': 20})
    ax.axis("off");
    if export:
        imageName = fileName + ".png"
        plt.savefig(os.path.join(path, imageName), transparent=True, bbox_inches='tight')
        print("Saved image " + imageName + "...")
    src.close()