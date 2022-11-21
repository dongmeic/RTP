import arcpy, os, datetime
from arcpy import env

env.overwriteOutput = True
env.workspace = r"T:\MPO\RTP\FY20 2045 Update\Data and Resources\Network_Analysis\Network_Analysis.gdb"
input_folder = r"T:\MPO\RTP\FY20 2045 Update\Data and Resources"
inNetworkDataset = "Network_Ped_Bike/Network_ND"

if arcpy.CheckExtension("network") == "Available":
    arcpy.CheckOutExtension("network")
else:
    raise arcpy.ExecuteError("Network Analyst Extension license is not available.")
    
def ServiceAreaAnalysis(layer_name = "Service Area", 
                       impedance = "Biking by distance",
                       dist = 17582.4, # this distance unit is feet
                       facilities = os.path.join(input_folder, "PerformanceAnalysis", 
                                                 "service_transit_equity", "service_stops.shp"),
                       mode = "Biking",
                       destination = "Jobs"):
    print('Creating service area analysis layer...')
    result_object = arcpy.na.MakeServiceAreaAnalysisLayer(inNetworkDataset, layer_name, impedance, 
                                                      "FROM_FACILITIES", [dist], None, "LOCAL_TIME_AT_LOCATIONS", 
                                                      "POLYGONS", "STANDARD", "OVERLAP", "RINGS", "100 Meters", None, None)
    print('Done...')
    layer_object = result_object.getOutput(0)
    sublayer_names = arcpy.na.GetNAClassNames(layer_object)
    facilities_layer_name = sublayer_names["Facilities"]
    polygons_layer_name = sublayer_names["SAPolygons"]
    print('Adding facilities...')
    field_mappings = arcpy.na.NAClassFieldMappings(layer_object,
                                                    facilities_layer_name)
    arcpy.na.AddLocations(layer_object, facilities_layer_name, facilities,
                        field_mappings, "", exclude_restricted_elements = "EXCLUDE")
    print('Done...')
    facilities_sublayer = layer_object.listLayers(facilities_layer_name)[0]
    polygons_sublayer = layer_object.listLayers(polygons_layer_name)[0]
    print('Solving service area...')
    now = datetime.datetime.now()
    solver_properties = arcpy.na.GetSolverProperties(layer_object)
    arcpy.na.Solve(layer_object)
    print('Done...')
    later = datetime.datetime.now()
    elapsed = later - now
    print(elapsed)
    print('Exporting service area polygons...')
    arcpy.management.AddJoin(polygons_sublayer, "FacilityID", facilities_sublayer, "ObjectID")
    out_featureclass = "SA" + mode + destination
    if arcpy.Exists(out_featureclass):
        arcpy.Delete_management(out_featureclass)
    if not arcpy.Exists(out_featureclass):
        arcpy.management.CopyFeatures(polygons_sublayer, out_featureclass)
    else:
        arcpy.management.Append(polygons_sublayer, out_featureclass)
    print('Done...')
