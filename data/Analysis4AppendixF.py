import geopandas as gpd
import os
import pandas as pd
import numpy as np

path = r'T:\MPO\RTP\FY20 2045 Update\Data and Resources\Data\GISData\Updated'
datapath = r'T:\MPO\RTP\FY20 2045 Update\Data and Resources\Data\ForAppendixF'

categories = ['Auto']*7 + ['Transit']*2 + ['Bike/Ped']*4

project_types = ['Added Freeway Lanes or Major Interchange Improvements',
                 'Arterial Capacity Improvements',
                 'New Arterial Link or Interchange',
                 'New Collectors',
                 'Study',
                 'Transit Oriented Development Implementation',
                 'Urban Standards',
                 'Frequent Transit Network',
                 'Stations',
                 'Multi-Use Paths Without Road Project',
                 'Multi-Use Paths With Road Project',
                 'On-Street Lanes or Routes With Road Project',
                 'On-Street Lanes or Routes Without Road Project']

varcats = ['EJ', 'Cultural Resources', 'Air Quality', 'Water Quality', 
           'Sensitive Habitat', 'Hazard Mitigation', 'MPO Area']
folders = ['EJ', 'Historic', 'AirQuality', 'WaterQuality', 
           'SensitiveHabitats', 'NaturalHazards', 'RTP']
filelist = [['equity_area.shp'], 
           ['NationalRegisterHistoricDistrictsCLMPO.shp',
            'NationalRegisterHistoricSitesCLMPO.shp'], 
           ['AirQualityMaintenanceArea.shp'],
           ['DEQ303dListedStreams.shp', 
            'SWV_GWMA.shp',
            'NavigableRivers.shp',
            'wetlandsCLMPO.shp'],
           ['ODFW_COAs_CLMPO.shp',
            'CRITHAB_CLMPO.shp'],
           ['Flood100yearCLMPO.shp',
            'EarthquakeLayer.shp'],
           ['MPO_Boundary.shp']]

keywordlist = [['equity'],
               ['HistoricDistricts', 'HistoricSites'],
               ['DEQ', 'SWV', 'Rivers', 'wetlands'],
               ['ODFW', 'CRITHAB'],
               ['Flood', 'Earthquake']]
varnmlist = [['Communities of Concern'],
             ['Historic Districts', 'Historic Sites'],
             ['303d Streams', 'GWMA', 'Navigable Rivers', 'Wetlands'],
             ['Conservation Opportunity Areas', 'USFWS Critical Habitat'],
             ['FEMA Flood Hazard', 'Seismic Zones']]
n = [0, 1, 3, 4, 5]
outnames = ['Communities_of_Concern', 'Cultural_Resources', 'Water_Quality',
            'Sensitive_Habitat', 'Hazard_Mitigation']

# total number of RTP projects is 247
tot_rtp_prj = 247

# get the summary table
def sum_RTP(export=False):
    for varcat in varcats:
        k = varcats.index(varcat)
        df = sum_RTP_for_each_env_category(varcat=varcat, folder=folders[k], files=filelist[k])
        if k==0:
            ndf = df
        else:
            ndf = pd.concat([ndf, df[[varcat]]], axis=1)
        #print(varcat)
    tdf = pd.concat([pd.DataFrame(data={'Project Category': [''], 'Project Type': ['TOTAL']}), 
                pd.DataFrame(ndf[ndf.columns[2:]].apply(np.sum, axis=0)).T], axis=1)
    pdf = pd.concat([pd.DataFrame(data={'Project Category': [''], 'Project Type': ['PERCENT OF ALL CONSTRAINED PROJECTS']}), 
                pd.DataFrame(ndf[ndf.columns[2:]].apply(lambda x: int(sum(x)/tot_rtp_prj*100+0.5), axis=0)).T], axis=1)
    ndf = pd.concat([ndf, tdf, pdf])
    #print(ndf)
    if export:
        ndf.to_csv(os.path.join(datapath, 'Tables', 'Summary.csv'), index=False)
    return ndf

