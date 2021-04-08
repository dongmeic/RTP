import arcpy, os, numpy, datetime, re
from arcpy import env
import pandas as pd

env.workspace = r"T:\MPO\RTP\FY20 2045 Update\Data and Resources\Network_Analysis\Network_Analysis.gdb"
env.overwriteOutput = True

input_folder = r"T:\MPO\RTP\FY20 2045 Update\Data and Resources"
EquityAreaID = pd.read_csv("../EquityAreaID.csv")

# 2 years * 3 AOI * 2 travel modes * 2 services
sas = ["Jobs", "Amenities"]
travel_modes = ["Biking", "Walking"]
layerNames = ["baseyearJobs_FeatureToPoint", "forecastJobs_FeatureToPoint"]
AOIs = ["MPO", "EFA", "NEFA"]
# matched with layer names
jobfields = ["ojobs", "jobs"]
years = [2020, 2045]
hhfields = ["ohh", "hh"]


def AccessibilitySpatialJoin_HH(AOI = "MPO",
                             service = "Jobs",
                             travel_mode = "Biking",
                             year = 2020):
    
    print("Spatial analysis for {0} by {1} in {2} in {3}...".format(service, travel_mode, AOI, str(year)))
    
    now = datetime.datetime.now()
    
    
    if service == "Jobs":
        if year == 2020:
            layer_for_spatial_join = "baseyear" + service + "_FeatureToPoint"
            count_field = "ojobs"
        else:
            layer_for_spatial_join = "forecast" + service + "_FeatureToPoint"
            count_field = "jobs"
    else:
        layer_for_spatial_join = os.path.join(input_folder, "PerformanceAnalysis", 
                                                 "service_transit_equity", "service_stops.shp")
            
        print("Getting a join table between household service area and household points...")
        oldFieldList = [f.name for f in arcpy.ListFields(sa_layer)]
        oldField = [i for i in oldFieldList if re.search(r'FacilityID', i)][0]
        newField = "FacilityID"
        if oldField != newField:
            arcpy.AlterField_management(sa_layer, oldField, newField)
        Fields = [f.name for f in arcpy.ListFields(point_layer)]
        
        if newField in Fields:
            pass
        else:
            arcpy.AddField_management(point_layer, newField, "LONG")
            
        arcpy.CalculateField_management(point_layer, newField, "!ORIG_FID! + 1", "PYTHON3" )
        
        
    out_layer = AOI + service + travel_mode + str(year) + "HH_SA"
    
    MPObound = r"V:\Data\Transportation\MPO_Boundary.shp"
    if AOI == "MPO":
        print("Getting the {0} points within the MPO boundary...".format(service))
        input_layer = arcpy.management.SelectLayerByLocation(layer_for_spatial_join, "COMPLETELY_WITHIN", MPObound, None, 
                                                                     "New_SELECTION", "NOT_INVERT")
    elif AOI == "EFA" or AOI == "NEFA": # Equity Focused Areas OR Non-Equity Focused Areas
        print("Getting the {0} points within the equity focused areas...".format(service))
        EFAbound = os.path.join(input_folder, "PerformanceAnalysis", 
                                                 "service_transit_equity", "equity_area.shp")
        input_layer = arcpy.management.SelectLayerByLocation(layer_for_spatial_join, "COMPLETELY_WITHIN", EFAbound, None, 
                                                                 "NEW_SELECTION", "NOT_INVERT")
        if AOI == "NEFA":
            print("Switching the {0} points to the non-equtiy focused areas within MPO...".format(service))
            input_layer = arcpy.management.SelectLayerByLocation(layer_for_spatial_join, "COMPLETELY_WITHIN", EFAbound, None, 
                                                                     "SWITCH_SELECTION", "NOT_INVERT")
            input_layer = arcpy.management.SelectLayerByLocation(layer_for_spatial_join, "COMPLETELY_WITHIN", MPObound, None, 
                                                                     "SUBSET_SELECTION", "NOT_INVERT")
    
    print("Getting a spatial join between the household service area joined table and the selected {0} points...".format(service))
    # keep all the fields in the household points
    if service == "Jobs":
        arcpy.analysis.SpatialJoin(out_SAjoin, input_layer, out_layer, "JOIN_ONE_TO_ONE", "KEEP_COMMON",'hh "hh" true true false 8 Double 0 0,First,#,{0},hh,-1,-1;ohh "ohh" true true false 8 Double 0 0,First,#,{0},ohh,-1,-1;{1}_{2} "{2}" true true false 8 Double 0 0,Sum,#,{3},{1}_{2},-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,{3},Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,{3},Shape_Area,-1,-1'.format(point_layer, layer_for_spatial_join, count_field, input_layer), 
                       "COMPLETELY_CONTAIN", None, '')
    else:
        arcpy.analysis.SpatialJoin(sa_layer, input_layer, out_layer, "JOIN_ONE_TO_ONE", "KEEP_COMMON",'hh "hh" true true false 8 Double 0 0,First,#,{0},hh,-1,-1;ohh "ohh" true true false 8 Double 0 0,First,#,{0},ohh,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,{1},Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,{1},Shape_Area,-1,-1'.format(layer_for_spatial_join, sa_layer), "COMPLETELY_CONTAIN", None, '')
            
    
    later = datetime.datetime.now()
    elapsed = later - now
    print("Completed spatial analysis for {0} by {1} in {2} in {3} completed with {4} timesteps...".format(service, 
                                                                                                   travel_mode, 
                                                                                                   AOI, 
                                                                                                   str(year), 
                                                                                                   elapsed))
    

