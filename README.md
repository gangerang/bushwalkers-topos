# Bushwalkers Topos
An interactive map designed for bushwalkers in NSW

[Try it out](https://bushwalkingmaps.com)

Based on leaflet

Includes various useful data sources

A number of historic topographic and cadastral maps sourced from the NLA Map Search website are also overlayed


## change log
### v0.1
- modify - trig station layer - add survey sketch link to trig station pop up and additional 
- modify - trig, parish, ga photos layers - add minzoom levels to prevent loading too many features
- add - about button - new button which links to github repo
- add - npws all managed land layer - new layer for all npws managed land, not just reserves
- add - gov property ex crown layer - new layer based on existing government property index layer, removing crown land lots
- add - government property layers - pop up on both gpi layers to give lot details
- add - fcnsw estate layer - new layer for all forestry corp estate, including state forest, flora reserves and other managed estate
- add - crown land layer popups - new popups for crown land layers (except 'all')
- add - crown land under disposal layer - new layer for crown land which has a current disposal action
- add - stream gauge esri layer - new layer and popup for stream gauge river height from esri filtered on australia only
- add - nsw stream gauge geojson layer - new layer and popup for stream gauge river height in nsw, based on bom processed data stored on github pages as geojson
- add - nsw stream gauge geojson file creation - via github actions, automation to create the dataset which is then referenced as a layer
- add - nsw historic aerial imagery layers - new raster layers for historic aerial imagery in nsw. 34 layers between years 1943 to 2013
- add - schedule 1 and 2 catchment layers - new vector layers from geojsons for waternsw schedule 1 and 2 catchment boundaries

### v0.2
- add - fesm fire layers - new fire extent and severity mapping layers for nsw, 2016-2024
- add - osm basemap - new OpenStreetMap basemap sourced via OpenFreeMap.org
- add - additional boundaries - new boundary layers for suburb, lga, state seats and federal seats, for nsw
- add - OpenTopoMap basemap - new OpenTopoMap basemap which is based on OSM data but styled as a topographic map with hillshade, souced via opentopomap.org
- add - ESRI OSM basemap - new OSM basemap sourced via ESRI vector tiles
- add - OSM seach function - new search tool which returns results from OSM for Australia. Uses leaflet-geosearch plugin and OSM Nominatim api
- add - NSW vector topo basemap - new basemap for NSW spatial services vector tile topo map. Combined with esri hillshade
- add - Sydney historic imagery photos - new layer for historic imagery points for sydney. A subset of the NSW dataset from Spatial Services served as a geopackage
- add - Crown road sales - new layers for proposed crown road sales, both current and past
- add - authenticated strava heatmap layers - based on authenticated data served via a proxy, providing a higher resolution to public version
- add - 1912 trig progress map - historic map of trig survey progress as of 1912, via georeferenced map from NLA surved via geoserver
- add - 100k topo maps - older topo maps from ga at 100k scale. tiffs stiched seamlessly and served via geoserver
- add - 50k topo maps - older topo maps from ga at 50k scale. tiffs stiched seamlessly and served via geoserver
- add - weather radar layer - from rain viewer, rain radar weather layer for most recent observations
- add - NSW historic imagery photos - replaces the sydney only layer, served via geoserver
- add - improve usability on mobile - when viewing on a small screen, basemaps and layers selectable via a popup modal instead of tree
- add - port hacking tourist 1966 - tourist map of port hacking from 1966, served via geoserver
- add - bruces walk 1931 map - tourist map of bruces walk from 1931, served via geoserver
- add - ssc historic aerial layers - historic aerial layers of sutherland shire council from 1930 to 2010
- add - nsw spot imagery - basemap from spot satellite of aerial imagery for nsw. from 2020 so shows fire extent
- add - nsw fires - fire boundaries from 'near real time bushfire boundaries' featureservice
- add - dea hotspots - fire hotspots from ga dea product. shows fire detection from satellite imagery from last 3 days