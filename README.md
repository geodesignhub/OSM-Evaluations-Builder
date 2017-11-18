# Geodesignhub OSM Evaluation Maps Builder
This program uses Openstreetmap data from [Trimble Marketplace](https://market.trimbledata.com/) to develop Evaluation maps for [Geodesignhub](https://www.geodesignhub.com/). It uses simple rules to parse the existing data and build evaluation maps that can be used directly on Geodesignhub.

Making evaluation maps is the most time consuming part of a Geodesign study, using this script it can be automated. The following evaluation maps are generated: 

* Residential (RES)
* Commerce (COM)
* Parks and Recreation (PREC)
* Active Transport (ATRANS)
* Public Transport (PTRANS)
* Community Facilities (COMFAC)
* Tourism (TOUR)

Find out more about evaluation maps at the [Making Evaluations Maps](https://community.geodesignhub.com/t/making-evaluation-maps/62) in our community page. 


At the moment, this is best suited for generating evaluations at local area level and for studies for where the study area is neighbourhoods, few streets etc. For larger areas this type of Evaluation map creation is not recommended. 

If you are new to Geodesignhub, please see our course at [Teachable.com](https://geodesignhub.teachable.com/p/geodesign-with-geodesignhub/)  

## Installation
Use the requirements.txt file to install libraries that are required for the program

```
pip install requirements.txt
```

## 3-Step process
**1. Download raw data**

1. Go to [https://market.trimbledata.com](https://market.trimbledata.com) to order and download OSM data for your area of interest.
 - Search for the area of your interst in the interface (top left)
 - Create a polygon and select OSM data (free) in the right hand side
 - Once the order is ready they will email you with a link to a zip file
2. Once the zip file is mailed to you will need to upload it to a publically accessible URL. e.g. 

**2. Update config.py**

1. In config.py set the URL of the Trimble data zip file
2. Set the aoibounds parameter to set the bounding box co-ordinates in `(southwest_lng,southwest_lat,northeast_lng,northeast_lat)` format. 

**3. Upload Evaluations**

1. Run the `OSM-evaluations-generator.py` script and check the `output` folder for the Evaluation GeoJSON that can be uploaded to Geodesignhub

