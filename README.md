# RTP
The repo is to collect data for RTP performance analysis and mapping

# Required datasets for performance analysis

1. Transit stops and high frequency stops

2. Bikeways / bike facility

3. Sidewalks & sidewalk ramps

4. Tail/multi-use path

5. MTIP map

6. Title VI category 3 and 4

The MPO facilities include bikeways and sidewalks. The steps for performance analysis are listed in 1) coburg_sidewalks_bike_lanes; 2) sidewalks_MPO; 3) bikeways_MPO; and 4) facilities in the 'RTP/data' folder and 5) system_completeness in the RTP/analysis folder.

# Required datasets for [web-mapping](https://arcg.is/0L8azS)
## Transportation

·        Roads (interstate, state freeways, arterials)

·        Transit network and stops

·        Bike/Ped facilities

## RTP

Project modes

·        Roads

·        Transit

·        Bike/Ped

## Recreation

·        Community centers 

·        Trails

·        Parks

·        Golf courses

·        Green space

o   Greenways

o   Mountain preservation

o   Rural preservation

o   Stream preservation
 
 
## Access to opportunities (off-peak and peaking)

·        Workplace accessibility auto

·        Workplace accessibility transit

## Growth projections

·        Population projections

·        Employment projections

## Active transportation

·        Planned pathways

·        Planned bike on-street

·        Existing pathways

·        Existing bike on-street

## Land use

## Plan designations (future land use)

# RTP map series
## [Scale-based RTP mapping (2040)](https://arcg.is/yL0nb) 

## Mapping RTP projects (2045)

1. Project review and GIS data update

The script [*reivew_RTP.py*](https://github.com/dongmeic/RTP/blob/main/projlist/review_RTP.py) includes all the functions used to review RTP project list spreadsheets and GIS data. 

Four rounds of review were conducted to match RTP list and GIS data. The RTP IDs in the 2045 table were matched with the RTP IDs in the existing GIS data first and then compared with the RTP IDs in the 2040 table, and both are by category. The RTP IDs are repeated between different categories, which caused a review in the duplicated RTP IDs before updating the attribute table with the 2045 data. The RTP IDs are also duplicated in the exiting GIS data and so the spatial features with the same RTP IDs were reviewed. As such, four steps were followed to create the 2045 GIS data.

Step 1: match ID between the 2040 GIS data and the 2045 table with common IDs in the same category and filter the exiting GIS data for the 2045 GIS data;

Step 2: match the 2045 GIS data from step 1 and common and unique RTP IDs from tables compared between 2040 and 2045 in the same category with a review on the duplicated IDs in the same category; the attribute table is updated with the 2045 table data in this step and the duplicated RTP IDs in either table are dropped first before the merge;

Step 3: add previously dropped duplicated projects in either table with a review in GIS data and drop duplicated GIS records in the new data in this step;

Step 4: review the projects that are with duplicated RTP IDs or without an ID, check whether these projects are in the existing GIS data by matching the names, and add the projects if they are or map the projects if they are not;

The transit projects are excluded in the mapping, however, the tables are matched between the two years (2040 and 2045). There are 306 records in the 2040 table and 279 records in the 2045 table. There are 25 records without an unique ID, with 15 of them are mapped and 2 from the match with the existing GIS data by name. There are 224 unique RTP IDs shared between the 2040 and 2045 data and 30 unique RTP IDs from the 2040 data are not in the 2045 data. Finally, there are 255 unique IDs mapped in the existing GIS data and 222 unique IDs in the 2045 GIS data. Random and unique RTP IDs are generated for the newly mapped projects, however, these projects might have existed in the 2040 GIS data and were missed in the match due to absent RTP IDs or unmatched names in the 2045 data.  

2. For future RTP project list update  

There are issues with duplicated RTP IDs with in the same category and between categories. These records are documented in T:\MPO\RTP\FY20 2045 Update\Data and Resources\ProjectReview\2045repeatedRTPID.csv (or 2040repeatedRTPID.csv for the 2040 table). Duplicated names are also found in the tables. It would be easier to track GIS data if the tables can keep unique IDs and names on the projects. GIS data has issues on unclear column names and changing project names. 

3. Links for webmap and data download

[Webmap for the 2045 RTP projects](https://arcg.is/1jmOyr)

[Constrained_BikePed](https://services5.arcgis.com/9s1YtFmLS0YTl10F/arcgis/rest/services/Constrained_BikePed/FeatureServer)

[Constrained_BikePed_points](https://services5.arcgis.com/9s1YtFmLS0YTl10F/arcgis/rest/services/Constrained_BikePed_points/FeatureServer)

[Constrained_Roadway_lines](https://services5.arcgis.com/9s1YtFmLS0YTl10F/arcgis/rest/services/Constrained_Roadway_lines/FeatureServer)

[Constrained_Roadway_points](https://services5.arcgis.com/9s1YtFmLS0YTl10F/arcgis/rest/services/Constrained_Roadway_points/FeatureServer)

[Illustrative_BikePed](https://services5.arcgis.com/9s1YtFmLS0YTl10F/arcgis/rest/services/Illustrative_BikePed/FeatureServer)

[Illustrative_Roadway_lines](https://services5.arcgis.com/9s1YtFmLS0YTl10F/arcgis/rest/services/Illustrative_Roadway_lines/FeatureServer)

[Illustrative_Roadway_points](https://services5.arcgis.com/9s1YtFmLS0YTl10F/arcgis/rest/services/Illustrative_Roadway_points/FeatureServer)