# summarize the number of projects when the env factor includes multiple layers                                
def sum_RTP_for_each_env_category(varcat = 'Cultural Resources', folder = 'Historic',
                                  files = ['NationalRegisterHistoricDistrictsCLMPO.shp',
                                           'NationalRegisterHistoricSitesCLMPO.shp']):
    df = pd.DataFrame(data={'Project Category': categories, 'Project Type': project_types})
    df[varcat] = 0
    # rwdf: roadway dataframe
    rwdf = sum_RTP_by_mode(mode='roadway', folder=folder, varcat=varcat, files=files)
    if isinstance(rwdf, pd.DataFrame):
        for ind in list(rwdf.index):
            df.loc[df['Project Type'] == ind, varcat] = rwdf.loc[ind, varcat]
    # bpdf: bike/ped dataframe
    bpdf = sum_RTP_by_mode(mode='bikeped', folder=folder, varcat=varcat, files=files)
    if isinstance(bpdf, pd.DataFrame):
        for ind in list(bpdf.index):
            df.loc[df['Project Type'] == ind, varcat] = bpdf.loc[ind, varcat]
    transitdf = sum_RTP_by_mode(mode='transit', folder=folder, varcat=varcat, files=files)
    df.loc[df['Project Type'] == 'Frequent Transit Network', varcat] = transitdf.loc['Frequent Transit Network', varcat]
    df.loc[df['Project Type'] == 'Stations', varcat] = transitdf.loc['Stations', varcat]
    return df

def sum_RTP_by_mode(mode = 'roadway', folder = 'Historic',
                    varcat = 'Cultural Resources',
                    files = ['NationalRegisterHistoricDistrictsCLMPO.shp',
                             'NationalRegisterHistoricSitesCLMPO.shp']):            
    if mode == 'roadway':
        line_res = sum_RTP_by_shp(shapefile='Roadway_lines', folder=folder,
                                 varcat=varcat, files=files)
        pnt_res = sum_RTP_by_shp(shapefile='Roadway_points', folder=folder,
                                 varcat=varcat, files=files)
    elif mode == 'bikeped':
        line_res = sum_RTP_by_shp(shapefile='BikePed', folder=folder,
                                 varcat=varcat, files=files)
        pnt_res = sum_RTP_by_shp(shapefile='BikePed_points', folder=folder,
                                 varcat=varcat, files=files)
    elif mode == 'transit':
        ftn = []
        sta = []
        for file in files:
            ftndf = RTP_counted_by_intersection(shapefile='FrequentTransitNetwork', 
                                        folder=folder, file=file,
                                        transit=True, ftn=True)
            stadf = RTP_counted_by_intersection(shapefile='stations',
                                        folder=folder, file=file, transit=True)
            ftn+=list(ftndf.index)
            sta+=list(stadf.index)
        df = pd.DataFrame(data={varcat: [len(unique(ftn)), len(unique(sta))]})
        df.index = ['Frequent Transit Network', 'Stations']
    
    if mode == 'transit':
        res = df
    else:        
        if isinstance(line_res, pd.DataFrame) and isinstance(pnt_res, pd.DataFrame):
            for ind in list(pnt_res.index):
                line_res.loc[ind, varcat] = line_res.loc[ind, varcat] + pnt_res.loc[ind, varcat]
            res = line_res
        else:
            if isinstance(line_res, pd.DataFrame):
                res = line_res
            elif isinstance(pnt_res, pd.DataFrame):
                res = pnt_res 
            else:
                res = 0
    return res

# function to get unique values
def unique(list1):
 
    # intilize a null list
    unique_list = []
     
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return(unique_list)

