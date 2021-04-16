import arcpy, os, numpy, datetime, re, os.path
from arcpy import env
import pandas as pd
from os import path

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


def AccessibilityEquityArea_HH(service = "Jobs",
                            travel_mode = "Biking",
                            year = 2020):
    
    EFAbound = os.path.join(input_folder, "PerformanceAnalysis", "service_transit_equity", "equity_area.shp")
    AOI = "EFA"

    sa_layer = "SA" + travel_mode + "HH"
    if year == 2020:
        sa_layer_name = sa_layer
        sa_layer = os.path.join(input_folder, sa_layer + ".shp")
    else:
        sa_layer_name = sa_layer + str(year)
        sa_layer = os.path.join(input_folder, sa_layer + str(year) + ".shp")

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
        count_field = "Join_Count"

    for i in EquityAreaID.index:
        BlkGrp10 = EquityAreaID['BlkGrp10'].values[i]
        EFAbound = arcpy.management.SelectLayerByAttribute(EFAbound, "NEW_SELECTION", "BlkGrp10 = '{0}'".format(BlkGrp10), None)
        
        input_layer = arcpy.management.SelectLayerByLocation(layer_for_spatial_join, "COMPLETELY_WITHIN", EFAbound, None, 
                                                                     "NEW_SELECTION", "NOT_INVERT")
        
        EFA_ID = EquityAreaID['EquityArea'].values[i]
        out_layer = AOI + str(EFA_ID) + service + travel_mode + str(year)
        
        if service == "Jobs":
            arcpy.analysis.SpatialJoin(sa_layer, input_layer, out_layer, "JOIN_ONE_TO_ONE", "KEEP_COMMON", 'FacilityID "FacilityID" true true false 18 Double 0 18,First,#,{0},FacilityID,-1,-1;{1} "{1}" true true false 8 Double 0 0,Sum,#,{2},{1},-1,-1'.format(sa_layer_name, count_field, layer_for_spatial_join), "COMPLETELY_CONTAINS", None, '')
        else:                
            arcpy.analysis.SpatialJoin(sa_layer, input_layer, out_layer, "JOIN_ONE_TO_ONE", "KEEP_COMMON", 'FacilityID "FacilityID" true true false 18 Double 0 18,First,#,{0},FacilityID,-1,-1'.format(sa_layer_name), "COMPLETELY_CONTAINS", None, '')   

        print("Got summarized {0} in {1} by {2} in {3}...".format(service, AOI + str(EFA_ID), travel_mode, year))


