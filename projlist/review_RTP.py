import pandas as pd
import geopandas as gpd
import re, fiona, os, glob
import numpy as np


excel='2040 Project List_Consolidated draft with AQ (ORIGINAL).xlsx'
xl = pd.ExcelFile(excel)
sheetList = xl.sheet_names
# update the sheet list
sheetList = [sheet for sheet in sheetList if sheet not in ['Transit Constrained', 'Transit Illustrative', 'Table Data']]
path = r'T:\MPO\RTP\FY20 2045 Update\Data and Resources\ProjectReview'

def reviewIDinGIS(layer= 'Constrained_Roadway_lines', IDs=[924, 333]):
    gdf = gpd.read_file(r'T:\MPO\RTP\FY16 2040 Update\Data\RTP_2040_Data.gdb', layer=layer)
    return gdf[gdf.RTP_ID.isin(IDs)]

# get information for ID review
def reviewIDforGIS(year=2040, export=False):
    df = pd.read_csv(os.path.join(path, str(year)+'repeatedRTPID.csv'))
    df['Review'] = df[['Table1', 'Table2']].apply(lambda row: review(row.Table1, row.Table2)[0], axis = 1)
    df['In'] = df[['Table1', 'Table2']].apply(lambda row: review(row.Table1, row.Table2)[1], axis = 1)
    if export:
        df.to_csv(os.path.join(path, str(year)+'repeatedRTPID.csv'), index=False)
    return df[df.Review == 'yes']

# review the repeatedly-used ID in the different spreadsheets
# modified version of the function combineTables
def reviewRepeatedIDs(year=2040, excludeTransit = False):
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
        if sheetName == sheetNames[0]:
            df = modifyRTP(readTable(sheetName=sheetName, year=year))
            RTPlist = list(df.RTP.unique())
            allrepeatedIDs = []
            alllistIDs = []
        else:
            ndf = modifyRTP(readTable(sheetName=sheetName, year=year))
            if ndf.shape[0] == 0:
                pass
            else:
                nRTPlist = list(ndf.RTP.unique())
                repeatedIDs = [ID for ID in nRTPlist if ID in RTPlist]
                if len(repeatedIDs) > 0:
                    tables = sheetNames[0:sheetNames.index(sheetName)]
                    for table in tables:
                        for ID in repeatedIDs:
                            odf = modifyRTP(readTable(sheetName=table, year=year))
                            oRTPlist = list(odf.RTP.unique())
                            if ID in oRTPlist:
                                listIDs = [ID, sheetName, table]
                                alllistIDs.append(listIDs)
                                print("ID {0}: {1}, {2}".format(ID, sheetName, table))                 
                RTPlist.extend(nRTPlist)
                allrepeatedIDs.extend(repeatedIDs)
            df = pd.DataFrame(alllistIDs, columns=['RTP_ID', 'Table1', 'Table2'])
            df.to_csv(os.path.join(path, str(year)+'repeatedRTPID.csv'), index=False)
    return RTPlist, allrepeatedIDs, df

def review(string1, string2):
    if string1.split("-")[0] == string2.split("-")[0]:
        res = "yes"
    else:
        res = "no"
    return res, string1.split("-")[0]

# for the shapefile column name length limit 10
def shortenColnames(df):
    df.rename(columns={'AirQualityStatus': 'AirQuaSta',
                      'Description': 'Narration',
                      'EstimatedCost': 'RoughCost',
                      'EstimatedYearofConstruction': 'YearRange',
                      'FunctionalClass': 'FunctClass',
                      'GeographicLimits': 'GeoLimits',
                      'JurisdictionalProject#': 'JurisProjN',
                      'PrimaryJurisdiction': 'PrimJurisd',
                      'YearofConstructionCostMax': 'CostMax', 
                      'YearofConstructionCostMin': 'CostMin',
                      'RTP': 'RTP_ID'}, inplace = True)