def sum_RTP_by_shp(shapefile='Roadway_lines', folder = 'Historic',
                    varcat = 'Cultural Resources',
                    files = ['NationalRegisterHistoricDistrictsCLMPO.shp',
                             'NationalRegisterHistoricSitesCLMPO.shp']):
    for file in files:
        df = RTP_counted_by_intersection(shapefile=shapefile, folder=folder, 
                                         file=file, returnID=True)
        if file==files[0]:
            ndf = df
        else:
            if ndf.shape[0] == 0:
                ndf = ndf.append(df)
            else:
                if df.shape[0] != 0:
                    for ind in list(df.index):
                        if ind in list(ndf.index):
                            ndf.loc[ind, 'RTP_ID'].update(df.loc[ind, 'RTP_ID'])
                        else:
                            sdf = pd.DataFrame(df.loc[ind, :]).T
                            ndf = pd.concat([ndf, sdf])
                            
        ndf[varcat] = ndf.RTP_ID.apply(lambda x: len(x))
        if ndf.shape[0] == 0:
            res = 0
        else:
            res = ndf[[varcat]]
    return res         

# print the tables by env category, by ID or geometry
# require the summary table for the total number of RTP project in CLMPO
def combine_RTP(export=False, by='ID'):
    for outname in outnames:
        l = outnames.index(outname)
        df = combine_RTP_for_each_env_category(keywords = keywordlist[l],
                                               varnms = varnmlist[l],
                                               folder = folders[n[l]],
                                               files = filelist[n[l]],
                                               by=by)
        tdf = pd.concat([pd.DataFrame(data={'Project Category': [''], 'Project Type': ['TOTAL']}), 
                pd.DataFrame(df[varnmlist[l]].apply(np.sum, axis=0)).T], axis=1)
        pdf = pd.concat([pd.DataFrame(data={'Project Category': [''], 'Project Type': ['PERCENT OF ALL CONSTRAINED PROJECTS']}), 
                pd.DataFrame(df[varnmlist[l]].apply(lambda x: int(sum(x)/tot_rtp_prj*100+0.5), axis=0)).T], axis=1)
        ndf = pd.concat([df, tdf, pdf])
        print(ndf)
        if export:
            ndf.to_csv(os.path.join(datapath, 'Tables', outname + '.csv'), index=False)

# combine the same environmental category, by ID or geometry
def combine_RTP_for_each_env_category(keywords = ['HistoricDistricts', 'HistoricSites'],
                                      varnms = ['Historic Districts', 'Historic Sites'],
                                      folder = 'Historic',
                                      files = ['NationalRegisterHistoricDistrictsCLMPO.shp',
                                               'NationalRegisterHistoricSitesCLMPO.shp'],
                                      by='ID'):
    for keyword in keywords:
        k = keywords.index(keyword)
        varnm = varnms[k]
        df = combine_RTP_for_each_env_factor(keyword = keyword,
                                             varnm = varnm,
                                             folder = folder,
                                             file = files[k], 
                                             by=by)
        if keyword == keywords[0]:
            ndf = df
        else:
            ndf = pd.concat([ndf, df[[varnm]]], axis=1)
    
    return ndf

# combine the same environmental factor, by ID or geometry
def combine_RTP_for_each_env_factor(keyword = 'HistoricSites',
                                    varnm = 'Historic Sites',
                                    folder='Historic',
                                    file='NationalRegisterHistoricSitesCLMPO.shp',
                                    by='ID'):
    df = pd.DataFrame(data={'Project Category': categories, 'Project Type': project_types})
    if keyword in file:
        var = varnm
    df[var] = 0
    # rwdf: roadway dataframe
    rwdf = combine_RTP_by_mode(mode='roadway', folder=folder, file=file, by=by)
    if rwdf.shape[0] != 0:
        for ind in list(rwdf.index):
            df.loc[df['Project Type'] == ind, var] = rwdf.loc[ind, by]
    # bpdf: bike/ped dataframe
    bpdf = combine_RTP_by_mode(mode='bikeped', folder=folder, file=file, by=by)
    if bpdf.shape[0] != 0:
        for ind in list(bpdf.index):
            df.loc[df['Project Type'] == ind, var] = bpdf.loc[ind, by]
    # ftndf: frequent transit network dataframe
    ftndf = RTP_counted_by_intersection(shapefile='FrequentTransitNetwork', 
                                        folder=folder, file=file,
                                        transit=True, ftn=True)
    df.loc[df['Project Type'] == 'Frequent Transit Network', var] = ftndf.shape[0]
    # stadf: stations dataframe
    stadf = RTP_counted_by_intersection(shapefile='stations',
                                        folder=folder, file=file, transit=True)
    df.loc[df['Project Type'] == 'Stations', var] = stadf.shape[0]
    return df

