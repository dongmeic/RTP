# Data for Environmental Analysis Maps (Appendix F)

The list of data sets applied is detailed in the [AppendixF_DataSources.xlsx](https://lanecouncilofgovernments-my.sharepoint.com/:x:/g/personal/dchen_lcog_org/ETvYwmozi9VDndxr9TPPGDEB7oElu_DHpgXZcPy45W1VuQ?e=W0fPG6). The final maps are saved [here](https://lanecouncilofgovernments-my.sharepoint.com/:f:/g/personal/dchen_lcog_org/Elv7d7rgBCdKm_EUAdfBcl0BtUtDN9rufbrMTSJcmoQyNQ?e=Pr43ul).

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

This data layer is downloaded from the [U.S. Fish and Wildlife Service](https://ecos.fws.gov/ecp/report/table/critical-habitat.html). The layer is clipped using the CLMPO boundary for mapping and GIS analysis.  

## Natural Hazards

### 1. FEMA Flood Hazard

The [FEMA map server](https://hazards.fema.gov/gis/nfhl/rest/services/public/NFHL/MapServer) includes the [flood hazard zones](https://hazards.fema.gov/gis/nfhl/rest/services/public/NFHL/MapServer/28). The flood data layer from V:\Data\Natural\Flood is applied while some server error occurred when downloading data from the rest point. The [100 and 500-year floodplains](https://spatialdata.oregonexplorer.info/geoportal/details;id=a0d39fedf55643fc9c2aa1f83b161c63) were not included. The FEMA flood layers are also available on the [DOGAMI MapServer](https://gis.dogami.oregon.gov/arcgis/rest/services/Public/FEMA_Flood/MapServer).

### 2. Seismic Hazard (e.g., liquefaction, landslide, expected shaking, etc.)

<!-- The landside susceptibility data layer is downloaded from the [DOGAMI ImageServer](https://gis.dogami.oregon.gov/arcgis/rest/services/Public/Landslide_Susceptibility/ImageServer).  -->

The [Oregon Seismic Hazards Database (OSHD)](https://www.oregongeology.org/pubs/dds/p-OSHD-1.htm) published on Jane 21st, 2021 by the Oregon Department of Geology and Mineral Industries (DOGAMI) is applied in this analysis with the [liquefaction susceptibility](https://htmlpreview.github.io/?https://github.com/dongmeic/RTP/blob/main/data/metadata/Liquefaction_Susceptibility_Map_metadata_HTML.html), [dry landslide susceptibility](https://htmlpreview.github.io/?https://github.com/dongmeic/RTP/blob/main/data/metadata/Dry_Landslide_Susceptibility_Map_metadata_HTML.html), [wet landslide susceptibility](https://htmlpreview.github.io/?https://github.com/dongmeic/RTP/blob/main/data/metadata/Wet_Landslide_Susceptibility_Map_metadata_HTML.html), and [probability of damaging shaking](https://htmlpreview.github.io/?https://github.com/dongmeic/RTP/blob/main/data/metadata/Probability_of_Damaging_Shaking_Map_metadata_HTML.html) data layers. The four data layers were reviewed on the spatial distribution of hazard probability and determined on the higher levels of risks. It took five steps to [get a seismic hazard data layer](https://github.com/dongmeic/RTP/blob/main/data/get_seismic_hazard_layer_for_AppendixF.ipynb) using the above data sets: 1) extract data by the mask of the CLMPO boundary; 2) reclassify the extracted data into 0 and 1 to fliter higher risk areas; 3) convert raster to polygon on each reclassified data; 4) select the higher risk regions marked as 1 from each polygon data and merge them to one single layer with notes on data sources; 5) dissolve the merged polygon by data source.

### 3. Fire Hazard

The nationwide fire hazard data layer is downloaded from the [USFS ImageServer](https://apps.fs.usda.gov/fsgisx01/rest/services/RDW_Wildfire/RMRS_WildfireHazardPotential_classified_2020/ImageServer) and clipped to Lane County.

## Air Quality

The air quality maintenance area is the Eugene-Springfield Urban Growth Boundaries from RLIDGeo.DBO.UGB.

## Environmental Justice

The environmental justice elements are derived from the Title VI data. The Title VI variables are explained [here](https://github.com/dongmeic/MPO_Data_Portal/tree/master/PopulationData#explanations-of-the-title-vi-variables).

## RTP projects

The LTD stations are collected from the facility data (RLIDGeo.DBO.Facility).

# GIS Analysis for the Appendix F Tables

The scripts [Analysis4AppendixF.py](https://github.com/dongmeic/RTP/blob/main/data/Analysis4AppendixF.py) and [analysis_for_AppendixF.ipynb](https://github.com/dongmeic/RTP/blob/main/data/analysis_for_AppendixF.ipynb) are used to calculate the number of projects intersected with the different environmental data layers (see the tables in the [Appendix F Outline & Mapping Needs.docx](https://lanecouncilofgovernments-my.sharepoint.com/:w:/g/personal/dchen_lcog_org/EVbeSXT1cblKo1NnhEIi-ZoBDXXLeRCT48o4oPZ8ld_ycg?e=ACuriv)). The function *RTP_counted_by_intersection* should create the same results as the tool *Select by Location* in ArcGIS Pro, with settings of the input feature as the bufferred RTP layer, relationship as "intersect", and the selecting feature as the environmental data layer. Since the transit project type only include LTD routes and stations, the intersection between transit projects, i.e., frequent transit network and stations, and environmental data is calculated for the number of unique routes and stations, respectively. The calculation for the environmental justice table using the population or household for minority, low-income, senior, disabled, and LEP in the intersected block groups and the total population or households columns in MPO from the TitleVI table (see script [analyisis_on_environmental_justice.ipynb](https://github.com/dongmeic/RTP/blob/main/data/analyisis_on_environmental_justice.ipynb)). Note that the population data in 2045 is not available with the same details, so the EJ data for the proposed bike paths and sidewalks is derived from the current TitleVI data. In this case, the intersection results of TitleVI data are the same with or without the proposed RTP projects. In the summary table for the number of intersected RTP projects, the EJ column is calculated based on the equity area defined as the number of factors that equals to or is higher than 3 for the communities of concern. The MPO area column can be used to calculate the percentage of RTP project coverage.