# get combined tables 
def getCombinedTables(cat='added', export=False, byCategory=False, category='AutoConstrained'):
    if cat == 'added':
        filePaths = glob.glob(os.path.join(path, '*45.csv'))
        # the last file is project_2045.csv
        filePaths.pop()
        data = combineProjectReviewTable(filePaths)
        data.columns = data.columns.str.replace('45', '')    
    elif cat == 'common':
        if byCategory:
            filePaths = glob.glob(os.path.join(path, category+'*.csv'))
            exclude = re.compile(r'.*[0-9]{2}.csv')
            filePaths = [f for f in filePaths if not exclude.match(f)]
        else:
            allfilePaths = glob.glob(os.path.join(path, '*.csv'))
            filePaths = [os.path.join(path, sheetName.replace(' ', '') + '.csv') for sheetName in sheetList if os.path.join(path, sheetName.replace(' ', '') + '.csv') in allfilePaths]
        df = combineProjectReviewTable(filePaths)
        sel = df.columns.map(lambda x: bool(re.search('45',x)))
        cols = list(df.columns[sel].values)
        cols.append('RTP')
        data = df[cols]
        # another way to select columns with certain string pattern: 
        # df[df.columns[df.columns.to_series().str.contains('45')]].head()
        data.columns = data.columns.str.replace('45', '')
    elif cat == 'missing':
        filePaths = glob.glob(os.path.join(path, '*40.csv'))
        # the last file is project_2045.csv
        filePaths.pop()
        data = combineProjectReviewTable(filePaths)
        data.columns = data.columns.str.replace('40', '') 
    if export:
        if byCategory:
            data.to_csv(os.path.join(path, cat + category + 'Projects.csv'), index=False)
        else:
            data.to_csv(os.path.join(path, cat + 'Projects.csv'), index=False)
    if cat == 'common':
        return df, data
    else:
        return data
    
# combine tables from the project review step
def combineProjectReviewTable(filePaths):
    for filePath in filePaths:
        if filePath == filePaths[0]:
            df = pd.read_csv(filePath)
            df['In'] = np.repeat(filePath.split('\\')[-1].split('-')[0], df.shape[0])
        else:
            ndf = pd.read_csv(filePath)
            ndf['In'] = np.repeat(filePath.split('\\')[-1].split('-')[0], ndf.shape[0])
            if 'RTP' in ndf.columns:
                selectedColumns = [a for a in list(ndf.columns) if a in list(df.columns)]
                ndf = ndf[selectedColumns]
                df = df[selectedColumns]
                df = df.append(ndf, ignore_index=True)
    return df
                              
# review RTP projects in all spreadsheets in a loop
def projectReviebyTable(sheetNames):
    outpath = r'T:\MPO\RTP\FY20 2045 Update\Data and Resources\ProjectReview'    
    sheetComplete=[]
    sheetEmpty=[]
    sheet2Review=[]
    for sheetName in sheetNames:
            res = checkDiffbyTable(sheetName=sheetName, export=True)
            if isinstance(res, pd.DataFrame):
                sheet2Review.append(sheetName)        
            elif res == 0:
                sheetEmpty.append(sheetName)              
            else:
                sheetComplete.append(sheetName)
    with open(os.path.join(outpath, "review_by_table.txt"), 'a') as f:
        print("\n", file=f)
        print("Need to review these tables:", file=f)
        print(sheet2Review, file=f)
        print("\n", file=f)
        print("These tables are empty:", file=f)
        print(sheetEmpty, file=f)
        print("\n", file=f)
        print("These tables are complete:", file=f)
        print(sheetComplete, file=f)

