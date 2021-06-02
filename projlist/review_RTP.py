import pandas as pd
import geopandas as gpd
import re, fiona, os
import numpy as np

# review the differences in multiple columns before and after changes over years
def checkDiff(export=True):
    df = modifyRTP(combineTables())
    df45 = modifyRTP(combineTables(year=2045))
    outpath = r'T:\MPO\RTP\FY20 2045 Update\Data and Resources\ProjectReview'
    if export:
        df.to_csv(os.path.join(outpath, 'project_2040.csv'), index=False)
        df45.to_csv(os.path.join(outpath, 'project_2045.csv'), index=False)
    df['ID'] = df[['Name', 'GeographicLimits', 'Description', 'EstimatedYearofConstruction']].apply(lambda row: str(row.Name) + str(row.GeographicLimits) + str(row.Description) + str(row.EstimatedYearofConstruction), axis=1)
    df45['ID'] = df45[['Name', 'GeographicLimits', 'Description', 'EstimatedYearofConstruction']].apply(lambda row: str(row.Name) + str(row.GeographicLimits) + str(row.Description) + str(row.EstimatedYearofConstruction), axis=1)
    cols = [col for col in list(df.columns) if (col in list(df45.columns)) and (col != 'ID')]
    df.columns = df.columns + '40'
    df.rename(columns={"ID40": "ID"}, inplace = True)
    df45.columns = df45.columns + '45'
    df45.rename(columns={"ID45": "ID"}, inplace = True)
    data = df.merge(df45, on='ID')
    data = data.drop(['ID'], axis=1)
    for col in cols:
        data[col+'Diff'] = data[[col+'40', col+'45']].apply(lambda row: compareDiff(row[col+'40'], row[col+'45']), axis = 1)
    if export:
        data.to_csv(os.path.join(outpath, 'project_review.csv'), index=False)
    return data

# compare the values before and after changes over years
def compareDiff(a, b):
    if type(a) is float and type(b) is float:
        res = b - a
    elif a != b:
        res = 999
    else:
        res = 0
    return res

# clearn RTP format
def modifyRTP(df):
    rtplist = df.RTP.unique()
    strlist = [item for item in rtplist if type(item) is str]
    df = df[~df.RTP.isin(strlist)]
    df = df[~df.RTP.astype(float).isna()]
    df.RTP = df.RTP.astype(int)
    return df

# combine spreadsheets in one dataframe
# edit parts of the spreadsheet to have consistent formats
def combineTables(year=2040, excludeTransit = False):
    if year == 2040:
        table='2040 Project List_Consolidated draft with AQ (ORIGINAL).xlsx'
    else:
        table='Working DRAFT 2045 Project List.xlsx'
        
    xl = pd.ExcelFile(table)
    sheetNames = xl.sheet_names
    sheetNames = [sheetnm for sheetnm in sheetNames if sheetnm != 'Table Data']
    if excludeTransit:
        sheetNames = [sheetnm for sheetnm in sheetNames if 'Transit' not in sheetnm]
    for sheetName in sheetNames:
        #print(sheetName)
        if sheetName == sheetNames[0]:
            df = readTable(sheetName=sheetName, year=year)
        else:
            ndf = readTable(sheetName=sheetName, year=year)
            if ndf.shape[0] == 0:
                pass
            else:
                selectedColumns = [a for a in list(ndf.columns) if a in list(df.columns)]
                ndf = ndf[selectedColumns]
                df = df[selectedColumns]
                df = df.append(ndf, ignore_index=True)
    return df

