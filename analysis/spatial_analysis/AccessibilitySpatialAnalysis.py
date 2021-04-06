import arcpy, os, numpy, datetime
from arcpy import env

env.workspace = r"T:\MPO\RTP\FY20 2045 Update\Data and Resources\Network_Analysis\Network_Analysis.gdb"
env.overwriteOutput = True

def AccessibilitySpatialJoin(layer_name = "baseyearHH_FeatureToPoint",
                             AOI = "MPO",
                             jobfield = "ojobs",
                             service = "Jobs",
                             travel_mode = "Biking",
                             year = 2020):
    
    print("Spatial analysis for {0} by {1} in {2} in {3}...".format(service, travel_mode, AOI, str(year)))
    
    now = datetime.datetime.now()
    
    sa_layer = "SA" + travel_mode + service
    if year == 2045:
        sa_layer = sa_layer + str(year)
    
    if service == "Jobs":
        if year == 2020:
            point_layer = "baseyear" + service + "_FeatureToPoint"
        else:
            point_layer = "forecast" + service + "_FeatureToPoint"
            
        print("Getting a join table between service area and job points...")
        table = arcpy.AddJoin_management(sa_layer, "ObjectID", point_layer, "ORIG_FID", "KEEP_COMMON")
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
        EFAbound = r"T:\MPO\RTP\FY20 2045 Update\Data and Resources\PerformanceAnalysis\service_transit_equity\equity_area.shp"
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
        arcpy.analysis.SpatialJoin(input_layer, out_SAjoin, out_layer, "JOIN_ONE_TO_ONE", "KEEP_COMMON",'btype "btype" true true false 80 Text 0 0,First,#,{0},btype,0,80;nrsqft "nrsqft" true true false 8 Double 0 0,First,#,{0},nrsqft,-1,-1;rsqft "rsqft" true true false 8 Double 0 0,First,#,{0},rsqft,-1,-1;du "du" true true false 8 Double 0 0,First,#,{0},du,-1,-1;yrbuilt "yrbuilt" true true false 8 Double 0 0,First,#,{0},yrbuilt,-1,-1;lpid "lpid" true true false 8 Double 0 0,First,#,{0},lpid,-1,-1;pundev "pundev" true true false 8 Double 0 0,First,#,{0},pundev,-1,-1;dev_land "dev_land" true true false 8 Double 0 0,First,#,{0},dev_land,-1,-1;developed "developed" true true false 8 Double 0 0,First,#,{0},developed,-1,-1;obtype "obtype" true true false 80 Text 0 0,First,#,{0},obtype,0,80;orsqft "orsqft" true true false 8 Double 0 0,First,#,{0},orsqft,-1,-1;onrsqft "onrsqft" true true false 8 Double 0 0,First,#,{0},onrsqft,-1,-1;odu "odu" true true false 8 Double 0 0,First,#,{0},odu,-1,-1;zid "zid" true true false 8 Double 0 0,First,#,{0},zid,-1,-1;rezoned "rezoned" true true false 8 Double 0 0,First,#,{0},rezoned,-1,-1;city "city" true true false 80 Text 0 0,First,#,{0},city,0,80;annexed "annexed" true true false 8 Double 0 0,First,#,{0},annexed,-1,-1;ozid "ozid" true true false 8 Double 0 0,First,#,{0},ozid,-1,-1;AreaPerJob "AreaPerJob" true true false 8 Double 0 0,First,#,{0},AreaPerJob,-1,-1;isNonRes "isNonRes" true true false 4 Long 0 0,First,#,{0},isNonRes,-1,-1;jobs "jobs" true true false 8 Double 0 0,First,#,{0},jobs,-1,-1;ojobs "ojobs" true true false 8 Double 0 0,First,#,{0},ojobs,-1,-1;hh "hh" true true false 8 Double 0 0,First,#,{0},hh,-1,-1;ohh "ohh" true true false 8 Double 0 0,First,#,{0},ohh,-1,-1;ORIG_FID "ORIG_FID" true true false 4 Long 0 0,First,#,{0},ORIG_FID,-1,-1;{1}_{2} "{2}" true true false 8 Double 0 0,Sum,#,{3},{1}_{2},-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,{3},Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,{3},Shape_Area,-1,-1'.format(layer_name, point_layer, jobfield, out_SAjoin), 
                           "COMPLETELY_WITHIN", None, '')
    else:
        arcpy.analysis.SpatialJoin(input_layer, sa_layer, out_layer, "JOIN_ONE_TO_ONE", "KEEP_COMMON",'btype "btype" true true false 80 Text 0 0,First,#,{0},btype,0,80;nrsqft "nrsqft" true true false 8 Double 0 0,First,#,{0},nrsqft,-1,-1;rsqft "rsqft" true true false 8 Double 0 0,First,#,{0},rsqft,-1,-1;du "du" true true false 8 Double 0 0,First,#,{0},du,-1,-1;yrbuilt "yrbuilt" true true false 8 Double 0 0,First,#,{0},yrbuilt,-1,-1;lpid "lpid" true true false 8 Double 0 0,First,#,{0},lpid,-1,-1;pundev "pundev" true true false 8 Double 0 0,First,#,{0},pundev,-1,-1;dev_land "dev_land" true true false 8 Double 0 0,First,#,{0},dev_land,-1,-1;developed "developed" true true false 8 Double 0 0,First,#,{0},developed,-1,-1;obtype "obtype" true true false 80 Text 0 0,First,#,{0},obtype,0,80;orsqft "orsqft" true true false 8 Double 0 0,First,#,{0},orsqft,-1,-1;onrsqft "onrsqft" true true false 8 Double 0 0,First,#,{0},onrsqft,-1,-1;odu "odu" true true false 8 Double 0 0,First,#,{0},odu,-1,-1;zid "zid" true true false 8 Double 0 0,First,#,{0},zid,-1,-1;rezoned "rezoned" true true false 8 Double 0 0,First,#,{0},rezoned,-1,-1;city "city" true true false 80 Text 0 0,First,#,{0},city,0,80;annexed "annexed" true true false 8 Double 0 0,First,#,{0},annexed,-1,-1;ozid "ozid" true true false 8 Double 0 0,First,#,{0},ozid,-1,-1;AreaPerJob "AreaPerJob" true true false 8 Double 0 0,First,#,{0},AreaPerJob,-1,-1;isNonRes "isNonRes" true true false 4 Long 0 0,First,#,{0},isNonRes,-1,-1;jobs "jobs" true true false 8 Double 0 0,First,#,{0},jobs,-1,-1;ojobs "ojobs" true true false 8 Double 0 0,First,#,{0},ojobs,-1,-1;hh "hh" true true false 8 Double 0 0,First,#,{0},hh,-1,-1;ohh "ohh" true true false 8 Double 0 0,First,#,{0},ohh,-1,-1;ORIG_FID "ORIG_FID" true true false 4 Long 0 0,First,#,{0},ORIG_FID,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,{1},Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,{1},Shape_Area,-1,-1'.format(layer_name, sa_layer), "COMPLETELY_WITHIN", None, '')
    
    later = datetime.datetime.now()
    elapsed = later - now
    print("Completed spatial analysis for {0} by {1} in {2} in {3} completed with {4} seconds...".format(service, 
                                                                                                   travel_mode, 
                                                                                                   AOI, 
                                                                                                   str(year), 
                                                                                                   elapsed))