def AccessibilitySpatialJoin_HH(AOI = "MPO",
                             service = "Jobs",
                             travel_mode = "Biking",
                             year = 2020, 
                             keep = "only"):
    
    print("Spatial analysis for {0} by {1} in {2} in {3}...".format(service, travel_mode, AOI, str(year)))
    
    now = datetime.datetime.now()
    
    sa_layer = "SA" + travel_mode + "HH"
    if year == 2020:
        sa_layer = sa_layer
        hh_point_layer = "baseyearHH_FeatureToPoint"
        target_field = 'ohh'
    else:
        sa_layer = sa_layer + str(year)
        hh_point_layer = "forecastHH_FeatureToPoint"
        target_field = 'hh'
    
    # change the identifier field name in the household service area for table join
    oldFieldList = [f.name for f in arcpy.ListFields(sa_layer)]
    oldField = [i for i in oldFieldList if re.search(r'FacilityID', i)][0]
    newField = "FacilityID"
    if oldField != newField:
        arcpy.AlterField_management(sa_layer, oldField, newField)
    
    # change the identifier field name in the household point layer for table join
    oldFieldList = [f.name for f in arcpy.ListFields(hh_point_layer)]
    if oldField not in oldFieldList:
        arcpy.AddField_management(hh_point_layer, "FacilityID", "LONG")
        arcpy.CalculateField_management(hh_point_layer, "FacilityID", "!ORIG_FID! + 1", "PYTHON3" )
      
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
        count_field = 'Join_Count'
                 
    out_layer = AOI + service + travel_mode + str(year) + "HH_SA"
    outTablepath = os.path.join(input_folder, 'Network_Analysis')
    SAcsv = out_layer + '.csv'
    
    file = os.path.join(outTablepath, SAcsv)
    if path.exists(file):
        print("Got the spatial join table...")
    else:
        print("Getting a spatial join between the household service areas and the {0} points...".format(service))
    
        if service == "Jobs":
            if keep == "all":
                # keep all the fields in the household service area
                arcpy.analysis.SpatialJoin(sa_layer, layer_for_spatial_join, out_layer, "JOIN_ONE_TO_ONE", "KEEP_COMMON", 'FacilityID "FacilityID" true true false 18 Double 0 18,First,#,{0},FacilityID,-1,-1;SAPolyName "SAPolyName" true true false 80 Text 0 0,First,#,{0},SAPolyName,0,80;FromBreak "FromBreak" true true false 24 Double 15 23,First,#,{0},FromBreak,-1,-1;ToBreak "ToBreak" true true false 24 Double 15 23,First,#,{0},ToBreak,-1,-1;ObjectID "ObjectID" true true false 18 Double 0 18,First,#,{0},ObjectID,-1,-1;FaciliName "FaciliName" true true false 80 Text 0 0,First,#,{0},FaciliName,0,80;SourceID "SourceID" true true false 18 Double 0 18,First,#,{0},SourceID,-1,-1;SourceOID "SourceOID" true true false 18 Double 0 18,First,#,{0},SourceOID,-1,-1;PosAlong "PosAlong" true true false 24 Double 15 23,First,#,{0},PosAlong,-1,-1;SideOfEdge "SideOfEdge" true true false 18 Double 0 18,First,#,{0},SideOfEdge,-1,-1;CurApp "CurApp" true true false 18 Double 0 18,First,#,{0},CurApp,-1,-1;Status "Status" true true false 18 Double 0 18,First,#,{0},Status,-1,-1;SnapX "SnapX" true true false 24 Double 15 23,First,#,{0},SnapX,-1,-1;SnapY "SnapY" true true false 24 Double 15 23,First,#,{0},SnapY,-1,-1;SnapZ "SnapZ" true true false 24 Double 15 23,First,#,{0},SnapZ,-1,-1;DTNIM "DTNIM" true true false 24 Double 15 23,First,#,{0},DTNIM,-1,-1;AttrLength "AttrLength" true true false 24 Double 15 23,First,#,{0},AttrLength,-1,-1;BreLen "BreLen" true true false 80 Text 0 0,First,#,{0},BreLen,0,80;Length "Length" true true false 24 Double 15 23,First,#,{0},Length,-1,-1;Area "Area" true true false 24 Double 15 23,First,#,{0},Area,-1,-1;{1} "{1}" true true false 8 Double 0 0,Sum,#,{2},{1},-1,-1'.format(sa_layer, count_field, layer_for_spatial_join), "COMPLETELY_CONTAINS", None, '')
            else:
                # keep the target fields only
                arcpy.analysis.SpatialJoin(sa_layer, layer_for_spatial_join, out_layer, "JOIN_ONE_TO_ONE", "KEEP_COMMON", 'FacilityID "FacilityID" true true false 18 Double 0 18,First,#,{0},FacilityID,-1,-1;{1} "{1}" true true false 8 Double 0 0,Sum,#,{2},{1},-1,-1'.format(sa_layer, count_field, layer_for_spatial_join), "COMPLETELY_CONTAINS", None, '')
        else:
            if keep == "all":
                # keep all the fields in the household service area
                arcpy.analysis.SpatialJoin(sa_layer, layer_for_spatial_join, out_layer, "JOIN_ONE_TO_ONE", "KEEP_COMMON", 'FacilityID "FacilityID" true true false 18 Double 0 18,First,#,{0},FacilityID,-1,-1;SAPolyName "SAPolyName" true true false 80 Text 0 0,First,#,{0},SAPolyName,0,80;FromBreak "FromBreak" true true false 24 Double 15 23,First,#,{0},FromBreak,-1,-1;ToBreak "ToBreak" true true false 24 Double 15 23,First,#,{0},ToBreak,-1,-1;ObjectID "ObjectID" true true false 18 Double 0 18,First,#,{0},ObjectID,-1,-1;FaciliName "FaciliName" true true false 80 Text 0 0,First,#,{0},FaciliName,0,80;SourceID "SourceID" true true false 18 Double 0 18,First,#,{0},SourceID,-1,-1;SourceOID "SourceOID" true true false 18 Double 0 18,First,#,{0},SourceOID,-1,-1;PosAlong "PosAlong" true true false 24 Double 15 23,First,#,{0},PosAlong,-1,-1;SideOfEdge "SideOfEdge" true true false 18 Double 0 18,First,#,{0},SideOfEdge,-1,-1;CurApp "CurApp" true true false 18 Double 0 18,First,#,{0},CurApp,-1,-1;Status "Status" true true false 18 Double 0 18,First,#,{0},Status,-1,-1;SnapX "SnapX" true true false 24 Double 15 23,First,#,{0},SnapX,-1,-1;SnapY "SnapY" true true false 24 Double 15 23,First,#,{0},SnapY,-1,-1;SnapZ "SnapZ" true true false 24 Double 15 23,First,#,{0},SnapZ,-1,-1;DTNIM "DTNIM" true true false 24 Double 15 23,First,#,{0},DTNIM,-1,-1;AttrLength "AttrLength" true true false 24 Double 15 23,First,#,{0},AttrLength,-1,-1;BreLen "BreLen" true true false 80 Text 0 0,First,#,{0},BreLen,0,80;Length "Length" true true false 24 Double 15 23,First,#,{0},Length,-1,-1;Area "Area" true true false 24 Double 15 23,First,#,{0},Area,-1,-1'.format(sa_layer), "COMPLETELY_CONTAINS", None, '')

            else:
                # keep the target fields only
                arcpy.analysis.SpatialJoin(sa_layer, layer_for_spatial_join, out_layer, "JOIN_ONE_TO_ONE", "KEEP_COMMON", 'FacilityID "FacilityID" true true false 18 Double 0 18,First,#,{0},FacilityID,-1,-1'.format(sa_layer), "COMPLETELY_CONTAINS", None, '')
                
        oldFieldList = [f.name for f in arcpy.ListFields(out_layer)]
        if target_field in oldFieldList:
            arcpy.management.DeleteField(out_layer, target_field)
        # export the table from service area
        SAtable = arcpy.conversion.TableToTable(out_layer, outTablepath, SAcsv, '', '', '')
    
    HHcsv = AOI + "_HH" + str(year) + '.csv'  
    file = os.path.join(outTablepath, HHcsv)
    if path.exists(file):
        print("Got the selected household points table...")
    else:
        print("Selecting target household points...")
        
        # select the target households in AOI  
        MPObound = r"V:\Data\Transportation\MPO_Boundary.shp"
        if AOI == "MPO":
            print("Getting the household points within the MPO boundary...")
            input_layer = arcpy.management.SelectLayerByLocation(hh_point_layer, "COMPLETELY_WITHIN", MPObound, None, 
                                                                         "New_SELECTION", "NOT_INVERT")
        elif AOI == "EFA" or AOI == "NEFA": # Equity Focused Areas OR Non-Equity Focused Areas
            print("Getting the household points within the equity focused areas...")
            EFAbound = os.path.join(input_folder, "PerformanceAnalysis", 
                                                     "service_transit_equity", "equity_area.shp")
            input_layer = arcpy.management.SelectLayerByLocation(hh_point_layer, "COMPLETELY_WITHIN", EFAbound, None, 
                                                                     "NEW_SELECTION", "NOT_INVERT")
            if AOI == "NEFA":
                print("Switching the household points to the non-equtiy focused areas within MPO...")
                input_layer = arcpy.management.SelectLayerByLocation(input_layer, "COMPLETELY_WITHIN", EFAbound, None, 
                                                                         "SWITCH_SELECTION", "NOT_INVERT")
                input_layer = arcpy.management.SelectLayerByLocation(input_layer, "COMPLETELY_WITHIN", MPObound, None, 
                                                                         "SUBSET_SELECTION", "NOT_INVERT")

        # total household counts
        totcnt = int(arcpy.GetCount_management(hh_point_layer)[0])
        # selected household counts
        selcnt = int(arcpy.GetCount_management(input_layer)[0])

        print("About {0}% of household points are selected within the area of interest...".format(str(round(selcnt/totcnt*100))))

        # keep only the required fields from the household points
        dropFields = [f.name for f in arcpy.ListFields(hh_point_layer)]
        keepFields = ['OBJECTID', 'Shape',  target_field, newField]
        for field in keepFields:
            dropFields.remove(field)

        for field in dropFields:
            arcpy.management.DeleteField(input_layer, field)
   
        # export the table from the selected household points
        HHtable = arcpy.conversion.TableToTable(input_layer, outTablepath, HHcsv, '', '', '')
    
    outCSV = os.path.join(input_folder, 'Network_Analysis', out_layer + '_df' + '.csv')
    if path.exists(outCSV):
        print("Got the final data table...")
    else:
        SDdf = pd.read_csv(SAtable[0])
        HHdf = pd.read_csv(HHtable[0])

        df = SDdf[[count_field, newField]].merge(HHdf[[target_field, newField]], how='inner', on = newField)
        df.to_csv(outCSV, index=False)
    
        print("Got the final output table to include only the required fields...")
    
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

    
    ######################################## Below are discarded codes #######################################
    # NOT RUN: this approach is wrong