# read each spreadsheet and convert it to dataframe
def readTable(sheetName='Auto Constrained - Arterial Lin',
              year=2040):
    if year == 2040:
        table='2040 Project List_Consolidated draft with AQ (ORIGINAL).xlsx'
    else:
        table='Working DRAFT 2045 Project List.xlsx'
        
    xl = pd.ExcelFile(table)
    
    if sheetName == 'Transit Constrained':
        if year == 2040:
            df1 = xl.parse(sheetName, skiprows=3, nrows=6)
            df1 = addCategory(df1)
            columns = df1.columns

            df2 = xl.parse(sheetName, skiprows=10, nrows=9)
            df2.columns = list(columns[0:(len(columns)-1)])
            df2 = addCategory(df2)

            df3 = xl.parse(sheetName, skiprows=20, nrows=6)
            df3.columns = list(columns[0:(len(columns)-1)])
            df3 = addCategory(df3)       
        else:
            df1 = xl.parse(sheetName, nrows=5)
            df1 = addCategory(df1)
            columns = df1.columns

            df2 = xl.parse(sheetName, skiprows=7, nrows=9)
            df2.columns = list(columns[0:(len(columns)-1)])
            df2 = addCategory(df2)

            df3 = xl.parse(sheetName, skiprows=17, nrows=6)
            df3.columns = list(columns[0:(len(columns)-1)])
            df3 = addCategory(df3)       

        df = pd.concat([df1, df2, df3], ignore_index=True)
        df.rename(columns={"Unnamed: 8": "Year of Construction Cost Max"}, inplace=True)
        
    else:
        df = xl.parse(sheetName)
        if len([col for col in df.columns if 'Unnamed' in col]) > 5:
            df = xl.parse(sheetName,  skiprows=3)
        if year == 2045:
            if sheetName in ['Bike Illustrative - withRd', 'Bike Illustrative - onstreet w', 
                             'Bike Illustrative - onstreet w', 'Bike Illustrative onstreet wout']:
                df.rename(columns={"Unnamed: 7": "Year of Construction Cost Max"}, inplace=True)
            else:
                df.rename(columns={"Unnamed: 8": "Year of Construction Cost Max"}, inplace=True)
        else:
            if sheetName in ['Auto Constrained - Study', 'Bike Constrained - wRd', 
                             'Bike Constrained - onstreet w', 'Bike Constrained - onstreet wou',
                             'Bike Illustrative - woutRD', 'Bike Illustrative - onstreet w',
                             'Bike Illustrative onstreet wout', 'Transit Illustrative']:
                df.rename(columns={"Unnamed: 8": "Year of Construction Cost Max"}, inplace=True)
            else:
                df.rename(columns={"Unnamed: 9": "Year of Construction Cost Max"}, inplace=True)
        if df.shape[0] == 0:
            pass
        else:
            df = addCategory(df)
    if year == 2040:    
        df.rename(columns={"Year of Construction\nCost Range": "Year of Construction Cost Min"}, inplace=True)
    else:
        df.rename(columns={"Year of Construction Range": "Year of Construction Cost Min",
                           "Year of Construction\nCost Range": "Year of Construction Cost Min",
                           "Year of Construction \nCost Range": "Year of Construction Cost Min"}, inplace=True)
            
    df = df[df.columns.drop(list(df.filter(regex='Unnamed')))]
    df.columns = df.columns.str.replace(' ', '')
    df.columns = df.columns.str.replace('\n', '')
    if 'EstimatedYearofStudy(4-YearWindow)' in list(df.columns):
        df.rename(columns={"EstimatedYearofStudy(4-YearWindow)": "EstimatedYearofConstruction(4-YearWindow)"}, 
                  inplace=True) 
    df.rename(columns={"RTP#": "RTP", "EstimatedYearofConstruction(4-YearWindow)":"EstimatedYearofConstruction"}, inplace=True) 
    df.rename(columns={"GeogrpahicLimits": "GeographicLimits"}, inplace=True)
    df.rename(columns={'EstimatedCost(2016)': 'EstimatedCost',
                       'EstimatedCost(2020)': 'EstimatedCost',
                       'EstimatedCost(2021)': 'EstimatedCost',
                       'EstimatedCost(20XX)': 'EstimatedCost'}, inplace=True)

    return df

