var wms_layers = [];


        var lyr_GoogleTerrain_0 = new ol.layer.Tile({
            'title': 'Google Terrain',
            'opacity': 1.000000,
            
            
            source: new ol.source.XYZ({
            attributions: '<a href="https://www.google.at/permissions/geoguidelines/attr-guide.html">Map data ©2015 Google</a>',
                url: 'https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}'
            })
        });
var format_kashmir_3districtsstudy_area_1 = new ol.format.GeoJSON();
var features_kashmir_3districtsstudy_area_1 = format_kashmir_3districtsstudy_area_1.readFeatures(json_kashmir_3districtsstudy_area_1, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_kashmir_3districtsstudy_area_1 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_kashmir_3districtsstudy_area_1.addFeatures(features_kashmir_3districtsstudy_area_1);
var lyr_kashmir_3districtsstudy_area_1 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_kashmir_3districtsstudy_area_1, 
                style: style_kashmir_3districtsstudy_area_1,
                popuplayertitle: 'kashmir_3districts — study_area',
                interactive: true,
                title: '<img src="styles/legend/kashmir_3districtsstudy_area_1.png" /> kashmir_3districts — study_area'
            });
var format_aoi_bbox_2 = new ol.format.GeoJSON();
var features_aoi_bbox_2 = format_aoi_bbox_2.readFeatures(json_aoi_bbox_2, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_aoi_bbox_2 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_aoi_bbox_2.addFeatures(features_aoi_bbox_2);
var lyr_aoi_bbox_2 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_aoi_bbox_2, 
                style: style_aoi_bbox_2,
                popuplayertitle: 'aoi_bbox',
                interactive: true,
                title: '<img src="styles/legend/aoi_bbox_2.png" /> aoi_bbox'
            });
var format_waterway_river_3 = new ol.format.GeoJSON();
var features_waterway_river_3 = format_waterway_river_3.readFeatures(json_waterway_river_3, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_waterway_river_3 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_waterway_river_3.addFeatures(features_waterway_river_3);
var lyr_waterway_river_3 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_waterway_river_3, 
                style: style_waterway_river_3,
                popuplayertitle: 'waterway_river',
                interactive: true,
                title: '<img src="styles/legend/waterway_river_3.png" /> waterway_river'
            });
var format_settlements_4 = new ol.format.GeoJSON();
var features_settlements_4 = format_settlements_4.readFeatures(json_settlements_4, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_settlements_4 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_settlements_4.addFeatures(features_settlements_4);
var lyr_settlements_4 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_settlements_4, 
                style: style_settlements_4,
                popuplayertitle: 'settlements',
                interactive: true,
                title: '<img src="styles/legend/settlements_4.png" /> settlements'
            });