def AccessibilityTAZ(AOI = "MPO",
                     service = "Jobs",
                     travel_mode = "Biking",
                     year = 2020):
    
    MPObound = r"V:\Data\Transportation\MPO_Boundary.shp"
    level = "KateTAZ"
    
    if service == "Jobs":
        layer_name = level + "_FeatureToPoint"
    else:
        layer_name = os.path.join(input_folder, "PerformanceAnalysis", 
                                                 "service_transit_equity", "service_stops.shp")
        
    if AOI == "MPO":
        print("Getting the {0} points within the MPO boundary...".format(service))
        input_layer = arcpy.management.SelectLayerByLocation(layer_name, "COMPLETELY_WITHIN", MPObound, None, 
                                                                     "New_SELECTION", "NOT_INVERT")
    elif AOI == "EFA" or AOI == "NEFA": # Equity Focused Areas OR Non-Equity Focused Areas
        print("Getting the {0} points within the equity focused areas...".format(service))
        EFAbound = os.path.join(input_folder, "PerformanceAnalysis", 
                                         "service_transit_equity", "equity_area.shp")
        input_layer = arcpy.management.SelectLayerByLocation(layer_name, "COMPLETELY_WITHIN", EFAbound, None, 
                                                                 "NEW_SELECTION", "NOT_INVERT")
        if AOI == "NEFA":
            print("Switching the {0} points to the non-equtiy focused areas within MPO...".format(service))
            input_layer = arcpy.management.SelectLayerByLocation(input_layer, "COMPLETELY_WITHIN", EFAbound, None, 
                                                                     "SWITCH_SELECTION", "NOT_INVERT")
            input_layer = arcpy.management.SelectLayerByLocation(input_layer, "COMPLETELY_WITHIN", MPObound, None, 
                                                                     "SUBSET_SELECTION", "NOT_INVERT")
    
    sa_layer = "SA" + travel_mode + level
    out_layer = AOI + service + travel_mode + str(year) + "TAZ"
    input_layer = arcpy.management.SelectLayerByLocation(input_layer, "COMPLETELY_WITHIN", sa_layer, None, 
                                                         "SUBSET_SELECTION", "NOT_INVERT")
    
    if arcpy.Exists(out_layer):
        arcpy.Delete_management(out_layer)
    arcpy.CopyFeatures_management(input_layer, out_layer)
    print("Got the targeted TAZ points and saved as {0}".format(out_layer))