# review RTP project in each spreadsheet between the tables 2040 and 2045
def checkDiffbyTable(sheetName='Auto Constrained - Arterial Lin', export=False):
    outpath = r'T:\MPO\RTP\FY20 2045 Update\Data and Resources\ProjectReview'
    df40r = readTable(sheetName=sheetName)
    df45r = readTable(sheetName=sheetName, year=2045)
    file = os.path.join(outpath, "review_by_table.txt")
    with open(file, 'a') as f:
        print("\n", file=f)
        print(sheetName, file=f)
        print("Dimension in 2040 data:", file=f)
        print(df40r.shape, file=f)
        print("Dimension in 2045 data:", file=f)
        print(df45r.shape, file=f)
        if df40r.shape[0] != 0 and df45r.shape[0] != 0:
            keepcols = [col for col in df40r.columns if col in df45r.columns]
            df40 = modifyRTP(df40r[keepcols])
            df45 = modifyRTP(df45r[keepcols])
            RTPex40 = len(df40r.RTP.unique()) - len(df40.RTP.unique())
            RTPex45 = len(df45r.RTP.unique()) - len(df45.RTP.unique())

            print("In 2040, there is {0} RTP in {1} items excluded in the match; In 2045, there is {2} RTP in {3} items excluded in the match.".format(RTPex40, df40r.shape[0] - df40.shape[0], RTPex45, df45r.shape[0] - df45.shape[0]), file=f)
            
            df40.columns = df40.columns + '40'
            df40.rename(columns={"RTP40": "RTP"}, inplace = True)
            df45.columns = df45.columns + '45'
            df45.rename(columns={"RTP45": "RTP"}, inplace = True)
            df40.drop_duplicates(subset='RTP', keep=False, inplace=True)
            df45.drop_duplicates(subset='RTP', keep=False, inplace=True)
            data = df40.merge(df45, on='RTP')
            keepcols.remove('RTP')
            if data.shape[0] != 0:
                for col in keepcols:
                    data[col+'Diff'] = data[[col+'40', col+'45']].apply(lambda row: compareDiff(row[col+'40'], row[col+'45']), axis = 1)
                data = data.reindex(sorted(data.columns), axis=1)
                if export:
                    outname = sheetName.replace(' ', '')                                                                                                                                      
                    data.to_csv(os.path.join(outpath, outname + '.csv'), index=False)
                if 'GeographicLimitsDiff' in data.columns:
                    print("Changes in geographic limits:", file=f)
                    print(data['GeographicLimitsDiff'].value_counts(), file=f)

                if 'LengthDiff' in data.columns:
                    print("Changes in length:", file=f)
                    print(data['LengthDiff'].value_counts(), file=f)

                print("Data include:", file=f)                
                print(data.columns, file=f)
                print(data[['RTP', 'Name40', 'Name45']].head(), file=f)
                if data.shape[0] == df40r.shape[0] == df45r.shape[0]:
                    res = 'ALL'
                    return data, res
                else:
                    if len([a for a in list(df40.RTP.unique()) if a not in list(data.RTP.unique())]) > 0:
                        df40[~df40.RTP.isin(list(data.RTP.unique()))].to_csv(os.path.join(outpath, outname + '40.csv'), index=False)
                    
                    if len([a for a in list(df45.RTP.unique()) if a not in list(data.RTP.unique())]) > 0:
                        df45[~df45.RTP.isin(list(data.RTP.unique()))].to_csv(os.path.join(outpath, outname + '45.csv'), index=False)
                    return data
        else:
            print("At least one of the two tables is empty or there is no match!", file=f)
            return 0

# review the differences in multiple columns before and after changes over years with all spreadsheets included
def checkDiff(export=True, excludeTransit = False, by="ID"):
    outpath = r'T:\MPO\RTP\FY20 2045 Update\Data and Resources\ProjectReview'
    if excludeTransit:
        df = modifyRTP(combineTables(excludeTransit = True))
        df45 = modifyRTP(combineTables(year=2045, excludeTransit = True))
        if export:
            df.to_csv(os.path.join(outpath, 'project_2040_excludeTransit.csv'), index=False)
            df45.to_csv(os.path.join(outpath, 'project_2045_excludeTransit.csv'), index=False)
    else:
        df = modifyRTP(combineTables())
        df45 = modifyRTP(combineTables(year=2045))
        if export:
            df.to_csv(os.path.join(outpath, 'project_2040.csv'), index=False)
            df45.to_csv(os.path.join(outpath, 'project_2045.csv'), index=False)
    
    if by == "ID":
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
    else:
        df = df[df.columns.drop(["EstimatedCost", "YearofConstructionCostMin", "YearofConstructionCostMax"])]
        df45 = df45[df45.columns.drop(["EstimatedCost", "YearofConstructionCostMin", "YearofConstructionCostMax"])]
        cols = [col for col in list(df.columns) if (col in list(df45.columns)) and (col != 'RTP')]
        df.columns = df.columns + '40'
        df.rename(columns={"RTP40": "RTP"}, inplace = True)
        df45.columns = df45.columns + '45'
        df45.rename(columns={"RTP45": "RTP"}, inplace = True)
        df.drop_duplicates(subset='RTP', keep=False, inplace=True)
        df45.drop_duplicates(subset='RTP', keep=False, inplace=True)
        data = df.merge(df45, on='RTP')
        for col in cols:
            data[col+'Diff'] = data[[col+'40', col+'45']].apply(lambda row: compareDiff(row[col+'40'], row[col+'45']), axis = 1)
        if export:
            data.to_csv(os.path.join(outpath, 'project_review_RTP.csv'), index=False)
        
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

# clean RTP format
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