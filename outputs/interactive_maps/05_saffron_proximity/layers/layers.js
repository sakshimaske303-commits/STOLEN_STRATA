var wms_layers = [];


        var lyr_DarkMatter_0 = new ol.layer.Tile({
            'title': 'Dark Matter',
            'opacity': 1.000000,
            
            
            source: new ol.source.XYZ({
            attributions: '<a href="https://cartodb.com/basemaps/">Map tiles by CartoDB, under CC BY 4.0. Data by OpenStreetMap, under ODbL.</a>',
                url: 'https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png'
            })
        });
var format_likely_degradedkarewa_bare_earth_change_1 = new ol.format.GeoJSON();
var features_likely_degradedkarewa_bare_earth_change_1 = format_likely_degradedkarewa_bare_earth_change_1.readFeatures(json_likely_degradedkarewa_bare_earth_change_1, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_likely_degradedkarewa_bare_earth_change_1 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_likely_degradedkarewa_bare_earth_change_1.addFeatures(features_likely_degradedkarewa_bare_earth_change_1);
var lyr_likely_degradedkarewa_bare_earth_change_1 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_likely_degradedkarewa_bare_earth_change_1, 
                style: style_likely_degradedkarewa_bare_earth_change_1,
                popuplayertitle: 'likely_degraded — karewa_bare_earth_change',
                interactive: true,
                title: '<img src="styles/legend/likely_degradedkarewa_bare_earth_change_1.png" /> likely_degraded — karewa_bare_earth_change'
            });
var format_Buffered_2 = new ol.format.GeoJSON();
var features_Buffered_2 = format_Buffered_2.readFeatures(json_Buffered_2, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_Buffered_2 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_Buffered_2.addFeatures(features_Buffered_2);
var lyr_Buffered_2 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_Buffered_2, 
                style: style_Buffered_2,
                popuplayertitle: 'Buffered',
                interactive: true,
                title: '<img src="styles/legend/Buffered_2.png" /> Buffered'
            });
var format_saffron_proximity_risk_3 = new ol.format.GeoJSON();
var features_saffron_proximity_risk_3 = format_saffron_proximity_risk_3.readFeatures(json_saffron_proximity_risk_3, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_saffron_proximity_risk_3 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_saffron_proximity_risk_3.addFeatures(features_saffron_proximity_risk_3);
var lyr_saffron_proximity_risk_3 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_saffron_proximity_risk_3, 
                style: style_saffron_proximity_risk_3,
                popuplayertitle: 'saffron_proximity_risk',
                interactive: true,
    title: 'saffron_proximity_risk<br />\
    <img src="styles/legend/saffron_proximity_risk_3_0.png" /> false<br />\
    <img src="styles/legend/saffron_proximity_risk_3_1.png" /> true<br />\
    <img src="styles/legend/saffron_proximity_risk_3_2.png" /> <br />' });
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

