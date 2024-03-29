# RTP
The repo is to collect data for RTP performance analysis and mapping. There are scripts using two python environments. To update the arcpy environment, clone the environment in ArcGIS Pro into C:\Users\clid1852\AppData\Local\ESRI\conda\envs. Delete the clone when there is an update in ArcGIS Pro.

# Required datasets for performance analysis

1. Transit stops and high frequency stops

2. Bikeways / bike facility

3. Sidewalks & sidewalk ramps

4. Tail/multi-use path

5. MTIP map

6. Title VI category 3 and 4

The MPO facilities include bikeways and sidewalks. The steps for performance analysis are listed in 1) coburg_sidewalks_bike_lanes; 2) sidewalks_MPO; 3) bikeways_MPO; and 4) facilities in the 'RTP/data' folder and 5) system_completeness in the RTP/analysis folder.

# Required datasets for [web-mapping](https://arcg.is/0L8azS)
1. Transportation

· Roads (interstate, state freeways, arterials)

· Transit network and stops

· Bike/Ped facilities

2. RTP

Project modes

· Roads

· Transit

· Bike/Ped

3. Facilities

4. Access to opportunities (off-peak and peaking, from the travel demand model)

· Workplace accessibility auto

· Workplace accessibility transit

5. Historically excluded populations (Title VI data)

6. Households and employment (from UrbanSim)

7. Land use

8. Plan designations (future land use)

# [Steps for the calculation of accessibility](https://github.com/dongmeic/RTP/blob/main/analysis/Steps.png)

# RTP map series
## [Scale-based RTP mapping (2040)](https://arcg.is/yL0nb)

This map is outdated. The RTP layer is not available. 

## [Mapping RTP projects (2045)](https://arcg.is/1jmOyr)

### Project review and GIS data update

