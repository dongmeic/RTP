import geopandas as gpd
import os
import pandas as pd
import numpy as np

pd.options.mode.chained_assignment = None

path = r'T:\MPO\RTP\FY20 2045 Update\Data and Resources\Data\Centerline_Network.gdb'
outpath = r'T:\MPO\RTP\FY20 2045 Update\Data and Resources\Data\QC_road_ownership'

# update data to match with city streets
# a revision and simplified version from reviewCommonIDs: change the owner info in the regional data 
# if it is different from the local data
def updateRoadOwnership(RLIDlayer='CenterlinesUpdated', ugb='EUG', export=False, commonIDonly=True, second=False, first='EUG'):
    # run after the first update using a different input
    # commonIDonly should run first
    if second:
        CLstreets = gpd.read_file(os.path.join(outpath, "{0}_{1}.shp".format(RLIDlayer, first)))
        CLstreets.rename(columns={'sponsor': 'contributor', 'road_segid': 'road_segment_gfid', 'ShpLength': 'Shape_Length'}, inplace=True)
    else:
        CLstreets = gpd.read_file(path, layer=RLIDlayer)
    
    if ugb == 'EUG':
        IDcol = 'EUGID'
        CLIDcol = 'eugid'
        Citystreets = gpd.read_file(path, layer=ugb + '_Streets')
    else:
        IDcol = 'COMPKEY'
        CLIDcol = 'sprid'
        Citystreets = adjustSPRownerName()
        
    Citystreets[IDcol] = Citystreets[Citystreets[IDcol].astype(str) != 'nan'][IDcol].astype(int)
    if commonIDonly:
        CLstreets[CLIDcol] = CLstreets[CLstreets[CLIDcol].astype(str) != 'nan'][CLIDcol].astype(int)
    else:
        if first=='EUG_SPR':
            CLstreets[CLIDcol] = CLstreets[CLstreets[CLIDcol].astype(str) != 'None'][CLIDcol].astype(int)
        else:
            CLstreets[CLIDcol] = CLstreets[CLstreets[CLIDcol].astype(str) != 'nan'][CLIDcol].astype(int)
    
    comIDs = [ID for ID in Citystreets[IDcol].unique() if ID in CLstreets[CLIDcol].unique()]
    
    if ugb == 'SPR':
        Citystreets.rename(columns={IDcol:CLIDcol}, inplace=True)
        
    cols = [var.lower() for var in list(Citystreets.columns)[:len(list(Citystreets.columns))-2]] + ['Shape_Length', 'geometry']
    Citystreets.columns = cols
    Citystreets.drop_duplicates(inplace=True, ignore_index=True)
    CLstreets.drop_duplicates(inplace=True, ignore_index=True)
    Citystreets.drop_duplicates(subset='geometry', keep='last', inplace=True, ignore_index=True)
    CLstreets.drop_duplicates(subset='geometry', keep='last', inplace=True, ignore_index=True)
    
    if commonIDonly:
        for ID in comIDs:
            cityOwners = list(Citystreets[Citystreets[CLIDcol] == ID].owner.values)
            CLowners = list(CLstreets[CLstreets[CLIDcol] == ID].owner.values)
            if len(cityOwners)==1:
                if any([val not in cityOwners for val in CLowners]):
                    CLstreets.loc[CLstreets[CLIDcol] == ID, 'owner'] = cityOwners[0]
            else:
                if any([val not in CLowners for val in cityOwners]):
                    # common columns between the regional and local datasets
                    cols1 = [x for x in cols if x in list(CLstreets.columns)]
                    # columns that are not in the local datasets
                    cols2 = [x for x in list(CLstreets.columns) if x not in cols]
                    # repeat the same values for the columns that are not in the local dataset
                    df2 = CLstreets[CLstreets[CLIDcol] == ID][cols2]
                    newdf = pd.DataFrame(np.repeat(df2.values,len(cityOwners),axis=0))
                    newdf.columns = df2.columns
                    df1 = Citystreets[Citystreets[CLIDcol] == ID][cols1]
                    # combine the columns
                    ndf = pd.concat([newdf.reset_index(drop=True), df1.reset_index(drop=True)], axis=1)
                    # drop the row(s) in the regional dataset and add rows from the local dataset when ownership is different with 
                    # a different number of features
                    CLstreets = CLstreets[~(CLstreets[CLIDcol] == ID)].append(ndf[list(CLstreets.columns)], ignore_index=True)
    else:       
        Citystreets = Citystreets.to_crs(epsg = 2914)
        
        # some common ids are broken down into different ids
        #CLstreets1 = CLstreets[CLstreets[CLIDcol].isin(comIDs)]
        #CLstreets = CLstreets[~CLstreets[CLIDcol].isin(comIDs)]  
        #Citystreets = Citystreets[~Citystreets[CLIDcol].isin(comIDs)]
        
        for ind in CLstreets.index:
            cnty_length = CLstreets[CLstreets.index==ind].Shape_Length.values[0]
            cnty_bound = CLstreets[CLstreets.index==ind].geometry.values.bounds
            city_length = Citystreets.Shape_Length.values
            # set the length precision as 0.001, need to be as small as possible to have only one match
            length_diff = abs(cnty_length - city_length) <= 0.001
            if sum(length_diff)==1:
                i = abs(Citystreets.Shape_Length-cnty_length) <= 0.001
                city_bound = Citystreets[i].geometry.values.bounds
                cnty_val = CLstreets[CLstreets.index==ind].owner.values[0]
                city_val1 = Citystreets[i].owner.values[0]
                city_val2 = Citystreets[i].maint.values[0]
                # set the boundary precision as 1
                bound_diff = abs(city_bound - cnty_bound) <= 1
                if bound_diff.all() & (cnty_val != city_val1):
                    CLstreets.loc[ind, 'owner'] = city_val1
                    CLstreets.loc[ind, 'maint'] = city_val2
       
    #CLstreets = CLstreets1.append(CLstreets, ignore_index=True) 
        
    if export:
        CLstreets.rename(columns={'contributor': 'sponsor', 'road_segment_gfid': 'road_segid', 'Shape_Length': 'ShpLength'}, inplace=True)
        if second:
            CLstreets.to_file(os.path.join(outpath, "{0}_{1}_{2}.shp".format(RLIDlayer, first, ugb)))
        else:
            CLstreets.to_file(os.path.join(outpath, "{0}_{1}.shp".format(RLIDlayer, ugb)))
        
    return CLstreets

