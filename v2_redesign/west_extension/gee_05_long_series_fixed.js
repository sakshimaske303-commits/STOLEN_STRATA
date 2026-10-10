// STOLEN STRATA v2 - long series, recomputed with the Landsat 8/9 adjustment in the right direction
// I paste this into the Earth Engine Code Editor, press Run, then start the one task in the Tasks tab.
// The file goes to Drive folder "StolenStrata_v2"; I put it in data/raw/ next to the others.
//
// gee_04_extended_box.js adjusted Landsat 8/9 with the Roy et al. (2016) ETM+ -> OLI coefficients, i.e. in the
// reverse direction. Here Landsat 8/9 red and NIR are converted to ETM+ with the OLI -> ETM+ coefficients of
// Roy et al. (2016, Table 2, OLS):  ETM+ red = 0.9372 x OLI red + 0.0123;  ETM+ NIR = 0.8339 x OLI NIR + 0.0448.
// Only the 2008-2025 stack contains Landsat 8/9 (from 2013), so only that file is exported again.
// Everything else (box, masks, yearly 90th percentile, int16 = NDVI x 10000, nodata -32768, 30 m, EPSG:32643)
// is exactly as in gee_04_extended_box.js.
//
//   StolenStrata_v2w_LS_p90_2008_2025_fixed   yearly 90th-percentile NDVI, Landsat 5/7/8/9, 8/9 adjusted to ETM+

var aoi = ee.Geometry.Rectangle([74.55, 33.80, 75.15, 34.15]);
var FOLDER = 'StolenStrata_v2';
var PREFIX = 'StolenStrata_v2w_';

function qaMask(img) {
  var qa = img.select('QA_PIXEL');
  return qa.bitwiseAnd(1 << 1).eq(0).and(qa.bitwiseAnd(1 << 3).eq(0))
    .and(qa.bitwiseAnd(1 << 4).eq(0)).and(qa.bitwiseAnd(1 << 5).eq(0));
}
function toNdvi(img, redBand, nirBand, oliToEtm) {
  var red = img.select(redBand).multiply(0.0000275).add(-0.2);
  var nir = img.select(nirBand).multiply(0.0000275).add(-0.2);
  var valid = red.gt(0).and(red.lt(1)).and(nir.gt(0)).and(nir.lt(1));
  if (oliToEtm) {                            // Roy et al. 2016, Table 2, OLI -> ETM+ (OLS)
    red = red.multiply(0.9372).add(0.0123);
    nir = nir.multiply(0.8339).add(0.0448);
  }
  var ndvi = nir.subtract(red).divide(nir.add(red)).rename('ndvi').toFloat();
  return ndvi.updateMask(qaMask(img)).updateMask(valid)
    .set('system:time_start', img.get('system:time_start'));
}
function tm(img)  { return toNdvi(img, 'SR_B3', 'SR_B4', false); }
function oli(img) { return toNdvi(img, 'SR_B4', 'SR_B5', true); }
function ls(id) { return ee.ImageCollection(id).filterBounds(aoi); }

var allLandsat = ls('LANDSAT/LT05/C02/T1_L2').map(tm).merge(ls('LANDSAT/LE07/C02/T1_L2').map(tm))
  .merge(ls('LANDSAT/LC08/C02/T1_L2').map(oli)).merge(ls('LANDSAT/LC09/C02/T1_L2').map(oli));

var dummy = ee.ImageCollection([ee.Image.constant(0).rename('ndvi').toFloat().updateMask(ee.Image.constant(0))]);
function yearCol(col, y) {
  return col.filterDate(ee.Date.fromYMD(y, 1, 1), ee.Date.fromYMD(y + 1, 1, 1)).merge(dummy);
}
function toInt(img) { return img.multiply(10000).round().unmask(-32768).toInt16(); }
function p90Stack(col, y0, y1) {
  var bands = [];
  for (var y = y0; y <= y1; y++) {
    bands.push(toInt(yearCol(col, y).reduce(ee.Reducer.percentile([90]))).rename('p90_' + y));
  }
  return ee.Image.cat(bands).clip(aoi);
}

var img = p90Stack(allLandsat, 2008, 2025);
Export.image.toDrive({
  image: img, description: PREFIX + 'LS_p90_2008_2025_fixed', folder: FOLDER,
  fileNamePrefix: PREFIX + 'LS_p90_2008_2025_fixed',
  region: aoi, scale: 30, crs: 'EPSG:32643', maxPixels: 1e9, fileFormat: 'GeoTIFF'
});

Map.centerObject(aoi, 10);
Map.addLayer(img.select('p90_2020'), {min: 0, max: 8000, palette: ['#8c510a', '#f6e8c3', '#01665e']}, 'p90 NDVI 2020 (fixed)');