def AccessibilityEquityArea(service = "Jobs",
                            travel_mode = "Biking",
                            year = 2020):
    
    EFAbound = os.path.join(input_folder, "PerformanceAnalysis", "service_transit_equity", "equity_area.shp")
    AOI = "EFA"
    layer_name = AOI + service + travel_mode + str(year)
    
    byYear = []
    colnm = []
    for i in EquityAreaID.index:
        BlkGrp10 = EquityAreaID['BlkGrp10'].values[i]
        EFAbound = arcpy.management.SelectLayerByAttribute(EFAbound, "NEW_SELECTION", "BlkGrp10 = '{0}'".format(BlkGrp10), None)
        
        if service == "Jobs":
            targetfield = layerNames[years.index(year)] + "_" + jobfields[years.index(year)]
            newfield = 'weighted_' + jobfields[years.index(year)]
        else:
            targetfield = "Join_Count"
            newfield = 'weighted_count'
            
        fieldList = arcpy.ListFields(layer_name)
        field_names = [f.name for f in fieldList]
        if newfield in field_names:
            pass
        else:
            arcpy.AddField_management(layer_name, newfield, "FLOAT", "", "", 50)
        
        hhfield = hhfields[years.index(year)]
            
        arcpy.management.CalculateField(layer_name, newfield, "!{0}! * !{1}!".format(hhfield, targetfield), "PYTHON3")
        input_layer = arcpy.management.SelectLayerByLocation(layer_name, "COMPLETELY_WITHIN", EFAbound, None, 
                                                                 "NEW_SELECTION", "NOT_INVERT")
        
        HHsum = arcpy.da.TableToNumPyArray(input_layer, hhfield, skip_nulls=True)
        Weighted = arcpy.da.TableToNumPyArray(input_layer, newfield, skip_nulls=True)
        
        acc = round(Weighted[newfield].sum() / HHsum[hhfield].sum())
        EFA_ID = EquityAreaID['EquityArea'].values[i]
        print("Got the accessibility number for {0} in {1} by {2} in {3}...".format(service, AOI + str(EFA_ID), travel_mode, year))
        byYear.append(acc)
        colnm.append(AOI + str(EFA_ID) + "_" + str(year))
    return byYear, colnm
    

