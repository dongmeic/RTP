import os, arcpy

ExtensionName = 'Spatial'
if arcpy.CheckExtension(ExtensionName) == "Available":
        arcpy.CheckOutExtension(ExtensionName)
        
arcpy.env.workspace = r'T:\Models\StoryMap\UrbanSim\UrbanSim.gdb'
arcpy.env.overwriteOutput = True
MPOBound = "V:/Data/Transportation/MPO_Bound.shp"

path = r'T:\Trans Projects\Model Development\UrbanSim_LandUse\Output\Simulation_47_Final_RTP'
outpath = r'T:\Models\Heatmap'

def convertXYpoints(intableName = "jobs_2045_xy"):
    s = intableName.split("_")
    intable = os.path.join(path, intableName + ".csv")
    outLayer = os.path.join(outpath, s[0] + s[1][2:4] + ".shp")
    arcpy.management.XYTableToPoint(intable, outLayer, "x", "y", None, "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision")
    print("created output {0}".format(outLayer))
  
    prj_layer = os.path.join(outpath, s[0] + s[1][2:4] + "prj.shp")
    arcpy.management.Project(outLayer, prj_layer, "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", None, "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", "NO_PRESERVE_SHAPE", None, "NO_VERTICAL")
    print("reproject output {0}".format(prj_layer))
    
def createHeatmap(yrbuilt = 2021, field = "nnsqft", cellSize = 100, searchRadius = 1000,
                  intableName = "jobs_2045_xy", method = "Kernel"):   

    s = intableName.split("_")
    outLayer = os.path.join(outpath, s[0] + s[1][2:4] + "prj.shp")
    outRaster = os.path.join(outpath, method + s[0] + s[1][2:4] + "_" + str(cellSize) + "_" + str(searchRadius) + ".tif")
    print("creating raster data for {0} heatmap in {1} using {2} Density with a cell size {3} and search radius {4}...".format(s[0], s[1], method, str(cellSize), str(searchRadius)))
    
    arcpy.env.extent = MPOBound
    mask = MPOBound
    with arcpy.EnvManager(mask=MPOBound):
        if method == "Point":
            arcpy.gp.PointDensity_sa(outLayer, "NONE", outRaster, 
                                   cellSize, "", "SQUARE_KILOMETERS")  

        else:
            arcpy.gp.KernelDensity_sa(outLayer, "NONE", outRaster, 
                                   cellSize, searchRadius, "SQUARE_KILOMETERS", "DENSITIES", "GEODESIC")                
            

    print("completed...")