import geopandas as gpd
import os

path = r'T:\MPO\RTP\FY20 2045 Update\Data and Resources\Data\GISData\Updated'
datapath = r'T:\MPO\RTP\FY20 2045 Update\Data and Resources\Data\ForAppendixF'

def RTP_counted_by_intersection(shapefile='Roadway_lines',
                                folder='Historic',
                                file='NationalRegisterHistoricSitesCLMPO.shp',
                                transit=False, ftn=False):
    if transit:
        rtp = gpd.read_file(os.path.join(datapath, 'RTP', shapefile+'.shp'))
    else:
        rtp = gpd.read_file(os.path.join(path, 'Constrained_'+shapefile+'.shp'))
    # 100 feet buffer
    rtp['buffered'] = rtp.buffer(100)
    rtp = rtp.set_geometry('buffered')
    rtp = rtp.to_crs(epsg=3857)
    env = gpd.read_file(os.path.join(datapath, folder, file))
    joined = gpd.tools.sjoin(rtp, env, how="inner")
    if transit:
        if ftn:
            joined = joined.drop_duplicates(subset=['route', 'geometry'])
            res = joined[['route', 'geometry']].groupby(['route']).agg('count')
        else:
            joined = joined.drop_duplicates(subset=['name_left', 'geometry'])
            res = joined[['name_left', 'geometry']].groupby(['name_left']).agg('count')
    else:
        joined = joined.drop_duplicates(subset=['RTP_ID', 'geometry'])
        res = joined[['Category', 'geometry']].groupby(['Category']).agg('count')
    return res