lyr_GoogleTerrain_0.setVisible(true);lyr_kashmir_3districtsstudy_area_1.setVisible(true);lyr_aoi_bbox_2.setVisible(true);lyr_waterway_river_3.setVisible(true);lyr_settlements_4.setVisible(true);
var layersList = [lyr_GoogleTerrain_0,lyr_kashmir_3districtsstudy_area_1,lyr_aoi_bbox_2,lyr_waterway_river_3,lyr_settlements_4];
lyr_kashmir_3districtsstudy_area_1.set('fieldAliases', {'fid': 'fid', 'DISTRICT': 'DISTRICT', 'ST_NM': 'ST_NM', 'ST_CEN_CD': 'ST_CEN_CD', 'DT_CEN_CD': 'DT_CEN_CD', 'censuscode': 'censuscode', });
lyr_aoi_bbox_2.set('fieldAliases', {'fid': 'fid', 'name': 'name', });
lyr_waterway_river_3.set('fieldAliases', {'fid': 'fid', 'full_id': 'full_id', 'osm_id': 'osm_id', 'osm_type': 'osm_type', 'waterway': 'waterway', 'tunnel': 'tunnel', 'layer': 'layer', 'name:zh': 'name:zh', 'boat': 'boat', 'name:ru': 'name:ru', 'name:fa': 'name:fa', 'wikipedia': 'wikipedia', 'wikidata': 'wikidata', 'name:ur': 'name:ur', 'name:sd': 'name:sd', 'name:pt': 'name:pt', 'name:pa': 'name:pa', 'name:ml': 'name:ml', 'name:kn': 'name:kn', 'name:hi': 'name:hi', 'name:es': 'name:es', 'name:en': 'name:en', 'name:de': 'name:de', 'name:cs': 'name:cs', 'name:azb': 'name:azb', 'name:az-Arab': 'name:az-Arab', 'name:ar': 'name:ar', 'name': 'name', 'alt_name:ar': 'alt_name:ar', });
lyr_settlements_4.set('fieldAliases', {'fid': 'fid', 'name': 'name', });
lyr_kashmir_3districtsstudy_area_1.set('fieldImages', {'fid': 'TextEdit', 'DISTRICT': 'TextEdit', 'ST_NM': 'TextEdit', 'ST_CEN_CD': 'Range', 'DT_CEN_CD': 'Range', 'censuscode': 'TextEdit', });
lyr_aoi_bbox_2.set('fieldImages', {'fid': 'TextEdit', 'name': 'TextEdit', });
lyr_waterway_river_3.set('fieldImages', {'fid': 'TextEdit', 'full_id': 'TextEdit', 'osm_id': 'TextEdit', 'osm_type': 'TextEdit', 'waterway': 'TextEdit', 'tunnel': 'TextEdit', 'layer': 'TextEdit', 'name:zh': 'TextEdit', 'boat': 'TextEdit', 'name:ru': 'TextEdit', 'name:fa': 'TextEdit', 'wikipedia': 'TextEdit', 'wikidata': 'TextEdit', 'name:ur': 'TextEdit', 'name:sd': 'TextEdit', 'name:pt': 'TextEdit', 'name:pa': 'TextEdit', 'name:ml': 'TextEdit', 'name:kn': 'TextEdit', 'name:hi': 'TextEdit', 'name:es': 'TextEdit', 'name:en': 'TextEdit', 'name:de': 'TextEdit', 'name:cs': 'TextEdit', 'name:azb': 'TextEdit', 'name:az-Arab': 'TextEdit', 'name:ar': 'TextEdit', 'name': 'TextEdit', 'alt_name:ar': 'TextEdit', });
lyr_settlements_4.set('fieldImages', {'fid': 'TextEdit', 'name': 'TextEdit', });
lyr_kashmir_3districtsstudy_area_1.set('fieldLabels', {'fid': 'no label', 'DISTRICT': 'no label', 'ST_NM': 'no label', 'ST_CEN_CD': 'no label', 'DT_CEN_CD': 'no label', 'censuscode': 'no label', });
lyr_aoi_bbox_2.set('fieldLabels', {'fid': 'no label', 'name': 'no label', });
lyr_waterway_river_3.set('fieldLabels', {'fid': 'no label', 'full_id': 'no label', 'osm_id': 'no label', 'osm_type': 'no label', 'waterway': 'no label', 'tunnel': 'no label', 'layer': 'no label', 'name:zh': 'no label', 'boat': 'no label', 'name:ru': 'no label', 'name:fa': 'no label', 'wikipedia': 'no label', 'wikidata': 'no label', 'name:ur': 'no label', 'name:sd': 'no label', 'name:pt': 'no label', 'name:pa': 'no label', 'name:ml': 'no label', 'name:kn': 'no label', 'name:hi': 'no label', 'name:es': 'no label', 'name:en': 'no label', 'name:de': 'no label', 'name:cs': 'no label', 'name:azb': 'no label', 'name:az-Arab': 'no label', 'name:ar': 'no label', 'name': 'no label', 'alt_name:ar': 'no label', });
lyr_settlements_4.set('fieldLabels', {'fid': 'no label', 'name': 'no label', });
lyr_settlements_4.on('precompose', function(evt) {
    evt.context.globalCompositeOperation = 'normal';
});