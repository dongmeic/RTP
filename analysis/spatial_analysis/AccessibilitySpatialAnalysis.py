import arcpy, os, numpy, datetime
from arcpy import env

env.workspace = r"T:\MPO\RTP\FY20 2045 Update\Data and Resources\Network_Analysis\Network_Analysis.gdb"
env.overwriteOutput = True

path = r"T:\MPO\RTP\FY20 2045 Update\Data and Resources\PerformanceAnalysis\service_transit_equity"

def AccessibilitySpatialAnalysis(layer_name = "baseyear_hh",
                                 condition = "ohh > 0",
                                 newfield = "sa_jobs",
                                 AOI = "MPO",
                                 bound = os.path.join(path, "equity_area.shp"),
                                 sa_point_layer = "baseyearJobs_FeatureToPoint",
                                 jobfield = "jobs",
                                 service = "Jobs",
                                 travel_mode = "Biking",
                                 year = 2020):
    
    sa_layer = "SA" + travel_mode + service
    
    if year == 2045:
        sa_layer = sa_layer + str(year)
        
    table = arcpy.AddJoin_management(sa_layer, "ObjectID", sa_point_layer, "ORIG_FID", "KEEP_COMMON")
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
            targetHH = arcpy.management.SelectLayerByAttribute(layer_name, "NEW_SELECTION", "ORIG_FID = {0}".format(row[0]), 
                                                           None)
            selectedSA = arcpy.management.SelectLayerByLocation("joinedtable", "COMPLETELY_CONTAINS", targetHH, 
                                               None, "NEW_SELECTION", "NOT_INVERT")         
            
            if AOI == "EFA" or AOI == "NEFA": # Equity Focused Areas OR Non-Equity Focused Areas
                arcpy.management.SelectLayerByLocation(selectedSA, "INTERSECT", bound, 
                                                   None, "SUBSET_SELECTION", "NOT_INVERT")
                if AOI == "NEFA":
                    arcpy.management.SelectLayerByLocation(selectedSA, "INTERSECT", bound, 
                                                   None, "SWITCH_SELECTION", "NOT_INVERT")
            
            if service == "Jobs":
                fieldName = sa_point_layer + "_" + jobfield
                fieldsum = arcpy.da.TableToNumPyArray(selectedSA, fieldName, skip_nulls=True)
                value = fieldsum[fieldName].sum()
                row[1] = value
            elif service == "Amenities":
                fieldName = "ObjectID"
                fieldcount = arcpy.da.TableToNumPyArray(selectedSA, fieldName, skip_nulls=True)
                value = fieldsum[fieldName].count()
                row[1] = value
                
            cursor.updateRow(row)
            
    later = datetime.datetime.now()
    elapsed = later - now
    print("updated field values for {0} by {1} in {2} in {3} completed with {4} seconds...".format(service, 
                                                                                                   travel_mode, 
                                                                                                   AOI, 
                                                                                                   str(year), 
                                                                                                   elapsed))
    arcpy.SelectLayerByAttribute_management(layer_name, "CLEAR_SELECTION")
    arcpy.CopyFeatures_management(layer_name, layer_name)
    