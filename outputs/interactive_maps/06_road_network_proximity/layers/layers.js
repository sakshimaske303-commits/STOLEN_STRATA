var wms_layers = [];


        var lyr_DarkMatter_0 = new ol.layer.Tile({
            'title': 'Dark Matter',
            'opacity': 1.000000,
            
            
            source: new ol.source.XYZ({
            attributions: '<a href="https://cartodb.com/basemaps/">Map tiles by CartoDB, under CC BY 4.0. Data by OpenStreetMap, under ODbL.</a>',
                url: 'https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png'
            })
        });
var format_karewa_bare_earth_change_1 = new ol.format.GeoJSON();
var features_karewa_bare_earth_change_1 = format_karewa_bare_earth_change_1.readFeatures(json_karewa_bare_earth_change_1, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_karewa_bare_earth_change_1 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_karewa_bare_earth_change_1.addFeatures(features_karewa_bare_earth_change_1);
var lyr_karewa_bare_earth_change_1 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_karewa_bare_earth_change_1, 
                style: style_karewa_bare_earth_change_1,
                popuplayertitle: 'karewa_bare_earth_change',
                interactive: true,
    title: 'karewa_bare_earth_change<br />\
    <img src="styles/legend/karewa_bare_earth_change_1_0.png" /> intact<br />\
    <img src="styles/legend/karewa_bare_earth_change_1_1.png" /> likely_degraded<br />' });
var format_road_network_2 = new ol.format.GeoJSON();
var features_road_network_2 = format_road_network_2.readFeatures(json_road_network_2, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_road_network_2 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_road_network_2.addFeatures(features_road_network_2);
var lyr_road_network_2 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_road_network_2, 
                style: style_road_network_2,
                popuplayertitle: 'road_network',
                interactive: true,
                title: '<img src="styles/legend/road_network_2.png" /> road_network'
            });
var format_settlements_3 = new ol.format.GeoJSON();
var features_settlements_3 = format_settlements_3.readFeatures(json_settlements_3, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_settlements_3 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_settlements_3.addFeatures(features_settlements_3);
var lyr_settlements_3 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_settlements_3, 
                style: style_settlements_3,
                popuplayertitle: 'settlements',
                interactive: true,
                title: '<img src="styles/legend/settlements_3.png" /> settlements'
            });

lyr_DarkMatter_0.setVisible(true);lyr_karewa_bare_earth_change_1.setVisible(true);lyr_road_network_2.setVisible(true);lyr_settlements_3.setVisible(true);
var layersList = [lyr_DarkMatter_0,lyr_karewa_bare_earth_change_1,lyr_road_network_2,lyr_settlements_3];
lyr_karewa_bare_earth_change_1.set('fieldAliases', {'fid': 'fid', 'terrace_candidate': 'terrace_candidate', 'area_km2': 'area_km2', 'mean_elevation': 'mean_elevation', 'bare_frac_1994': 'bare_frac_1994', 'bare_frac_2025': 'bare_frac_2025', 'bare_frac_change': 'bare_frac_change', 'status': 'status', });
lyr_road_network_2.set('fieldAliases', {'fid': 'fid', });
lyr_settlements_3.set('fieldAliases', {'fid': 'fid', 'name': 'name', });
lyr_karewa_bare_earth_change_1.set('fieldImages', {'fid': 'TextEdit', 'terrace_candidate': 'TextEdit', 'area_km2': 'TextEdit', 'mean_elevation': 'TextEdit', 'bare_frac_1994': 'TextEdit', 'bare_frac_2025': 'TextEdit', 'bare_frac_change': 'TextEdit', 'status': 'TextEdit', });
lyr_road_network_2.set('fieldImages', {'fid': '', });
lyr_settlements_3.set('fieldImages', {'fid': 'TextEdit', 'name': 'TextEdit', });
lyr_karewa_bare_earth_change_1.set('fieldLabels', {'fid': 'no label', 'terrace_candidate': 'no label', 'area_km2': 'no label', 'mean_elevation': 'no label', 'bare_frac_1994': 'no label', 'bare_frac_2025': 'no label', 'bare_frac_change': 'no label', 'status': 'no label', });
lyr_road_network_2.set('fieldLabels', {'fid': 'no label', });
lyr_settlements_3.set('fieldLabels', {'fid': 'no label', 'name': 'no label', });
lyr_settlements_3.on('precompose', function(evt) {
    evt.context.globalCompositeOperation = 'normal';
});