# combine the same RTP project categories by roadway or bike/ped, based on ID or geometry
def combine_RTP_by_mode(mode='roadway', folder='Historic',
                        file='NationalRegisterHistoricSitesCLMPO.shp',
                        by='ID'):
    if by == 'ID':
        if mode == 'roadway':
            df1=RTP_counted_by_intersection(shapefile='Roadway_lines', folder=folder, file=file, returnID=True)
            df2=RTP_counted_by_intersection(shapefile='Roadway_points', folder=folder, file=file, returnID=True)
        elif mode == 'bikeped':
            df1=RTP_counted_by_intersection(shapefile='BikePed', folder=folder, file=file, returnID=True)
            df2=RTP_counted_by_intersection(shapefile='BikePed_points', folder=folder, file=file, returnID=True)
        
        if df1.shape[0] == 0:
            if df2.shape[0] == 0:
                res = df1
            else:
                res = df1.append(df2)
        else:    
            if df2.shape[0] != 0:
                for ind in list(df2.index):
                    df1.loc[ind,'RTP_ID'].update(df2.loc[ind, 'RTP_ID'])
            res = df1
        if isinstance(res, pd.DataFrame):
            res[by] = res.RTP_ID.apply(lambda x: len(x))
            res = res[[by]]     
    else:
        if mode == 'roadway':
            df1=RTP_counted_by_intersection(shapefile='Roadway_lines', folder=folder, file=file)
            df2=RTP_counted_by_intersection(shapefile='Roadway_points', folder=folder, file=file)
        elif mode == 'bikeped':
            df1=RTP_counted_by_intersection(shapefile='BikePed', folder=folder, file=file)
            df2=RTP_counted_by_intersection(shapefile='BikePed_points', folder=folder, file=file)
        
        if df1.shape[0] == 0:
            if df2.shape[0] == 0:
                res = df1
            else:
                res = df1.append(df2)
        else:    
            if df2.shape[0] != 0:
                for ind in list(df2.index):
                    df1.loc[ind, 'geometry'] = df1.loc[ind, 'geometry'] + df2.loc[ind, 'geometry']
            res = df1
    return res

# the results should be the same as the output from Select by Location in ArcGIS Pro
def RTP_counted_by_intersection(shapefile='Roadway_lines',
                                folder='Historic',
                                file='NationalRegisterHistoricSitesCLMPO.shp',
                                transit=False, ftn=False, returnID=False):
    if transit:
        rtp = gpd.read_file(os.path.join(datapath, 'RTP', shapefile+'.shp'))
    else:
        rtp = gpd.read_file(os.path.join(path, 'Constrained_'+shapefile+'.shp'))
    # 100 feet buffer
    rtp['buffered'] = rtp.buffer(100)
    rtp = rtp.set_geometry('buffered')
    rtp = rtp.to_crs(epsg=3857)
    env = gpd.read_file(os.path.join(datapath, folder, file))
    if env.crs != 'EPSG:3857':
        env = env.to_crs(epsg=3857)
    joined = gpd.tools.sjoin(rtp, env, how="inner")
    if transit:
        if ftn:
            joined = joined.drop_duplicates(subset=['route', 'geometry'])
            res = joined[['route', 'geometry']].groupby(['route']).agg('count')
        elif 'name_left' in joined.columns:
            joined = joined.drop_duplicates(subset=['name_left', 'geometry'])
            res = joined[['name_left', 'geometry']].groupby(['name_left']).agg('count')
        else:
            joined = joined.drop_duplicates(subset=['name', 'geometry'])
            res = joined[['name', 'geometry']].groupby(['name']).agg('count')
    else:
        joined = joined.drop_duplicates(subset=['RTP_ID', 'geometry'])
        if returnID:
            res = joined[['Category', 'RTP_ID']].groupby(['Category']).agg(lambda x: set(x))
        else:
            res = joined[['Category', 'geometry']].groupby(['Category']).agg('count')
    return res