import arcpy, os
from arcpy import env
import pandas as pd

env.overwriteOutput = True
path = r'T:\MPO\RTP\FY20 2045 Update\Data and Resources\PerformanceAnalysis'
env.workspace = os.path.join(path, "SystemCompleteness/SystemCompleteness.gdb")
facilities = os.path.join(path, 'sidewalk_bikeway_trails/facilities_mpo.shp')
network = os.path.join(path, "network.shp")


def get_completeness(facility_mode = 'bikeway', level = 'regionwide'):
    a = network_with_facility(facility_mode, level)
    return a, round((a/258.76 * 100), 2)

def network_with_facility(facility_mode = 'bikeway', level = 'regionwide'):
    arcpy.MakeFeatureLayer_management(facilities, facility_mode, "mode = '{0}'".format(facility_mode))
    arcpy.MakeFeatureLayer_management(network, "network")
    arcpy.CalculateGeometryAttributes_management("network", [["Length_mi", "LENGTH_GEODESIC"]], "MILES_US")
    
    if level == 'regionwide':
        arcpy.SelectLayerByLocation_management("network", "INTERSECT", facility_mode, "70 Feet")

    elif level == 'equity-focused areas':
        equity_area = os.path.join(path, 'service_transit_equity/equity_area.shp')
        arcpy.MakeFeatureLayer_management(equity_area, "equity_area")
        arcpy.SelectLayerByLocation_management("network", "INTERSECT", "equity_area")
        arcpy.SelectLayerByLocation_management("network", "INTERSECT", facility_mode, "70 Feet", "SUBSET_SELECTION")
    else:
        if level == '1/4 miles from transit stops':
            transit_stops = os.path.join(path, 'service_transit_equity/transit_stops.shp')
            arcpy.MakeFeatureLayer_management(transit_stops, "transit_stops")
        else:
            high_freq_transit = os.path.join(path, 'service_transit_equity/high_frequency_transit.shp')
            arcpy.MakeFeatureLayer_management(high_freq_transit, "transit_stops")
        
        arcpy.SelectLayerByLocation_management("network", "WITHIN_A_DISTANCE_GEODESIC", "transit_stops", "0.25 Miles")
        arcpy.SelectLayerByLocation_management("network", "INTERSECT", facility_mode, "70 Feet", "SUBSET_SELECTION")       
        
    
    arcpy.Statistics_analysis("network", "network_w_" + facility_mode, [["Length_mi", "SUM"]])
    fields = [f.name for f in arcpy.ListFields("network_w_" + facility_mode)]
    arr = arcpy.da.TableToNumPyArray("network_w_" + facility_mode, fields)
    table = pd.DataFrame(arr, columns=fields)
    return round(table['SUM_Length_mi'].values[0], 2)


