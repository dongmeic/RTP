import geopandas as gpd
import os
import pandas as pd

path = r'T:\MPO\RTP\FY20 2045 Update\Data and Resources\Data\GISData\Updated'
datapath = r'T:\MPO\RTP\FY20 2045 Update\Data and Resources\Data\ForAppendixF'

categories = ['Auto']*7 + ['Transit']*2 + ['Bike/Ped']*4

project_types = ['Added Freeway Lanes or Major Interchange Improvements',
                 'Arterial Capacity Improvements',
                 'New Arterial Link or Interchange',
                 'New Collectors',
                 'Transit Oriented Development Implementation',
                 'Study',
                 'Urban Standards',
                 'Frequent Transit Network',
                 'Stations',
                 'Multi-Use Paths Without Road Project',
                 'Multi-Use Paths With Road Project',
                 'On-Street Lanes or Routes With Road Project',
                 'On-Street Lanes or Routes Without Road Project']

# combine the same environmental factor
def combine_RTP_for_each_env_factor(folder='Historic',
                                    file='NationalRegisterHistoricSitesCLMPO.shp'):
    df = pd.DataFrame(data={'Project Category': categories, 'Project Type': project_types})
    if 'HistoricSites' in file:
        var = 'Historic Sites'
    df[var] = 0
    # rwdf: roadway dataframe
    rwdf = combine_RTP_by_mode(mode='roadway', folder=folder, file=file)
    if rwdf.shape[0] != 0:
        for ind in list(rwdf.index):
            df.loc[df['Project Type'] == ind, var] = rwdf.loc[ind, 'geometry']
    # bpdf: bike/ped dataframe
    bpdf = combine_RTP_by_mode(mode='bikeped', folder=folder, file=file)
    if bpdf.shape[0] != 0:
        for ind in list(bpdf.index):
            df.loc[df['Project Type'] == ind, var] = bpdf.loc[ind, 'geometry']
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

# combine the same RTP project categories by roadway or bike/ped
def combine_RTP_by_mode(mode='roadway', folder='Historic',
                                file='NationalRegisterHistoricSitesCLMPO.shp'):
    if mode == 'roadway':
        df1=RTP_counted_by_intersection(shapefile='Roadway_lines', folder=folder, file=file)
        df2=RTP_counted_by_intersection(shapefile='Roadway_points', folder=folder, file=file)
    elif mode == 'bikeped':
        df1=RTP_counted_by_intersection(shapefile='BikePed', folder=folder, file=file)
        df2=RTP_counted_by_intersection(shapefile='BikePed_points', folder=folder, file=file)
        
    if df2.shape[0] != 0:
        for ind in list(df2.index):
            df1.loc[ind, 'geometry'] = df1.loc[ind, 'geometry'] + df2.loc[ind, 'geometry']
    return df1

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