def AccessibilitySpatialJoin(layer_name = "baseyearHH_FeatureToPoint",
                             AOI = "MPO",
                             jobfield = "ojobs",
                             service = "Jobs",
                             travel_mode = "Biking",
                             year = 2020,
                             keep = "all"):
    
    print("Spatial analysis for {0} by {1} in {2} in {3}...".format(service, travel_mode, AOI, str(year)))
    
    now = datetime.datetime.now()
    
    sa_layer = "SA" + travel_mode + service
    if service == "Jobs" and year == 2045:
        sa_layer = sa_layer + str(year)
    
    if service == "Jobs":
        if year == 2020:
            point_layer = "baseyear" + service + "_FeatureToPoint"
        else:
            point_layer = "forecast" + service + "_FeatureToPoint"
            
        print("Getting a join table between service area and job points...")
        oldFieldList = [f.name for f in arcpy.ListFields(sa_layer)]
        oldField = [i for i in oldFieldList if re.search(r'FacilityID', i)][0]
        newField = "FacilityID"
        if oldField != newField:
            arcpy.AlterField_management(sa_layer, oldField, newField)
        arcpy.AddField_management(point_layer, "FacilityID", "LONG")
        arcpy.CalculateField_management(point_layer, "FacilityID", "!ORIG_FID! + 1", "PYTHON3" )
        table = arcpy.AddJoin_management(sa_layer, "FacilityID", point_layer, "FacilityID", "KEEP_ALL")
        out_SAjoin = "SAJoinedTable"
        if arcpy.Exists(out_SAjoin):
            arcpy.Delete_management(out_SAjoin)
        arcpy.CopyFeatures_management(table, out_SAjoin)
        print("Completed...")
    
    out_layer = AOI + service + travel_mode + str(year)
    
    MPObound = r"V:\Data\Transportation\MPO_Boundary.shp"
    if AOI == "MPO":
        print("Getting the household points within the MPO boundary...")
        input_layer = arcpy.management.SelectLayerByLocation(layer_name, "COMPLETELY_WITHIN", MPObound, None, 
                                                                     "New_SELECTION", "NOT_INVERT")
    elif AOI == "EFA" or AOI == "NEFA": # Equity Focused Areas OR Non-Equity Focused Areas
        print("Getting the household points within the equity focused areas...")
        EFAbound = os.path.join(input_folder, "PerformanceAnalysis", 
                                         "service_transit_equity", "equity_area.shp")
        input_layer = arcpy.management.SelectLayerByLocation(layer_name, "COMPLETELY_WITHIN", EFAbound, None, 
                                                                 "NEW_SELECTION", "NOT_INVERT")
        if AOI == "NEFA":
            print("Switching the household points to the non-equtiy focused areas within MPO...")
            input_layer = arcpy.management.SelectLayerByLocation(input_layer, "COMPLETELY_WITHIN", EFAbound, None, 
                                                                     "SWITCH_SELECTION", "NOT_INVERT")
            input_layer = arcpy.management.SelectLayerByLocation(input_layer, "COMPLETELY_WITHIN", MPObound, None, 
                                                                     "SUBSET_SELECTION", "NOT_INVERT")
    
    print("Getting a spatial join between the selected household points and service area joined table...")
    # keep all the fields in the household points
    if service == "Jobs":
        if keep == "all":
            arcpy.analysis.SpatialJoin(input_layer, out_SAjoin, out_layer, "JOIN_ONE_TO_ONE", "KEEP_COMMON",'btype "btype" true true false 80 Text 0 0,First,#,{0},btype,0,80;nrsqft "nrsqft" true true false 8 Double 0 0,First,#,{0},nrsqft,-1,-1;rsqft "rsqft" true true false 8 Double 0 0,First,#,{0},rsqft,-1,-1;du "du" true true false 8 Double 0 0,First,#,{0},du,-1,-1;yrbuilt "yrbuilt" true true false 8 Double 0 0,First,#,{0},yrbuilt,-1,-1;lpid "lpid" true true false 8 Double 0 0,First,#,{0},lpid,-1,-1;pundev "pundev" true true false 8 Double 0 0,First,#,{0},pundev,-1,-1;dev_land "dev_land" true true false 8 Double 0 0,First,#,{0},dev_land,-1,-1;developed "developed" true true false 8 Double 0 0,First,#,{0},developed,-1,-1;obtype "obtype" true true false 80 Text 0 0,First,#,{0},obtype,0,80;orsqft "orsqft" true true false 8 Double 0 0,First,#,{0},orsqft,-1,-1;onrsqft "onrsqft" true true false 8 Double 0 0,First,#,{0},onrsqft,-1,-1;odu "odu" true true false 8 Double 0 0,First,#,{0},odu,-1,-1;zid "zid" true true false 8 Double 0 0,First,#,{0},zid,-1,-1;rezoned "rezoned" true true false 8 Double 0 0,First,#,{0},rezoned,-1,-1;city "city" true true false 80 Text 0 0,First,#,{0},city,0,80;annexed "annexed" true true false 8 Double 0 0,First,#,{0},annexed,-1,-1;ozid "ozid" true true false 8 Double 0 0,First,#,{0},ozid,-1,-1;AreaPerJob "AreaPerJob" true true false 8 Double 0 0,First,#,{0},AreaPerJob,-1,-1;isNonRes "isNonRes" true true false 4 Long 0 0,First,#,{0},isNonRes,-1,-1;jobs "jobs" true true false 8 Double 0 0,First,#,{0},jobs,-1,-1;ojobs "ojobs" true true false 8 Double 0 0,First,#,{0},ojobs,-1,-1;hh "hh" true true false 8 Double 0 0,First,#,{0},hh,-1,-1;ohh "ohh" true true false 8 Double 0 0,First,#,{0},ohh,-1,-1;ORIG_FID "ORIG_FID" true true false 4 Long 0 0,First,#,{0},ORIG_FID,-1,-1;{1}_{2} "{2}" true true false 8 Double 0 0,Sum,#,{3},{1}_{2},-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,{3},Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,{3},Shape_Area,-1,-1'.format(layer_name, point_layer, jobfield, out_SAjoin), 
                           "COMPLETELY_WITHIN", None, '')
        else:
            arcpy.analysis.SpatialJoin(input_layer, out_SAjoin, out_layer, "JOIN_ONE_TO_ONE", "KEEP_COMMON",'hh "hh" true true false 8 Double 0 0,First,#,{0},hh,-1,-1;ohh "ohh" true true false 8 Double 0 0,First,#,{0},ohh,-1,-1;{1}_{2} "{2}" true true false 8 Double 0 0,Sum,#,{3},{1}_{2},-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,{3},Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,{3},Shape_Area,-1,-1'.format(layer_name, point_layer, jobfield, out_SAjoin), 
                           "COMPLETELY_WITHIN", None, '')
    else:
        if keep == "all":
            arcpy.analysis.SpatialJoin(input_layer, sa_layer, out_layer, "JOIN_ONE_TO_ONE", "KEEP_COMMON",'btype "btype" true true false 80 Text 0 0,First,#,{0},btype,0,80;nrsqft "nrsqft" true true false 8 Double 0 0,First,#,{0},nrsqft,-1,-1;rsqft "rsqft" true true false 8 Double 0 0,First,#,{0},rsqft,-1,-1;du "du" true true false 8 Double 0 0,First,#,{0},du,-1,-1;yrbuilt "yrbuilt" true true false 8 Double 0 0,First,#,{0},yrbuilt,-1,-1;lpid "lpid" true true false 8 Double 0 0,First,#,{0},lpid,-1,-1;pundev "pundev" true true false 8 Double 0 0,First,#,{0},pundev,-1,-1;dev_land "dev_land" true true false 8 Double 0 0,First,#,{0},dev_land,-1,-1;developed "developed" true true false 8 Double 0 0,First,#,{0},developed,-1,-1;obtype "obtype" true true false 80 Text 0 0,First,#,{0},obtype,0,80;orsqft "orsqft" true true false 8 Double 0 0,First,#,{0},orsqft,-1,-1;onrsqft "onrsqft" true true false 8 Double 0 0,First,#,{0},onrsqft,-1,-1;odu "odu" true true false 8 Double 0 0,First,#,{0},odu,-1,-1;zid "zid" true true false 8 Double 0 0,First,#,{0},zid,-1,-1;rezoned "rezoned" true true false 8 Double 0 0,First,#,{0},rezoned,-1,-1;city "city" true true false 80 Text 0 0,First,#,{0},city,0,80;annexed "annexed" true true false 8 Double 0 0,First,#,{0},annexed,-1,-1;ozid "ozid" true true false 8 Double 0 0,First,#,{0},ozid,-1,-1;AreaPerJob "AreaPerJob" true true false 8 Double 0 0,First,#,{0},AreaPerJob,-1,-1;isNonRes "isNonRes" true true false 4 Long 0 0,First,#,{0},isNonRes,-1,-1;jobs "jobs" true true false 8 Double 0 0,First,#,{0},jobs,-1,-1;ojobs "ojobs" true true false 8 Double 0 0,First,#,{0},ojobs,-1,-1;hh "hh" true true false 8 Double 0 0,First,#,{0},hh,-1,-1;ohh "ohh" true true false 8 Double 0 0,First,#,{0},ohh,-1,-1;ORIG_FID "ORIG_FID" true true false 4 Long 0 0,First,#,{0},ORIG_FID,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,{1},Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,{1},Shape_Area,-1,-1'.format(layer_name, sa_layer), "COMPLETELY_WITHIN", None, '')
        else:
            arcpy.analysis.SpatialJoin(input_layer, sa_layer, out_layer, "JOIN_ONE_TO_ONE", "KEEP_COMMON",'hh "hh" true true false 8 Double 0 0,First,#,{0},hh,-1,-1;ohh "ohh" true true false 8 Double 0 0,First,#,{0},ohh,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,{1},Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,{1},Shape_Area,-1,-1'.format(layer_name, sa_layer), "COMPLETELY_WITHIN", None, '')
            
    
    later = datetime.datetime.now()
    elapsed = later - now
    print("Completed spatial analysis for {0} by {1} in {2} in {3} completed with {4} timesteps...".format(service, 
                                                                                                   travel_mode, 
                                                                                                   AOI, 
                                                                                                   str(year), 
                                                                                                   elapsed))