The final data is saved in the folder T:\MPO\RTP\FY20 2045 Update\Data and Resources\Data\GISData\Updated. The script [*reivew_RTP.py*](https://github.com/dongmeic/RTP/blob/main/projlist/review_RTP.py) includes all the functions used to review RTP project list spreadsheets and GIS data.

Four rounds of review were conducted to match RTP list and GIS data. The RTP IDs in the 2045 table were matched with the RTP IDs in the existing GIS data first and then compared with the RTP IDs in the 2040 table, and both are by category. Some RTP IDs are repeated between different categories, which caused a review in the duplicated RTP IDs before updating the attribute table with the 2045 data. The RTP IDs are also duplicated in the exiting GIS data and so the spatial features with the same RTP IDs were reviewed. As such, four steps were followed to create the 2045 GIS data.

Step 1: match ID between the 2040 GIS data and the 2045 table with common IDs in the same category and filter the exiting GIS data for the 2045 GIS data;

Step 2: match the 2045 GIS data from step 1 and common and unique RTP IDs from tables compared between 2040 and 2045 in the same category with a review on the duplicated IDs in the same category; the attribute table is updated with the 2045 table data in this step and the duplicated RTP IDs in either table are dropped first before the merge;

Step 3: add previously dropped duplicated projects in either table with a review in GIS data and drop duplicated GIS records in the new data in this step;

Step 4: review the projects that are with duplicated RTP IDs or without an ID, check whether these projects are in the existing GIS data by matching the names, and add the projects if they are or map the projects if they are not;

The transit projects are excluded in the mapping, however, the tables are matched between the two years (2040 and 2045). There are 306 records in the 2040 table and 279 records in the 2045 table. There are 25 records without an unique ID, with 15 of them are mapped and 2 from the match with the existing GIS data by name. There are 224 unique RTP IDs shared between the 2040 and 2045 data and 30 unique RTP IDs from the 2040 data are not in the 2045 data. Finally, there are 255 unique IDs mapped in the existing GIS data and 222 unique IDs in the 2045 GIS data. Random and unique RTP IDs are generated for the newly mapped projects, however, these projects might have existed in the 2040 GIS data and were missed in the match due to absent RTP IDs or unmatched names in the 2045 data.  

### For future RTP project list update  

There are issues with duplicated RTP IDs within the same category and between categories. These records are documented in T:\MPO\RTP\FY20 2045 Update\Data and Resources\ProjectReview\2045repeatedRTPID.csv (or 2040repeatedRTPID.csv for the 2040 table). Duplicated names are also found in the tables. It would be easier to track GIS data if the tables can keep unique IDs and names on the projects. GIS data has issues on unclear column names and changing project names.

### Links for webmap and data download

[Webmap for the 2045 RTP projects](https://arcg.is/1jmOyr)

[Constrained_BikePed](https://services5.arcgis.com/9s1YtFmLS0YTl10F/arcgis/rest/services/Constrained_BikePed/FeatureServer)

[Constrained_BikePed_points](https://services5.arcgis.com/9s1YtFmLS0YTl10F/arcgis/rest/services/Constrained_BikePed_points/FeatureServer)

[Constrained_Roadway_lines](https://services5.arcgis.com/9s1YtFmLS0YTl10F/arcgis/rest/services/Constrained_Roadway_lines/FeatureServer)

[Constrained_Roadway_points](https://services5.arcgis.com/9s1YtFmLS0YTl10F/arcgis/rest/services/Constrained_Roadway_points/FeatureServer)

[Illustrative_BikePed](https://services5.arcgis.com/9s1YtFmLS0YTl10F/arcgis/rest/services/Illustrative_BikePed/FeatureServer)

[Illustrative_Roadway_lines](https://services5.arcgis.com/9s1YtFmLS0YTl10F/arcgis/rest/services/Illustrative_Roadway_lines/FeatureServer)

[Illustrative_Roadway_points](https://services5.arcgis.com/9s1YtFmLS0YTl10F/arcgis/rest/services/Illustrative_Roadway_points/FeatureServer)

# RTP data quality control

## Facilities (bikeways and sidewalks in CLMPO)

The [facilities](https://github.com/dongmeic/RTP/blob/main/data/facilities.ipynb) data includes [bikeways](https://github.com/dongmeic/RTP/blob/main/data/bikeways_MPO.ipynb) and [sidewalks](https://github.com/dongmeic/RTP/blob/main/data/sidewalks_MPO.ipynb), clipped by the boundary of MPO. The bike facility data is updated weekly in RLID Geo from RLID Transportation, a collaborative data layer among the cities. Sidewalks and bikeways are combined to be the facilities layer after data cleaning, e.g., excluding the future status in the bike facility data and combining the [Coburg bike paths edited](https://github.com/dongmeic/RTP/blob/main/data/coburg_sidewalks_bike_lanes.ipynb). Data can be downloaded on ArcGIS Online: [bikeways](https://lcog.maps.arcgis.com/home/item.html?id=48d3859500494495b71d87afd5eb8fae) and [facilities](https://lcog.maps.arcgis.com/home/item.html?id=24458e4a14744c259fe172177de6960f).

## Centerline road ownership comparison among street data sets

The webmap [Centerlines by Owner](https://arcg.is/19naGy0) shows the results of the comparisons. Go to the Content column to select the specific layers for more information. The script [QC_centerlines.py](https://github.com/dongmeic/RTP/blob/main/data/QC_centerlines.py) lists the functions used to review and update the regional centerline network data.

### Data sources

1) Central lane road centerlines from RLDGeo;

2) Eugene street lines from the [City of Eugene Mapping HUB](https://mapping.eugene-or.gov/datasets/eugene-street-lines-hub/explore?location=44.063960%2C-123.125350%2C12.24&showTable=true), downloaded on June 2nd, 2021.

3) Springfield streets from the Geodatabase *Springfield_Infrastructure_P*, access on June 8th, 2021.

The local functional class is excluded in all datasets in the comparison.

### Data manipulation

The owner names "CNTY" and "LANE" are changed to "LCPW" and "CITY" is changed to "SPR" in the Springfield streets data to keep the names consistent between the city street data and central lane data. The ID columns "COMPKEY" and "EUGID" in the Springfield and Eugene streets data are matched with the ID columns "sprid" and "eugid" respectively. Only the common IDs that are shared in both datasets in the comparing group are used in the comparison. The IDs that are not shared between datasets might share the same spatial features, caused by mismatches between IDs. Within the common IDs, features from both datasets in the comparison are selected by each ID one by one.

There are four situations that can happen in both selected datasets: only one feature in each, and one or both datasets has/have more than one feature. If both dataset matched by ID has one feature only and the owner information is the same, then it is considered as having same owner information, otherwise, the ID is included in the different-owner ID list. When the number of features are different, if any of differences exist, the ID is also included in the different-owner ID list. The features with an ID in the different-owner ID list or the ID list that excludes the common IDs are selected in each comparing dataset.

The quality control (QC) results are mapped using the same color schemes to compare spatial features. The differences within common IDs show direct results of different owner information and the differences including mismatched IDs also show features that are with different IDs but the owner information can be consistent. Most of the road segments with different ownerships are relatively short except for Delta Highway, Northwest Expressway, and Ferry Street Bridge.

Detailed QC output can be found in T:\MPO\RTP\FY20 2045 Update\Data and Resources\Data\QC_road_ownership. The text files *reviewCommonIDsEUG.txt* and *reviewCommonIDsSPR.txt* list the detailed differences in the two comparing groups. The ArcGIS Pro project *Centerline_Network.aprx* located at T:\MPO\RTP\FY20 2045 Update\Data and Resources\Data displays most of the data except the difference data with common IDs only that was added directly to the web map.

### Data update

#### Review after the RLID update

The ArcGIS Pro project `T:\MPO\RTP\FY20 2045 Update\Data and Resources\Data\Centerline_Network.aprx` shows the changes before and after the updates of road ownership. The [main changes](https://lanecouncilofgovernments-my.sharepoint.com/:w:/g/personal/dchen_lcog_org/EVIHdP4GmRNNtbSrdKh0HrYBXF19Qg7bQIDu921kZr_gtg?e=mB7QAR) in road ownership are in the Delta Highway, from LCPW to ODOT, Northwest Expressway, from EUG to LCPW, and Coburg Road (near E 2nd Ave), from EUG to ODOT, although some differences between the regional and city data still exist. The rest differences (not limited on road ownership difference) are shown in small segments, mainly in three conditions: 1) either the Central Lane centerlines or Eugene streets have extra segments, 2) the IDs are different, and 3) the IDs are the same but with different numbers of features.   

#### Update the data for DKS

The data can be downloaded [here](https://github.com/dongmeic/RTP/blob/main/data/download/Central_Lane_Centerline_Network.shp.zip). Note that the local functional class is excluded in this data.

To keep the road ownership consistent between the regional and city data, the adjustments are made firstly among the common IDs and then based on the length and geometry with a precision setting to make sure the exact one-on-one match. Some extra segments in either dataset and different road segments with the same ID or on the same road cause the remaining mismatches. These mismatches are usually in small segments, which are considered minor issues and ignored. However, more work might be required to ensure the different road segments in either are necessarily matched, particularly on the mismatches in multiple road segments on the same road or large gaps.