lyr_DarkMatter_0.setVisible(true);lyr_likely_degradedkarewa_bare_earth_change_1.setVisible(true);lyr_Buffered_2.setVisible(true);lyr_saffron_proximity_risk_3.setVisible(true);lyr_settlements_4.setVisible(true);
var layersList = [lyr_DarkMatter_0,lyr_likely_degradedkarewa_bare_earth_change_1,lyr_Buffered_2,lyr_saffron_proximity_risk_3,lyr_settlements_4];
lyr_likely_degradedkarewa_bare_earth_change_1.set('fieldAliases', {'fid': 'fid', 'terrace_candidate': 'terrace_candidate', 'area_km2': 'area_km2', 'mean_elevation': 'mean_elevation', 'bare_frac_1994': 'bare_frac_1994', 'bare_frac_2025': 'bare_frac_2025', 'bare_frac_change': 'bare_frac_change', 'status': 'status', });
lyr_Buffered_2.set('fieldAliases', {'fid': 'fid', 'terrace_candidate': 'terrace_candidate', 'area_km2': 'area_km2', 'mean_elevation': 'mean_elevation', 'bare_frac_1994': 'bare_frac_1994', 'bare_frac_2025': 'bare_frac_2025', 'bare_frac_change': 'bare_frac_change', 'status': 'status', });
lyr_saffron_proximity_risk_3.set('fieldAliases', {'fid': 'fid', 'terrace_candidate': 'terrace_candidate', 'area_km2': 'area_km2', 'mean_elevation': 'mean_elevation', 'bare_frac_1994': 'bare_frac_1994', 'bare_frac_2025': 'bare_frac_2025', 'bare_frac_change': 'bare_frac_change', 'status': 'status', 'saffron_index': 'saffron_index', 'likely_saffron': 'likely_saffron', 'dist_to_nearest_degraded_m': 'dist_to_nearest_degraded_m', 'at_risk': 'at_risk', });
lyr_settlements_4.set('fieldAliases', {'fid': 'fid', 'name': 'name', });
lyr_likely_degradedkarewa_bare_earth_change_1.set('fieldImages', {'fid': 'TextEdit', 'terrace_candidate': 'TextEdit', 'area_km2': 'TextEdit', 'mean_elevation': 'TextEdit', 'bare_frac_1994': 'TextEdit', 'bare_frac_2025': 'TextEdit', 'bare_frac_change': 'TextEdit', 'status': 'TextEdit', });
lyr_Buffered_2.set('fieldImages', {'fid': 'TextEdit', 'terrace_candidate': 'TextEdit', 'area_km2': 'TextEdit', 'mean_elevation': 'TextEdit', 'bare_frac_1994': 'TextEdit', 'bare_frac_2025': 'TextEdit', 'bare_frac_change': 'TextEdit', 'status': 'TextEdit', });
lyr_saffron_proximity_risk_3.set('fieldImages', {'fid': 'TextEdit', 'terrace_candidate': 'TextEdit', 'area_km2': 'TextEdit', 'mean_elevation': 'TextEdit', 'bare_frac_1994': 'TextEdit', 'bare_frac_2025': 'TextEdit', 'bare_frac_change': 'TextEdit', 'status': 'TextEdit', 'saffron_index': 'TextEdit', 'likely_saffron': 'CheckBox', 'dist_to_nearest_degraded_m': 'TextEdit', 'at_risk': 'CheckBox', });
lyr_settlements_4.set('fieldImages', {'fid': 'TextEdit', 'name': 'TextEdit', });
lyr_likely_degradedkarewa_bare_earth_change_1.set('fieldLabels', {'fid': 'no label', 'terrace_candidate': 'no label', 'area_km2': 'no label', 'mean_elevation': 'no label', 'bare_frac_1994': 'no label', 'bare_frac_2025': 'no label', 'bare_frac_change': 'no label', 'status': 'no label', });
lyr_Buffered_2.set('fieldLabels', {'fid': 'no label', 'terrace_candidate': 'no label', 'area_km2': 'no label', 'mean_elevation': 'no label', 'bare_frac_1994': 'no label', 'bare_frac_2025': 'no label', 'bare_frac_change': 'no label', 'status': 'no label', });
lyr_saffron_proximity_risk_3.set('fieldLabels', {'fid': 'no label', 'terrace_candidate': 'no label', 'area_km2': 'no label', 'mean_elevation': 'no label', 'bare_frac_1994': 'no label', 'bare_frac_2025': 'no label', 'bare_frac_change': 'no label', 'status': 'no label', 'saffron_index': 'no label', 'likely_saffron': 'no label', 'dist_to_nearest_degraded_m': 'no label', 'at_risk': 'no label', });
lyr_settlements_4.set('fieldLabels', {'fid': 'no label', 'name': 'no label', });
lyr_settlements_4.on('precompose', function(evt) {
    evt.context.globalCompositeOperation = 'normal';
});