# review common IDs
def reviewCommonIDs(ugb='EUG', export=False, commonIDonly=False, update=False):
    if update:
        CLstreets = gpd.read_file(path, layer='CenterlinesUpdated')
        outfile = os.path.join(outpath, "reviewCommonIDs"+ugb+"Updated.txt")
        CityShp = "_diff_from_CL_commonIDsUpdated.shp"
        LCshp = "CL_diff_from_{0}_commonIDsUpdated.shp".format(ugb)
        CityShpDiff = "_diff_from_CL_updated.shp"
        LCshpDiff = "CL_diff_from_{0}_updated.shp".format(ugb)
    else:
        CLstreets = gpd.read_file(path, layer='Centerlines')
        outfile = os.path.join(outpath, "reviewCommonIDs"+ugb+".txt")
        CityShp = "_diff_from_CL_commonIDs.shp"
        LCshp = "CL_diff_from_{0}_commonIDs.shp".format(ugb)
        CityShpDiff = "_diff_from_CL.shp"
        LCshpDiff = "CL_diff_from_{0}.shp".format(ugb)
    
    CLstreets = CLstreets[CLstreets.ugbcity==ugb]
    
    if ugb == 'EUG':
        IDcol = 'EUGID'
        CLIDcol = 'eugid'
        cols = ['OWNER', 'NAME', 'TYPE', 'AIRSNAME', 'FCLASS']
        Citystreets = gpd.read_file(path, layer=ugb + '_Streets')
    else:
        IDcol = 'COMPKEY'
        CLIDcol = 'sprid'
        cols = ['OWNER', 'RLIDNAME', 'FCLASS']
        Citystreets = adjustSPRownerName()
    CLcols = ['owner', 'name', 'type', 'rlidname', 'fclass']
    Citystreets[IDcol] = Citystreets[Citystreets[IDcol].astype(str) != 'nan'][IDcol].astype(int)
    CLstreets[CLIDcol] = CLstreets[CLstreets[CLIDcol].astype(str) != 'nan'][CLIDcol].astype(int)
    comIDs = [ID for ID in Citystreets[IDcol].unique() if ID in CLstreets[CLIDcol].unique()]
    sameOwners = []
    diffOwners = []
    cityIDs = []
    CLIDs = []
    bothIDs = []
    
    if os.path.exists(outfile):
          os.remove(outfile)
    with open(outfile, 'a') as f:
        print("Differences between {0} and Central Lane centerlines data:".format(ugb), file=f)
        for ID in comIDs:
            if Citystreets[Citystreets[IDcol] == ID].shape[0] == 1 and CLstreets[CLstreets[CLIDcol] == ID].shape[0] == 1:
                if Citystreets[Citystreets[IDcol] == ID].OWNER.values[0] == CLstreets[CLstreets[CLIDcol] == ID].owner.values[0]:
                    sameOwners.append(ID)
                else:
                    print("For the ID {0}, the {1} city street data shows:\n".format(ID, ugb), file=f)
                    print(Citystreets[Citystreets[IDcol] == ID][[IDcol, *cols, 'Shape_Length']], file=f)
                    print("\n", file=f)
                    print("and the boundary is {0}".format(Citystreets[Citystreets[IDcol] == ID].geometry.values.bounds),file=f)
                    print("\n", file=f)
                    print("For the ID {0}, the Central Lane data shows:\n".format(ID), file=f)
                    print(CLstreets[CLstreets[CLIDcol] == ID][[CLIDcol, *CLcols, 'Shape_Length']], file=f)
                    print("\n", file=f)
                    print("and the boundary is {0}".format(CLstreets[CLstreets[CLIDcol] == ID].geometry.values.bounds),file=f)
                    print("\n", file=f)
                    diffOwners.append(ID)
            elif Citystreets[Citystreets[IDcol] == ID].shape[0] == 1 and CLstreets[CLstreets[CLIDcol] == ID].shape[0] > 1:
                CLIDs.append(ID)
                if any([val != Citystreets[Citystreets[IDcol] == ID].OWNER.values[0] for val in CLstreets[CLstreets[CLIDcol] == ID].owner.values]):
                    print("For the ID {0}, the {1} city street data shows:\n".format(ID, ugb), file=f)
                    print(Citystreets[Citystreets[IDcol] == ID][[IDcol, *cols, 'Shape_Length']], file=f)
                    print("\n", file=f)
                    print("and the boundary is {0}".format(Citystreets[Citystreets[IDcol] == ID].geometry.values.bounds),file=f)
                    print("\n", file=f)
                    print("For the ID {0}, the Central Lane data shows:\n".format(ID), file=f)
                    print(CLstreets[CLstreets[CLIDcol] == ID][[CLIDcol, *CLcols, 'Shape_Length']], file=f)
                    print("\n", file=f)
                    print("and the boundaries are", file=f)
                    for i in range(0, CLstreets[CLstreets[CLIDcol] == ID].shape[0]):
                        print(CLstreets[CLstreets[CLIDcol] == ID].geometry.values[i].bounds, file=f)
                    print("\n", file=f)
                    diffOwners.append(ID)
                else:
                    sameOwners.append(ID)
            elif Citystreets[Citystreets[IDcol] == ID].shape[0] > 1 and CLstreets[CLstreets[CLIDcol] == ID].shape[0] == 1:
                cityIDs.append(ID)
                if any([val != CLstreets[CLstreets[CLIDcol] == ID].owner.values[0] for val in Citystreets[Citystreets[IDcol] == ID].OWNER.values]):
                    print("For the ID {0}, the {1} city street data shows:\n".format(ID, ugb), file=f)
                    print(Citystreets[Citystreets[IDcol] == ID][[IDcol, *cols, 'Shape_Length']], file=f)
                    print("\n", file=f)
                    print("and the boundaries are", file=f)
                    for i in range(0, Citystreets[Citystreets[IDcol] == ID].shape[0]):
                        print(Citystreets[Citystreets[IDcol] == ID].geometry.values[i].bounds, file=f)
                    print("\n", file=f)
                    print("For the ID {0}, the Central Lane data shows:\n".format(ID), file=f)
                    print(CLstreets[CLstreets[CLIDcol] == ID][[CLIDcol, *CLcols, 'Shape_Length']], file=f)
                    print("\n", file=f)
                    print("and the boundary is {0}".format(CLstreets[CLstreets[CLIDcol] == ID].geometry.values.bounds),file=f)
                    print("\n", file=f)
                    print("and the boundaries are", file=f)
                    for i in range(0, CLstreets[CLstreets[CLIDcol] == ID].shape[0]):
                        print(CLstreets[CLstreets[CLIDcol] == ID].geometry.values[i].bounds, file=f)
                    print("\n", file=f)
                    diffOwners.append(ID)
                else:
                    sameOwners.append(ID)
            else:
                bothIDs.append(ID)
                if any([val not in Citystreets[Citystreets[IDcol] == ID].OWNER.values for val in CLstreets[CLstreets[CLIDcol] == ID].owner.values]) or any([val not in CLstreets[CLstreets[CLIDcol] == ID].owner.values for val in Citystreets[Citystreets[IDcol] == ID].OWNER.values]):
                    print("For the ID {0}, the {1} city street data shows:\n".format(ID, ugb), file=f)
                    print(Citystreets[Citystreets[IDcol] == ID][[IDcol, *cols, 'Shape_Length']], file=f)
                    print("\n", file=f)
                    print("and the boundaries are", file=f)
                    for i in range(0, Citystreets[Citystreets[IDcol] == ID].shape[0]):
                        print(Citystreets[Citystreets[IDcol] == ID].geometry.values[i].bounds, file=f)
                    print("\n", file=f)
                    print("For the ID {0}, the Central Lane data shows:\n".format(ID), file=f)
                    print(CLstreets[CLstreets[CLIDcol] == ID][[CLIDcol, *CLcols, 'Shape_Length']], file=f)
                    print("\n", file=f)
                    print("and the boundaries are", file=f)
                    for i in range(0, CLstreets[CLstreets[CLIDcol] == ID].shape[0]):
                        print(CLstreets[CLstreets[CLIDcol] == ID].geometry.values[i].bounds, file=f)
                    print("\n", file=f)
                    diffOwners.append(ID)
                else:
                    sameOwners.append(ID)
        if len(cityIDs) > 0:
            print("These IDs include more than one feature in the city street data when the Central Lane data only inclues one feaure:", file=f)
            print(cityIDs, file=f)
            print("\n", file=f)

        if len(CLIDs) > 0:
            print("These IDs include more than one feature in the Central Lane data when the city street data only inclues one feaure:", file=f)
            print(CLIDs, file=f)
            print("\n", file=f)

        if len(bothIDs) > 0:
            print("These IDs include more than one feature in both the city street data and the Central Lane data:", file=f)
            print(bothIDs, file=f)
            print("\n", file=f)
        
        print("Comparison between Central Lane (CL) and {0} street data:\n".format(ugb), file=f)
        CityDiffIDs = [ID for ID in Citystreets[IDcol].unique() if ID not in CLstreets[CLIDcol].unique()]
        CLDiffIDs = [ID for ID in CLstreets[CLIDcol].unique() if ID not in Citystreets[IDcol].unique()]
        print("There are {0} IDs in common between CL and {1}, {2} {1} IDs are not in CL and {3} CL IDs are not in {1};".format(len(comIDs), ugb, len(CityDiffIDs),len(CLDiffIDs)), file=f)
        print("In the common IDs, {0} {1} IDs and {2} CL IDs have more than one feature, and {3} IDs have one feature only in both.".format(len([ID for ID in comIDs if Citystreets[Citystreets[IDcol] == ID].shape[0] > 1]), ugb, len([ID for ID in comIDs if CLstreets[CLstreets[CLIDcol] == ID].shape[0] > 1]), len([ID for ID in comIDs if Citystreets[Citystreets[IDcol] == ID].shape[0] == 1 and CLstreets[CLstreets[CLIDcol] == ID].shape[0] == 1])), file=f)
    
    if export:
        if commonIDonly:
            Citystreets = Citystreets[Citystreets[IDcol].isin(diffOwners)][[IDcol, *cols, 'geometry']]
            CLstreets = CLstreets[CLstreets[CLIDcol].isin(diffOwners)][[CLIDcol, *CLcols, 'geometry']]
            Citystreets.to_file(os.path.join(outpath, ugb + CityShp))
            CLstreets.to_file(os.path.join(outpath, LCshp))
        else:
            Citystreets = Citystreets[Citystreets[IDcol].isin(diffOwners+CityDiffIDs)][[IDcol, *cols, 'geometry']]
            CLstreets = CLstreets[CLstreets[CLIDcol].isin(diffOwners+CLDiffIDs)][[CLIDcol, *CLcols, 'geometry']]
            Citystreets.to_file(os.path.join(outpath, ugb + CityShpDiff))
            CLstreets.to_file(os.path.join(outpath, LCshpDiff))
                                  
    return sameOwners, diffOwners, cityIDs, CLIDs, bothIDs
    
