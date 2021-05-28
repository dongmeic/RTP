import pandas as pd
import geopandas as gpd
import re, fiona
import numpy as np


def modifyRTP(df):
    rtplist = df.RTP.unique()
    strlist = [item for item in rtplist if type(item) is str]
    df = df[~df.RTP.isin(strlist)]
    df = df[~df.RTP.astype(float).isna()]
    df.RTP = df.RTP.astype(int)
    return df

def combineTables(year=2040):
    if year == 2040:
        table='2040 Project List_Consolidated draft with AQ (ORIGINAL).xlsx'
    else:
        table='Working DRAFT 2045 Project List.xlsx'
        
    xl = pd.ExcelFile(table)
    sheetNames = xl.sheet_names
    sheetNames = [sheetnm for sheetnm in sheetNames if sheetnm != 'Table Data']
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
                             'Bike Illustrative onstreet wout']:
                df.rename(columns={"Unnamed: 8": "Year of Construction Cost Max"}, inplace=True)
            elif sheetName == 'Transit Illustrative':
                df.rename(columns={"Unnamed: 7": "Year of Construction Cost Max"}, inplace=True)
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
    df.rename(columns={"RTP#": "RTP"}, inplace=True) 
    df.rename(columns={"GeogrpahicLimits": "GeographicLimits"}, inplace=True)
    return df

def addCategory(df):
    name = df['Name'][0].split(":")[1].lstrip()
    df = df.drop(labels=0, axis=0)
    df = df[df.Name.astype(str) != 'nan']
    #df = df[df.columns.drop(list(df.filter(regex='Unnamed')))]
    s = pd.Series([name])
    df['Category'] = list(s.repeat(df.shape[0]))
    return df

def targetLayers(patterns = ['Constrained_Roadway', 'Illustrative_Roadway', 'Constrained_BikePed', 'Illustrative_BikePed']):
    targetLayers = []
    for pattern in patterns:
        layers = [item for item in getLayernames(pattern=pattern) if 'P1' not in item]
        targetLayers += layers
    return targetLayers

def matchID(rtpid_table, rtpid_layer):
    newRTPid = [a for a in rtpid_table if a not in rtpid_layer]
    missedRTPid = [a for a in rtpid_layer if a not in rtpid_table]
    commonid = [a for a in rtpid_table if a in rtpid_layer]
    return newRTPid, missedRTPid, commonid

def getIDs(excel='Working DRAFT 2045 Project List.xlsx',
           Tablepattern='Auto Constrained',
           Layerpattern='Constrained_Roadway'):
    sheetNames = getSheetnames(pattern=Tablepattern)
    rtpid_table = []
    for sheetName in sheetNames:
        #print(sheetName)
        xl = pd.ExcelFile(excel)
        df = xl.parse(sheetName)
        if df.shape[0] != 0:
            l = getRTPid(sheet_name=sheetName)[1]
            rtpid_table += l
    
    layers = [item for item in getLayernames(pattern=Layerpattern) if 'P1' not in item]
    rtpid_layer = []
    for layer in layers:
        #print(layer)
        l = LayerRTPid(layer = layer)
        rtpid_layer += l
    
    return rtpid_table, rtpid_layer

def LayerRTPid(gdb_file = r'T:\MPO\RTP\FY16 2040 Update\Data\RTP_2040_Data.gdb',
               layer='Constrained_Roadway_lines_P1'):
    gpdfile = gpd.read_file(gdb_file, layer=layer)
    a = gpdfile.RTP_ID.unique()
    return a[~np.isnan(a)].astype(int).tolist()

def getLayernames(gdb_file = r'T:\MPO\RTP\FY16 2040 Update\Data\RTP_2040_Data.gdb',
                  pattern='Constrained_Roadway'):
    layers = fiona.listlayers(gdb_file)
    return [layer for layer in layers if re.match(pattern, layer)]

def getRTPid(excel='Working DRAFT 2045 Project List.xlsx',
             sheet_name='Auto Constrained - Arterial Lin'):
    xl = pd.ExcelFile(excel)
    df = xl.parse(sheet_name)
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

def getSheetnames(excel='Working DRAFT 2045 Project List.xlsx',
                 pattern='Auto Constrained'):
    xl = pd.ExcelFile(excel)
    sheetList = xl.sheet_names
    return [sheet for sheet in sheetList if re.match(pattern, sheet)]