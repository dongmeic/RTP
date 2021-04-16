import arcpy, os
import pandas as pd

# set-up
boundPath = r"C:\Users\clid1852\OneDrive - lanecouncilofgovernments\data\Boundaries"
UGBbound = os.path.join(boundPath, "UGB.shp")
MPObound = r"V:\Data\Transportation\MPO_Boundary.shp"
pointPath = r'T:\Models\Heatmap'

variables = ["households", "jobs"]
years = [2020, 2045]
AOIs = ['MPO', 'Within UGB', 'Lane']
UGBs = ['COB', 'EUG', 'SPR']

def getCounts(variable = 'households', year = 2020, 
              AOI = 'MPO', UGB = 'COB'):
    
    layerName = variable + str(year)[2:4] + 'prj.shp'
    pointLayer = os.path.join(pointPath, layerName)
    
    if AOI == 'MPO':
        boundLayer = MPObound
    elif AOI == 'Within UGB':
        boundLayer = arcpy.management.SelectLayerByAttribute(UGBbound, "NEW_SELECTION", "ugbcity = '{0}'".format(UGB), None)
    else:
        boundLayer = UGBbound 
                 
    if AOI == 'Lane':
        input_layer = arcpy.management.SelectLayerByLocation(pointLayer, "COMPLETELY_WITHIN", MPObound, None, 
                                                                     "NEW_SELECTION", "NOT_INVERT")
        
        input_layer = arcpy.management.SelectLayerByLocation(input_layer, "COMPLETELY_WITHIN", boundLayer, None, 
                                                                     "SUBSET_SELECTION", "NOT_INVERT")
        
        input_layer = arcpy.management.SelectLayerByLocation(input_layer, "COMPLETELY_WITHIN", boundLayer, None, 
                                                                     "SWITCH_SELECTION", "NOT_INVERT")
        
    else:
        input_layer = arcpy.management.SelectLayerByLocation(pointLayer, "COMPLETELY_WITHIN", boundLayer, None, 
                                                                     "NEW_SELECTION", "NOT_INVERT")
        
    return int(arcpy.GetCount_management(input_layer)[0])


def getTable():
    table = []
    for variable in variables:
        byVariable = []
        colnms = []
        for year in years:
            byYear = []
            colnm = []
            for AOI in AOIs:
                if AOI == 'Within UGB':
                    for UGB in UGBs:
                        cnt = getCounts(variable = variable, year = year, AOI = AOI, UGB = UGB)
                        print("Got counts for {0} in {1} in {2}...".format(variable, UGB, year))
                        byYear.append(cnt)
                        colnm.append(UGB + str(year)[2:4])
                else:
                    cnt = getCounts(variable = variable, year = year, AOI = AOI)
                    print("Got counts for {0} in {1} in {2}...".format(variable, AOI, year))
                    byYear.append(cnt)
                    colnm.append(AOI + str(year)[2:4])
            byVariable += byYear
            colnms += colnm
        table.append(byVariable)
    print("Got the table...")
    df = pd.DataFrame(table)
    df.columns = colnms
    df.index= variables
    print(df)
    df.to_csv(os.path.join(pointPath, "Households_Employment_Counts.csv"))