var wms_layers = [];


        var lyr_ESRIGraydark_0 = new ol.layer.Tile({
            'title': 'ESRI Gray (dark)',
            'opacity': 1.000000,
            
            
            source: new ol.source.XYZ({
            attributions: ' ',
                url: 'https://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}'
            })
        });
var format_karewa_candidates_filtered_1 = new ol.format.GeoJSON();
var features_karewa_candidates_filtered_1 = format_karewa_candidates_filtered_1.readFeatures(json_karewa_candidates_filtered_1, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_karewa_candidates_filtered_1 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_karewa_candidates_filtered_1.addFeatures(features_karewa_candidates_filtered_1);
var lyr_karewa_candidates_filtered_1 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_karewa_candidates_filtered_1, 
                style: style_karewa_candidates_filtered_1,
                popuplayertitle: 'karewa_candidates_filtered',
                interactive: true,
                title: '<img src="styles/legend/karewa_candidates_filtered_1.png" /> karewa_candidates_filtered'
            });
var format_settlements_2 = new ol.format.GeoJSON();
var features_settlements_2 = format_settlements_2.readFeatures(json_settlements_2, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_settlements_2 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_settlements_2.addFeatures(features_settlements_2);
var lyr_settlements_2 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_settlements_2, 
                style: style_settlements_2,
                popuplayertitle: 'settlements',
                interactive: true,
                title: '<img src="styles/legend/settlements_2.png" /> settlements'
            });

lyr_ESRIGraydark_0.setVisible(true);lyr_karewa_candidates_filtered_1.setVisible(true);lyr_settlements_2.setVisible(true);
var layersList = [lyr_ESRIGraydark_0,lyr_karewa_candidates_filtered_1,lyr_settlements_2];
lyr_karewa_candidates_filtered_1.set('fieldAliases', {'fid': 'fid', 'terrace_candidate': 'terrace_candidate', 'area_km2': 'area_km2', 'mean_elevation': 'mean_elevation', });
lyr_settlements_2.set('fieldAliases', {'fid': 'fid', 'name': 'name', });
lyr_karewa_candidates_filtered_1.set('fieldImages', {'fid': 'TextEdit', 'terrace_candidate': 'TextEdit', 'area_km2': 'TextEdit', 'mean_elevation': 'TextEdit', });
lyr_settlements_2.set('fieldImages', {'fid': 'TextEdit', 'name': 'TextEdit', });
lyr_karewa_candidates_filtered_1.set('fieldLabels', {'fid': 'no label', 'terrace_candidate': 'no label', 'area_km2': 'no label', 'mean_elevation': 'no label', });
lyr_settlements_2.set('fieldLabels', {'fid': 'no label', 'name': 'no label', });
lyr_settlements_2.on('precompose', function(evt) {
    evt.context.globalCompositeOperation = 'normal';
});