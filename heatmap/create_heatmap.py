import os, arcpy

ExtensionName = 'Spatial'
if arcpy.CheckExtension(ExtensionName) == "Available":
        arcpy.CheckOutExtension(ExtensionName)
        
arcpy.env.workspace = r'T:\Models\StoryMap\UrbanSim\UrbanSim.gdb'
arcpy.env.overwriteOutput = True
MPOBound = "V:/Data/Transportation/MPO_Bound.shp"
arcpy.env.extent = MPOBound
mask = MPOBound

path = r'T:\Trans Projects\Model Development\UrbanSim_LandUse\Output\Simulation_47_Final_RTP'
outpath = r'T:\Models\Heatmap'

def convertXYpoints(intableName = "jobs_2045_xy"):
    s = intableName.split("_")
    intable = os.path.join(path, intableName + ".csv")
    outLayer = os.path.join(outpath, s[0] + s[1][2:4] + ".shp")
    arcpy.management.XYTableToPoint(intable, outLayer, "x", "y", None, "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision")
    print("created output {0}".format(outLayer))
    
    
def createHeatmap(yrbuilt = 2021, field = "nnsqft", cellSize = 100, 
                  intableName = "jobs_2045_xy", method = 'Kernel', xypoint = False):
    
    if xypoint:
        s = intableName.split("_")
        outLayer = os.path.join(outpath, s[0] + s[1][2:4] + ".shp")
        outRaster = os.path.join(outpath, method + s[0] + s[1][2:4] + "_" + str(cellSize) + ".tif")
        print("creating raster data for heatmap...")
        with arcpy.EnvManager(mask=MPOBound):
            if method == 'Point':
                arcpy.gp.PointDensity_sa(outLayer, "NONE", outRaster, 
                                       cellSize, "", "SQUARE_KILOMETERS")  

            else:
                arcpy.gp.KernelDensity_sa(outLayer, "NONE", outRaster, 
                                       cellSize, "", "SQUARE_KILOMETERS", "DENSITIES", "GEODESIC")                
            
    else:
        print("converting parcel polygons to centroid points...")
        parcelCentroid = arcpy.FeatureToPoint_management(in_features=os.path.join(path, 'output', 'newDevAnn' + str(yrbuilt) +'.shp'), 
                                    out_feature_class="newDevCentroid", point_location="INSIDE")
        print("creating raster data for heatmap...")
        outRaster = os.path.join(path, 'output', "KernelD_" + field + "_" + str(yrbuilt) + ".tif")
        with arcpy.EnvManager(mask=MPOBound):
            arcpy.gp.KernelDensity_sa(parcelCentroid, field, outRaster,
                                  cellSize,"", "SQUARE_KILOMETERS", "DENSITIES", "GEODESIC")
    print("completed...")