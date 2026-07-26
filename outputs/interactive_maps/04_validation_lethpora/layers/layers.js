var wms_layers = [];


        var lyr_ESRISatellite_0 = new ol.layer.Tile({
            'title': 'ESRI Satellite',
            'opacity': 1.000000,
            
            
            source: new ol.source.XYZ({
            attributions: ' ',
                url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
            })
        });
var format_karewa_saffron_overlay_1 = new ol.format.GeoJSON();
var features_karewa_saffron_overlay_1 = format_karewa_saffron_overlay_1.readFeatures(json_karewa_saffron_overlay_1, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_karewa_saffron_overlay_1 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_karewa_saffron_overlay_1.addFeatures(features_karewa_saffron_overlay_1);
var lyr_karewa_saffron_overlay_1 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_karewa_saffron_overlay_1, 
                style: style_karewa_saffron_overlay_1,
                popuplayertitle: 'karewa_saffron_overlay',
                interactive: true,
                title: '<img src="styles/legend/karewa_saffron_overlay_1.png" /> karewa_saffron_overlay'
            });
var format_karewa_candidates_filtered_2 = new ol.format.GeoJSON();
var features_karewa_candidates_filtered_2 = format_karewa_candidates_filtered_2.readFeatures(json_karewa_candidates_filtered_2, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_karewa_candidates_filtered_2 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_karewa_candidates_filtered_2.addFeatures(features_karewa_candidates_filtered_2);
var lyr_karewa_candidates_filtered_2 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_karewa_candidates_filtered_2, 
                style: style_karewa_candidates_filtered_2,
                popuplayertitle: 'karewa_candidates_filtered',
                interactive: true,
                title: '<img src="styles/legend/karewa_candidates_filtered_2.png" /> karewa_candidates_filtered'
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

lyr_ESRISatellite_0.setVisible(true);lyr_karewa_saffron_overlay_1.setVisible(true);lyr_karewa_candidates_filtered_2.setVisible(true);lyr_settlements_3.setVisible(true);
var layersList = [lyr_ESRISatellite_0,lyr_karewa_saffron_overlay_1,lyr_karewa_candidates_filtered_2,lyr_settlements_3];
lyr_karewa_saffron_overlay_1.set('fieldAliases', {'fid': 'fid', 'terrace_candidate': 'terrace_candidate', 'area_km2': 'area_km2', 'mean_elevation': 'mean_elevation', 'bare_frac_1994': 'bare_frac_1994', 'bare_frac_2025': 'bare_frac_2025', 'bare_frac_change': 'bare_frac_change', 'status': 'status', 'saffron_index': 'saffron_index', 'likely_saffron': 'likely_saffron', });
lyr_karewa_candidates_filtered_2.set('fieldAliases', {'fid': 'fid', 'terrace_candidate': 'terrace_candidate', 'area_km2': 'area_km2', 'mean_elevation': 'mean_elevation', });
lyr_settlements_3.set('fieldAliases', {'fid': 'fid', 'name': 'name', });
lyr_karewa_saffron_overlay_1.set('fieldImages', {'fid': 'TextEdit', 'terrace_candidate': 'TextEdit', 'area_km2': 'TextEdit', 'mean_elevation': 'TextEdit', 'bare_frac_1994': 'TextEdit', 'bare_frac_2025': 'TextEdit', 'bare_frac_change': 'TextEdit', 'status': 'TextEdit', 'saffron_index': 'TextEdit', 'likely_saffron': 'CheckBox', });
lyr_karewa_candidates_filtered_2.set('fieldImages', {'fid': 'TextEdit', 'terrace_candidate': 'TextEdit', 'area_km2': 'TextEdit', 'mean_elevation': 'TextEdit', });
lyr_settlements_3.set('fieldImages', {'fid': 'TextEdit', 'name': 'TextEdit', });
lyr_karewa_saffron_overlay_1.set('fieldLabels', {'fid': 'no label', 'terrace_candidate': 'no label', 'area_km2': 'no label', 'mean_elevation': 'no label', 'bare_frac_1994': 'no label', 'bare_frac_2025': 'no label', 'bare_frac_change': 'no label', 'status': 'no label', 'saffron_index': 'no label', 'likely_saffron': 'no label', });
lyr_karewa_candidates_filtered_2.set('fieldLabels', {'fid': 'no label', 'terrace_candidate': 'no label', 'area_km2': 'no label', 'mean_elevation': 'no label', });
lyr_settlements_3.set('fieldLabels', {'fid': 'no label', 'name': 'no label', });
lyr_settlements_3.on('precompose', function(evt) {
    evt.context.globalCompositeOperation = 'normal';
});