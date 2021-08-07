import geopandas as gpd
import os

path = r'T:\MPO\RTP\FY20 2045 Update\Data and Resources\Data\GISData\Updated'
datapath = r'T:\MPO\RTP\FY20 2045 Update\Data and Resources\Data\ForAppendixF'

def RTP_counted_by_intersection(shapefile='Roadway_lines',
                                folder='Historic',
                                file='NationalRegisterHistoricSitesCLMPO.shp',
                                transit=False):
    rtp = gpd.read_file(os.path.join(path, 'Constrained_'+shapefile+'.shp'))
    # 100 feet buffer
    rtp['buffered'] = rtp.buffer(100)
    rtp = rtp.set_geometry('buffered')
    rtp = rtp.to_crs(epsg=3857)
    env = gpd.read_file(os.path.join(datapath, folder, file))
    joined = gpd.tools.sjoin(rtp, env, how="inner")
    if transit:
        res = joined.shape[0]
    else:
        joined = joined.drop_duplicates(subset=['RTP_ID', 'geometry'])
        res = joined[['Category', 'geometry']].groupby(['Category']).agg('count')
    return res