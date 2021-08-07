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

1. DEQ 303d Listed Streams

2. Southern Willamette Valley Groundwater Management Area

3. Navigable Rivers

4. Wetlands (significant Goal 5 wetlands only)

## Watershed

Watershed Boundaries and Stormwater Basins

## Sensitive Habitats -- Part of Goal 5

1. Threatened/Endangered Species Habitats 

2. Oregon Conservation Strategy

3. ODFW Conservation Opportunity Areas

## Natural Hazards

1. FEMA Flood Hazard

2. Seismic Hazard (e.g., liquefaction, landslide, etc.)

3. Fire Hazard


## RTP projects

The LTD stations are collected from the facility data (RLIDGeo.DBO.Facility). 