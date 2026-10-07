// STOLEN STRATA v2 — Phase 4 gate test: did the ground actually get lower?
// Paste into the Earth Engine Code Editor, press Run, start all 3 tasks. Files go to Drive folder
// "StolenStrata_v2"; put them in data/raw/ with the others.
//
//   1 DEM_SRTM_2000        SRTM 1 arc-second, surface in February 2000
//   2 DEM_AW3D30_2006_2011 ALOS World 3D 30 m, surface in 2006–2011
//        (the Copernicus DEM already in data/raw is 2011–2015: three epochs, all BEFORE the 2017 kiln field)
//   3 GEDI_ground_2019_2025 GEDI laser ground elevation, one set of bands per year:
//        dz_YYYY  = median of (GEDI ground elevation − TanDEM-X DEM carried in the GEDI product), metres x 100
//        n_YYYY   = number of good laser shots in the 25 m cell that year
//        This is the only free height data AFTER 2017. Shots are sparse (laser tracks), not a full map.

var aoi = ee.Geometry.Rectangle([74.75, 33.85, 75.15, 34.15]);
var FOLDER = 'StolenStrata_v2';

// ---------- 1 and 2: older DEMs ----------
var srtm = ee.Image('USGS/SRTMGL1_003').select('elevation').toFloat().rename('srtm_2000');
var aw3d = ee.ImageCollection('JAXA/ALOS/AW3D30/V3_2').select('DSM').mosaic().toFloat().rename('aw3d_2006_2011');

// ---------- 3: GEDI ----------
function gediPrep(img) {
  var good = img.select('quality_flag').eq(1)
    .and(img.select('degrade_flag').eq(0))
    .and(img.select('sensitivity').gte(0.95));
  var dz = img.select('elev_lowestmode').subtract(img.select('digital_elevation_model'))
    .rename('dz').toFloat();
  return dz.updateMask(good).updateMask(dz.abs().lt(100));   // drop cloud returns and gross blunders
}
var gedi = ee.ImageCollection('LARSE/GEDI/GEDI02_A_002_MONTHLY').filterBounds(aoi);
var dummy = ee.ImageCollection([ee.Image.constant(0).rename('dz').toFloat().updateMask(ee.Image.constant(0))]);

var bands = [];
for (var y = 2019; y <= 2025; y++) {
  var c = gedi.filterDate(ee.Date.fromYMD(y, 1, 1), ee.Date.fromYMD(y + 1, 1, 1)).map(gediPrep).merge(dummy);
  bands.push(c.reduce(ee.Reducer.median()).multiply(100).round().unmask(-32768).toInt16().rename('dz_' + y));
  bands.push(c.reduce(ee.Reducer.count()).unmask(0).toInt16().rename('n_' + y));
}
var gediStack = ee.Image.cat(bands).clip(aoi);

// ---------- exports ----------
Export.image.toDrive({image: srtm.clip(aoi), description: 'StolenStrata_v2_DEM_SRTM_2000', folder: FOLDER,
  fileNamePrefix: 'StolenStrata_v2_DEM_SRTM_2000', region: aoi, scale: 30, crs: 'EPSG:32643', maxPixels: 1e9});
Export.image.toDrive({image: aw3d.clip(aoi), description: 'StolenStrata_v2_DEM_AW3D30_2006_2011', folder: FOLDER,
  fileNamePrefix: 'StolenStrata_v2_DEM_AW3D30_2006_2011', region: aoi, scale: 30, crs: 'EPSG:32643', maxPixels: 1e9});
Export.image.toDrive({image: gediStack, description: 'StolenStrata_v2_GEDI_ground_2019_2025', folder: FOLDER,
  fileNamePrefix: 'StolenStrata_v2_GEDI_ground_2019_2025', region: aoi, scale: 25, crs: 'EPSG:32643', maxPixels: 1e9});

// ---------- quick look ----------
print('GEDI monthly rasters over the box:', gedi.size());
print('GEDI date range:', gedi.aggregate_min('system:time_start'), gedi.aggregate_max('system:time_start'));
Map.centerObject(ee.Geometry.Point([74.848, 33.944]), 14);
Map.addLayer(gedi.map(gediPrep).median(), {min: -15, max: 15, palette: ['#b2182b', '#f7f7f7', '#2166ac']},
  'GEDI ground minus TanDEM-X (m), all years');
