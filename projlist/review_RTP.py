import pandas as pd
import geopandas as gpd
import re, fiona
import numpy as np

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
