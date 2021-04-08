import os, re, datetime
import pandas as pd
import geopandas as gpd

path = r"T:\MPO\RTP\FY20 2045 Update\Data and Resources\Network_Analysis\Network_Analysis.gdb"
outPath = r"T:\MPO\RTP\FY20 2045 Update\Data and Resources"

def shortenColnm(x):
    if len(x) > 10:
        charList = [char for char in x if char.isupper()]
        if len(charList) >= 5:
            colnm = ''.join(re.findall(r'[A-Z]', x))
        else:
            colnm = ''.join(re.findall(r'[A-Z]..', x))
    else:
        colnm = x
    return colnm

def renameCols(x):
    strList = x.split("_")
    l = len(strList)
    if l == 1:
        colnm = shortenColnm(x)
    elif l == 2:
        s = strList[1]
        if s == 'Name':
            colnm = strList[0][0:6] + s
        else:
            colnm = shortenColnm(s)     
        if strList[0] == 'shape':
            colnm = 'SHP' + s
    elif l == 3:
        colnm = shortenColnm(strList[1] + strList[2])
    else:
        print("The column name is too long.")
    return colnm

def UpateHHTables(AOI = "MPO", service = "Jobs", year = 2020, travel_mode = 'Biking', 
                  EFA_ID = 5, EFA = False):
    if EFA:
        sa_layer = AOI + str(EFA_ID) + service + travel_mode + str(year)
    else:
        sa_layer = AOI + service + travel_mode + str(year) + "HH_SA"
    
    if year == 2020:
        point_layer = "baseyearHH_FeatureToPoint"
        targetField = 'ohh'
        jobField = 'ojobs'
    else:
        point_layer = "forecastHH_FeatureToPoint"
        targetField = 'hh'
        jobField = 'jobs'
        
    countField = 'Join_Count' 
    IDField = 'FacilityID'
    
    hhSA = gpd.read_file(path, layer = sa_layer)
    hhpts = gpd.read_file(path, layer = point_layer)
    
    hhSA_df = pd.DataFrame(hhSA)
    hhpts_df = pd.DataFrame(hhpts)
    
    hhpts_df[IDField] = hhpts_df['ORIG_FID'] + 1
    hhpts_df = hhpts_df[[targetField, IDField]]
    
    if service == "Jobs":
        hhSAJoined = hhSA[[IDField, jobField]].merge(hhpts_df, on=IDField, how='left')
    else:
        hhSAJoined = hhSA[[IDField, countField]].merge(hhpts_df, on=IDField, how='left')
    return hhSAJoined
    
    
def JoinHHTables(year = 2020, travel_mode = 'Biking'):
    now = datetime.datetime.now()
    sa_layer = "SA" + travel_mode + "HH"
    if year == 2020:
        sa_layer = sa_layer
        point_layer = "baseyearHH_FeatureToPoint"
        targetField = 'ohh'
    else:
        sa_layer = sa_layer + str(year)
        point_layer = "forecastHH_FeatureToPoint"
        targetField = 'hh'
    
    print("Reading the input features...")
    hhSA = gpd.read_file(path, layer = sa_layer)
    hhpts = gpd.read_file(path, layer = point_layer)
    print("Got the data...")
    
    # get the matched ID columns
    print("Renaming the input features...")
    newField = 'FacilityID'
    hhpts_df = pd.DataFrame(hhpts)
    hhpts_df[newField] = hhpts_df['ORIG_FID'] + 1
    hhpts_df = hhpts_df[['ohh', newField]]
    hhSA = hhSA.rename(columns = {x:newField for x in list(hhSA) if re.search(r'FacilityID', x)})
    # join the tables
    print("Merging the input features...")
    hhSAJoinedpts = hhSA.merge(hhpts_df, on=newField, how='left')
    # rename the columns to export due to the name length limit 10
    hhSAJoinedpts.rename(columns = {x: renameCols(x) for x in list(hhSAJoinedpts)}, inplace = True)
    hhSAJoinedpts_gpd = gpd.GeoDataFrame(hhSAJoinedpts)
    print("Writing the output feature...")
    hhSAJoinedpts_gpd.to_file(os.path.join(outPath, sa_layer + '.shp'))
    print("Exported the features with the joined table!")
    later = datetime.datetime.now()
    elapsed = later - now
    print("Used time: {0}".format(elapsed))