# Data for Environmental Analysis Maps (Appendix F) 

## Cultural and Natural Resources

### Cultural Resources -- Part of Goal 5

#### Historical Sites/Properties (point)

##### 1. Data sources

Historic districts and sites in Eugene and Springfield were collected from the city GIS teams (see *T:\MPO\RTP\FY20 2045 Update\Data and Resources\Data\ForAppendixF\Historic\ReadMe.txt*). The national register historic sites from the cities are compared with the data sets downloaded from [National Park Service (NPS)](https://mapservices.nps.gov/arcgis/rest/services/cultural_resources/nrhp_locations/MapServer) and [State Historic Preservation Offices (SHPO)](http://maps.prd.state.or.us/histsites/historicsites.html). The SHPO data or data from SHPO used by the City only includes the eligible/significant status. The historic district in Coburg remains the the same as the last RTP data (*T:\MPO\RTP\FY11 2035 Update\Environmental Coordination\Historic Properties\Historical_Districts.shp*). Historic sites in Coburg are from the SHPO data. Only national register historic sites are included in the GIS analysis for RTP due to the data uncertainty and potential irrelevance to RTP on the city/local historic sites. 

##### 2. Data paths

All the raw and editted data sets on historic sites and districts are saved on the **Cultural Resources** map in *T:\MPO\RTP\FY20 2045 Update\Maps\Appendix F\Maps4AppendixF\Maps4AppendixF.aprx*.

##### 3. Notes on the comparisons of historic sites among NPS, SHPO and city data

City of Eugene includes 155 national register historic sites and 81 local historic sites with 35 sites are both national and local. City of Springfield includes only 4 national register historic sites ('NRI' indicated in the 'nr_status' column) and 22 local historic sites using the survey data, however, the [map of Springfield historicl resources](https://www.springfield-or.gov/wp-content/uploads/2019/01/SpringfieldNationalRegisterProperties.pdf) indicates 7 national register sites. SHPO and NPS cover 113 and 60 historic sites in Eugene, 49 and 5 historic sites in Springfield, and 6 and 2 historic sites in Coburg, respectively. The numbers of national register sites are [76](http://heritagedata.prd.state.or.us/historic/index.cfm?do=v.dsp_resultList&urlString=&county=20&city=759&street=&strNbrLow=&strNbrHi=&strDir=0&twnShp=&rnge=&section=&group=0&propName=&rscType=0&eligEval=ES&constrYr1=&constrYr2=&origUse=0&style=0&archBldr=&nrListDate1=&nrListDate2=&nrCritA=false&nrCritB=false&nrCritC=false&nrCritD=false&resultType=3), [8](http://heritagedata.prd.state.or.us/historic/index.cfm?do=v.dsp_resultList&urlString=&county=20&city=1249&street=&strNbrLow=&strNbrHi=&strDir=0&twnShp=&rnge=&section=&group=0&propName=&rscType=0&eligEval=ES&constrYr1=&constrYr2=&origUse=0&style=0&archBldr=&nrListDate1=&nrListDate2=&nrCritA=false&nrCritB=false&nrCritC=false&nrCritD=false&resultType=3), and [4](http://heritagedata.prd.state.or.us/historic/index.cfm?do=v.dsp_resultList&urlString=&county=20&city=574&street=&strNbrLow=&strNbrHi=&strDir=0&twnShp=&rnge=&section=&group=0&propName=&rscType=0&eligEval=ES&constrYr1=&constrYr2=&origUse=0&style=0&archBldr=&nrListDate1=&nrListDate2=&nrCritA=false&nrCritB=false&nrCritC=false&nrCritD=false&resultType=3) in Eugene, Springfield, Coburg in the SHPO data. The equivalent numbers from NPS are 46, 5, and 2. The data sets from cities adjusted with follow-up communication are adopted when there are discrepancies among the city, SHPO, and NPS data sets. Only sites within UGB are included.

##### 4. Combine national register sites from Eugene and SHPO data

The columns on id, name, address, city, yrbuilt, and geometry are combined from cleaned Eugene and SHPO data. The duplicated Eugene data is removed with the same name and geometry. The ID columns are *cultural_r* and *resource_1*, the name columns are *historic_n* and *propName*, the yrbuilt columns are *constructi* and *yrBuilt*, from Eugene and SHPO data. The id column is kept to track the source data ('Eugene/CL_NR_HistoricSites_July2021.shp' and 'SHPO/HistoricSites-point.shp' in *T:\MPO\RTP\FY20 2045 Update\Data and Resources\Data\ForAppendixF\Historic*). The file T:\MPO\RTP\FY20 2045 Update\Data and Resources\Data\ForAppendixF\Historic\NationalRegisterHistoricSitesCLMPO.shp includes the combined national register sites, from the script [historic_sites.ipynb](https://github.com/dongmeic/RTP/blob/main/data/historic_sites.ipynb), and the file T:\MPO\RTP\FY20 2045 Update\Data and Resources\Data\ForAppendixF\Historic\NationalRegisterHistoricDistrictsCLMPO.shp includes the combined national register districts, from the script [historic_districts.ipynb](https://github.com/dongmeic/RTP/blob/main/data/historic_districts.ipynb). 

#### Historical Districts (polygon)

There are totally five historic districts in CLMPO combining data from multiple sources (see [notes](https://github.com/dongmeic/RTP/tree/main/data#1-data-sources) above), including East Skinner Butte National Register Historic District and Blair Boulevard Historic Commercial Area in Eugene, Washburne Historic District and Dorris Ranch Historic District in Springfield, and Coburg Historic District. The boundary of Dorris Ranch Historic District was adjusted based on an excerpt from the Dorris Ranch Historic District submission shared by the City. The file T:\MPO\RTP\FY20 2045 Update\Data and Resources\Data\ForAppendixF\Historic\NationalRegisterHistoricDistrictsCLMPO.shp includes the combined national register districts.

<!-- #### Open Space

#### Scenic Views and Sites

### Natural Resources (Land)

#### Goal 3 Agricultural Lands

#### Goal 4 Forest Lands

#### Goal 5 Natural Resources (Land) -- Part of Goal 5

1. Riparian corridors

2. Wetlands (all national and local wetland inventories)

3. Uplands

4. Approved Oregon Recreation Trails

5. Natural Areas

#### Goal 15 Willamette River Greenway 
 -->

## Sensitive Water Resources -- Part of Goal 5

### 1. DEQ 303d Listed Streams

The Department of Environmental Quality (DEQ) lists water bodies with limited water quality that need TMDLs (Total Maximum Daily Loads), [303(d) list](https://www.deq.state.or.us/wq/assessment/rpt2010/search.asp#db). The data was downloaded from the [Oregon Spatial Data Library](https://spatialdata.oregonexplorer.info/geoportal/details;id=7bee41a81cdb4eb99d71cdd2217ee3da). The streams with a listing status 'Cat 5: Water quality limited, 303(d) list, TMDL needed' or '303(d)' are included in the GIS analysis (see the script [DEQ303(d)ListedStreams.ipynb](https://github.com/dongmeic/RTP/blob/main/data/DEQ303(d)ListedStreams.ipynb)), although duplicated geometry founded in these assessments, which won't affect the analysis results. The data was not clipped into the CLMPO area.

### 2. Southern Willamette Valley Groundwater Management Area

The Southern Willamette Valley Groundwater Management Area data layer downloaded from the [Oregon Spatial Data Library](https://spatialdata.oregonexplorer.info/geoportal/details;id=ab957b8b4f7244b68fe902eb4f1dd6f5) remains the same as the last RTP data layer. 

### 3. Navigable Rivers

The Oregon rivers layer downloaded from the [Oregon Spatial Data Library](https://spatialdata.oregonexplorer.info/geoportal/details;id=01606665b1034dc6877fbad58bb9879a) with a filter applied (Mckenzie River and Willamette River based on the list in [Navigable Riverways Within the State of Oregon](https://www.nwp.usace.army.mil/Portals/24/docs/regulatory/jurisdiction/Navigable_US_Waters_Oregon_1993.pdf?ver=b_nFSoXJ1YwCARFvh9kNbw%3D%3D)) is considered as the navigable rivers layer for the RTP GIS analysis and mapping.

### 4. Wetlands

The wetlands data layer are derived from the [national wetlands inventory (NWI)](https://www.fws.gov/wetlands/) and the [local wetlands inventories (LWI)](https://www.oregon.gov/dsl/WW/Pages/Inventories.aspx). After comparing the West Eugene LWI with the data layer from the last RTP, which covers larger areas, the West Eugene LWI remains the same as the last RTP. The NWI and LWI layers are combined into a wetlands layer for CLMPO using the script [wetlands.ipynb](https://github.com/dongmeic/RTP/blob/main/data/wetlands.ipynb). 

## Watershed

[Watershed boundaries](https://spatialdata.oregonexplorer.info/geoportal/details;id=4b1b008d5a764a209b2df040689c0779) and stormwater basins are included in mapping only. The stormwater basins data layers are from the last RTP data. The major basin names in Eugene are shown in the [Stormwater Basin Master Plan](https://www.eugene-or.gov/DocumentCenter/View/2674/Stormwater-Basin-Master-Plan---Volume-4).

## Sensitive Habitats -- Part of Goal 5

<!-- 1. Threatened/Endangered Species Habitats 

2. Oregon Conservation Strategy -->

1. ODFW Conservation Opportunity Areas

This data layer is downloaded from the [Oregon Department of Fish and Wildlife (ODFW)](https://nrimp.dfw.state.or.us/dataclearinghouse/default.aspx?p=202&XMLname=897.xml) website. The layer is clipped using the CLMPO boundary for GIS analysis. 

2. USFWS Critical Habitat



## Natural Hazards

1. FEMA Flood Hazard

2. Seismic Hazard (e.g., liquefaction, landslide, etc.)

3. Fire Hazard


## RTP projects

The LTD stations are collected from the facility data (RLIDGeo.DBO.Facility). 