# compare the IDs and quantify the differences
def diffInIDs(update=False):
    EUGstreets = gpd.read_file(path, layer='EUG_Streets')
    SPRstreets = gpd.read_file(path, layer='SPR_Streets')
    if update:
        CLstreets = gpd.read_file(path, layer='CenterlinesUpdated') 
    else:  
        CLstreets = gpd.read_file(path, layer='Centerlines') 
        
    EUGcomIDs = [ID for ID in EUGstreets.EUGID.unique() if ID in CLstreets.eugid.unique()]
    SPRcomIDs = [ID for ID in CLstreets.sprid.unique() if ID in SPRstreets.COMPKEY.unique()]
    print("Comparison between Central Lane (CL) and Eugene (EUG) street data:\n")
    print("There are {0} IDs in common between CL and EUG, {1} EUG IDs are not in CL and {2} CL IDs are not in EUG;".format(len(EUGcomIDs), len([ID for ID in EUGstreets.EUGID.unique() if ID not in CLstreets.eugid.unique()]),len([ID for ID in CLstreets.eugid.unique() if ID not in EUGstreets.EUGID.unique()])))
    print("In the common IDs, {0} EUG IDs and {1} CL IDs have more than one feature, and {2} IDs have one feature only in both.".format(len([ID for ID in EUGcomIDs if EUGstreets[EUGstreets.EUGID == ID].shape[0] > 1]),len([ID for ID in EUGcomIDs if CLstreets[CLstreets.eugid == ID].shape[0] > 1]), len([ID for ID in EUGcomIDs if EUGstreets[EUGstreets.EUGID == ID].shape[0] == 1 and CLstreets[CLstreets.eugid == ID].shape[0] == 1])))
    print("\n")
    print("Comparison between Central Lane (CL) and Springfield (SPR) street data:\n")
    print("There are {0} IDs in common between CL and SPR, {1} SPR IDs are not in CL and {2} CL IDs are not in SPR;".format(len(SPRcomIDs), len([ID for ID in SPRstreets.COMPKEY.unique() if ID not in CLstreets.sprid.unique()]),len([ID for ID in CLstreets.sprid.unique() if ID not in SPRstreets.COMPKEY.unique()])))
    print("In the common IDs, {0} SPR IDs and {1} CL IDs have more than one feature, and {2} IDs have one feature only in both.".format(len([ID for ID in SPRcomIDs if SPRstreets[SPRstreets.COMPKEY == ID].shape[0] > 1]),len([ID for ID in SPRcomIDs if CLstreets[CLstreets.sprid == ID].shape[0] > 1]), len([ID for ID in SPRcomIDs if SPRstreets[SPRstreets.COMPKEY == ID].shape[0] == 1 and CLstreets[CLstreets.sprid == ID].shape[0] == 1])))
    
# adjust Springfield road ownership names for comparison
def adjustSPRownerName():
    SPRstreets = gpd.read_file(path, layer='SPR_Streets')
    SPRstreets.loc[SPRstreets.OWNER.isin(['LANE', 'CNTY']), 'OWNER'] = 'LCPW'
    SPRstreets.loc[SPRstreets.OWNER == 'CITY', 'OWNER'] = 'SPR'
    return SPRstreets