# Do Not Run - way too slow with thousands of points
def AccessibilitySA_withCursor(layer_name = "baseyear_hh",
                                 condition = "ohh > 0",
                                 newfield = "sa_jobs",
                                 AOI = "MPO",
                                 point_layer = "baseyearJobs_FeatureToPoint",
                                 jobfield = "jobs",
                                 service = "Jobs",
                                 travel_mode = "Biking",
                                 year = 2020):
    
    sa_layer = "SA" + travel_mode + service
    
    if year == 2045:
        sa_layer = sa_layer + str(year)
        
    table = arcpy.AddJoin_management(sa_layer, "ObjectID", point_layer, "ORIG_FID", "KEEP_COMMON")
    arcpy.CopyFeatures_management(table, "joinedtable")
    
    arcpy.management.MakeFeatureLayer("parcels_FeatureToPoint", layer_name, condition)
    fieldList = arcpy.ListFields(layer_name)
    field_names = [f.name for f in fieldList]
    if newfield in field_names:
        pass
    else:
        arcpy.AddField_management(layer_name, newfield, "FLOAT", "", "", 20)
    now = datetime.datetime.now()
    with arcpy.da.UpdateCursor(layer_name, ['ORIG_FID', newfield]) as cursor: 
        for row in cursor:
            print(row)
            targetHH = arcpy.management.SelectLayerByAttribute(layer_name, "NEW_SELECTION", "ORIG_FID = {0}".format(row[0]), 
                                                           None)
            selectedSA = arcpy.management.SelectLayerByLocation("joinedtable", "COMPLETELY_CONTAINS", targetHH, 
                                               None, "NEW_SELECTION", "NOT_INVERT")         
            
            bound = r"T:\MPO\RTP\FY20 2045 Update\Data and Resources\PerformanceAnalysis\service_transit_equity\equity_area.shp"
            if AOI == "EFA" or AOI == "NEFA": # Equity Focused Areas OR Non-Equity Focused Areas
                arcpy.management.SelectLayerByLocation(selectedSA, "INTERSECT", bound, 
                                                   None, "SUBSET_SELECTION", "NOT_INVERT")
                if AOI == "NEFA":
                    arcpy.management.SelectLayerByLocation(selectedSA, "INTERSECT", bound, 
                                                   None, "SWITCH_SELECTION", "NOT_INVERT")
            
            if service == "Jobs":
                fieldName = point_layer + "_" + jobfield
                fieldsum = arcpy.da.TableToNumPyArray(selectedSA, fieldName, skip_nulls=True)
                value = fieldsum[fieldName].sum()
                row[1] = value
            elif service == "Amenities":
                fieldName = "ObjectID"
                fieldcount = arcpy.da.TableToNumPyArray(selectedSA, fieldName, skip_nulls=True)
                value = fieldsum[fieldName].count()
                row[1] = value
                
            cursor.updateRow(row)
            print(value)
            
    later = datetime.datetime.now()
    elapsed = later - now
    print("updated field values for {0} by {1} in {2} in {3} completed with {4} seconds...".format(service, 
                                                                                                   travel_mode, 
                                                                                                   AOI, 
                                                                                                   str(year), 
                                                                                                   elapsed))
    arcpy.SelectLayerByAttribute_management(layer_name, "CLEAR_SELECTION")
    arcpy.CopyFeatures_management(layer_name, layer_name)
    
    