# add category to the dataframe
def addCategory(df):
    name = df['Name'][0].split(":")[1].lstrip()
    df = df.drop(labels=0, axis=0)
    df = df[df.Name.astype(str) != 'nan']
    #df = df[df.columns.drop(list(df.filter(regex='Unnamed')))]
    s = pd.Series([name])
    df['Category'] = list(s.repeat(df.shape[0]))
    return df

# get targeted layers to modify GIS data
def targetLayers(patterns = ['Constrained_Roadway', 'Illustrative_Roadway', 'Constrained_BikePed', 'Illustrative_BikePed']):
    targetLayers = []
    for pattern in patterns:
        layers = [item for item in getLayernames(pattern=pattern) if 'P1' not in item]
        targetLayers += layers
    return targetLayers

# match IDs between the table and GIS data
def matchID(rtpid_table, rtpid_layer):
    newRTPid = [a for a in rtpid_table if a not in rtpid_layer]
    missedRTPid = [a for a in rtpid_layer if a not in rtpid_table]
    commonid = [a for a in rtpid_table if a in rtpid_layer]
    return newRTPid, missedRTPid, commonid

# get RTP IDs from both spreadsheets and layers
def getIDs(excel='2040 Project List_Consolidated draft with AQ (ORIGINAL).xlsx',#Working DRAFT 2045 Project List.xlsx
           Tablepattern='Auto Constrained',
           Layerpattern='Constrained_Roadway'):
    sheetNames = getSheetnames(excel=excel, pattern=Tablepattern)
    rtpid_table = []
    for sheetName in sheetNames:
        print(sheetName)
        xl = pd.ExcelFile(excel)
        df = xl.parse(sheetName)
        if df.shape[0] != 0:
            l = getRTPid(excel=excel, sheet_name=sheetName)[1]
            rtpid_table += l
    
    layers = [item for item in getLayernames(pattern=Layerpattern) if 'P1' not in item]
    rtpid_layer = []
    for layer in layers:
        print(layer)
        l = LayerRTPid(layer = layer)
        rtpid_layer += l
    
    return rtpid_table, rtpid_layer

# get RTP ID from the layers
def LayerRTPid(gdb_file = r'T:\MPO\RTP\FY16 2040 Update\Data\RTP_2040_Data.gdb',
               layer='Constrained_Roadway_lines_P1'):
    gpdfile = gpd.read_file(gdb_file, layer=layer)
    a = gpdfile.RTP_ID.unique()
    return a[~np.isnan(a)].astype(int).tolist()

# get layer names
def getLayernames(gdb_file = r'T:\MPO\RTP\FY16 2040 Update\Data\RTP_2040_Data.gdb',
                  pattern='Constrained_Roadway'):
    layers = fiona.listlayers(gdb_file)
    return [layer for layer in layers if re.match(pattern, layer)]

# get RTP ID from the table
def getRTPid(excel='Working DRAFT 2045 Project List.xlsx',
             sheet_name='Auto Constrained - Arterial Lin'):
    xl = pd.ExcelFile(excel)
    df = xl.parse(sheet_name)
    if len([col for col in df.columns if 'Unnamed' in col]) > 5:
            df = xl.parse(sheet_name,  skiprows=3)
    if df.shape[0] != 0:
        name = df['Name'][0].split(":")[1].lstrip()
        df = df.drop(labels=0, axis=0)
        rtplist = df['RTP #'].unique()
        strlist = [item for item in rtplist if type(item) is str]
        if len(strlist) > 0:
            for s in strlist:
                rtplist = rtplist[rtplist != s]
        a = rtplist.astype(float)
        b = a[~np.isnan(a)].astype(int).tolist()
        res = [int(ele) for ele in b if ele > 0]
    return name, res

# get spreadsheet names from the table file
def getSheetnames(excel='Working DRAFT 2045 Project List.xlsx',
                 pattern='Auto Constrained'):
    xl = pd.ExcelFile(excel)
    sheetList = xl.sheet_names
    return [sheet for sheet in sheetList if re.match(pattern, sheet)]