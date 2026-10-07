// STOLEN STRATA v2 — extended study box (old box + Budgam karewa belt to the west and a little south)
// Old box: 74.75–75.15 E, 33.85–34.15 N.   New box: 74.55–75.15 E, 33.80–34.15 N.
// Paste into the Earth Engine Code Editor, press Run, start all 7 tasks. Files go to Drive folder
// "StolenStrata_v2"; put them in data/raw/ with the others. All names start with StolenStrata_v2w_ ("w" = wide box).
//
//   1 DEM_GLO30_buffered     Copernicus DEM, new box + ~10 km buffer (for the terrace delineation)
//   2 LS_p90_1990_2007       yearly 90th-percentile NDVI, Landsat 5/7 (same recipe as before)
//   3 LS_p90_2008_2025       same, Landsat 5/7/8/9 with 8/9 adjusted to ETM+ (split in two to keep files small)
//   4 LS_counts_1990_2025    clear observations per pixel per year
//   5 L7only_p90_2013_2021   Landsat 7 only
//   6 OLIonly_p90_2013_2025  Landsat 8/9 only, not adjusted   <- the series the conversion test uses
//   7 S2_p90_2019_2025       Sentinel-2 only
// NDVI is stored as int16 = NDVI x 10000, nodata -32768; 30 m, EPSG:32643. The summer median is not exported
// again: it proved unusable (too few clear monsoon scenes before 2009).

var aoi = ee.Geometry.Rectangle([74.55, 33.80, 75.15, 34.15]);
var aoiBuf = ee.Geometry.Rectangle([74.45, 33.70, 75.25, 34.25]);
var FOLDER = 'StolenStrata_v2';
var PREFIX = 'StolenStrata_v2w_';

// ---------- Landsat ----------
function qaMask(img) {
  var qa = img.select('QA_PIXEL');
  return qa.bitwiseAnd(1 << 1).eq(0).and(qa.bitwiseAnd(1 << 3).eq(0))
    .and(qa.bitwiseAnd(1 << 4).eq(0)).and(qa.bitwiseAnd(1 << 5).eq(0));
}
function toNdvi(img, redBand, nirBand, harmonizeOli) {
  var red = img.select(redBand).multiply(0.0000275).add(-0.2);
  var nir = img.select(nirBand).multiply(0.0000275).add(-0.2);
  var valid = red.gt(0).and(red.lt(1)).and(nir.gt(0)).and(nir.lt(1));
  if (harmonizeOli) {                        // Roy et al. 2016, OLI -> ETM+
    red = red.multiply(0.9047).add(0.0061);
    nir = nir.multiply(0.8462).add(0.0412);
  }
  var ndvi = nir.subtract(red).divide(nir.add(red)).rename('ndvi').toFloat();
  return ndvi.updateMask(qaMask(img)).updateMask(valid)
    .set('system:time_start', img.get('system:time_start'));
}
function tm(img)     { return toNdvi(img, 'SR_B3', 'SR_B4', false); }
function oliH(img)   { return toNdvi(img, 'SR_B4', 'SR_B5', true); }
function oliRaw(img) { return toNdvi(img, 'SR_B4', 'SR_B5', false); }
function ls(id) { return ee.ImageCollection(id).filterBounds(aoi); }

var l7 = ls('LANDSAT/LE07/C02/T1_L2').map(tm);
var allLandsat = ls('LANDSAT/LT05/C02/T1_L2').map(tm).merge(l7)
  .merge(ls('LANDSAT/LC08/C02/T1_L2').map(oliH)).merge(ls('LANDSAT/LC09/C02/T1_L2').map(oliH));
var oliOnly = ls('LANDSAT/LC08/C02/T1_L2').map(oliRaw).merge(ls('LANDSAT/LC09/C02/T1_L2').map(oliRaw));

// ---------- Sentinel-2 ----------
var csPlus = ee.ImageCollection('GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED');
var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(aoi)
  .linkCollection(csPlus, ['cs_cdf'])
  .map(function (img) {
    var ndvi = img.normalizedDifference(['B8', 'B4']).rename('ndvi').toFloat();
    return ndvi.updateMask(img.select('cs_cdf').gte(0.6))
      .set('system:time_start', img.get('system:time_start'));
  });

// ---------- yearly stacks (the dummy is merged in after all date filtering) ----------
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
function countStack(col, y0, y1) {
  var bands = [];
  for (var y = y0; y <= y1; y++) {
    bands.push(yearCol(col, y).reduce(ee.Reducer.count()).unmask(0).toInt16().rename('n_' + y));
  }
  return ee.Image.cat(bands).clip(aoi);
}

var products = [
  ['LS_p90_1990_2007',      p90Stack(allLandsat, 1990, 2007)],
  ['LS_p90_2008_2025',      p90Stack(allLandsat, 2008, 2025)],
  ['LS_counts_1990_2025',   countStack(allLandsat, 1990, 2025)],
  ['L7only_p90_2013_2021',  p90Stack(l7, 2013, 2021)],
  ['OLIonly_p90_2013_2025', p90Stack(oliOnly, 2013, 2025)],
  ['S2_p90_2019_2025',      p90Stack(s2, 2019, 2025)]
];
products.forEach(function (p) {
  Export.image.toDrive({
    image: p[1], description: PREFIX + p[0], folder: FOLDER, fileNamePrefix: PREFIX + p[0],
    region: aoi, scale: 30, crs: 'EPSG:32643', maxPixels: 1e9, fileFormat: 'GeoTIFF'
  });
});

// ---------- DEM ----------
var dem = ee.ImageCollection('COPERNICUS/DEM/GLO30').select('DEM').mosaic().toFloat().clip(aoiBuf);
Export.image.toDrive({
  image: dem, description: PREFIX + 'DEM_GLO30_buffered', folder: FOLDER, fileNamePrefix: PREFIX + 'DEM_GLO30_buffered',
  region: aoiBuf, scale: 30, crs: 'EPSG:4326', maxPixels: 1e9, fileFormat: 'GeoTIFF'
});

// ---------- quick look ----------
Map.centerObject(aoi, 10);
Map.addLayer(ee.Image().paint(aoi, 1, 2), {palette: ['#00e5ff']}, 'new box');
Map.addLayer(ee.Image().paint(ee.Geometry.Rectangle([74.75, 33.85, 75.15, 34.15]), 1, 2), {palette: ['#ffd400']}, 'old box');
