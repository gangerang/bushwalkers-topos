# Bushwalkers Topos
An interactive map designed for bushwalkers in NSW

[Try it out](https://gangerang.github.io/bushwalkers-topos/index.html)

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