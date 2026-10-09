// NOTE: exports 2 and 3 (LS_summer, LS_counts) failed from this script in Earth Engine; they were
// produced with gee_02_summer_counts.js. Exports 1, 4, 5, 6 ran from this script as written.
// STOLEN STRATA v2 — Phase 2: annual single-sensor-family NDVI composites, 1990–2025
// Paste into the Earth Engine Code Editor, press Run, then start all 6 tasks in the Tasks tab.
// Files land in Google Drive folder "StolenStrata_v2". Put them in:  data/raw/v2/
//
// What it exports (all 30 m, EPSG:32643, study box only, NDVI stored as int16 = NDVI x 10000, nodata -32768)
//   1 LS_p90_1990_2025        one band per year: 90th percentile of NDVI over the whole year
//                             (a pixel that is bare ALL year has a low yearly maximum; a saffron or
//                             crop field that is bare only in summer does not)
//   2 LS_summer_1990_2025     one band per year: June–September median NDVI (comparable to v1)
//   3 LS_counts_1990_2025     clear observations per pixel per year (n_YYYY = all year, ns_YYYY = Jun–Sep)
//   4 L7only_p90_2013_2021    Landsat 7 only     } same years, different sensors: measures the
//   5 OLIonly_p90_2013_2025   Landsat 8/9 only   } sensor effect directly on the terraces
//   6 S2_p90_2019_2025        Sentinel-2 only (cross-check of the recent years)
//
// Landsat 5/7/8/9 Collection 2 Level 2 surface reflectance. In exports 1–3, Landsat 8/9 red and NIR are
// adjusted to Landsat 7 ETM+ with the Roy et al. (2016) coefficients so the series is one sensor family.
// Export 5 is NOT adjusted (raw OLI), so 4 vs 5 shows the raw sensor difference.

var aoi = ee.Geometry.Rectangle([74.75, 33.85, 75.15, 34.15]);
var START = 1990, END = 2025;
var FOLDER = 'StolenStrata_v2';

// ---------- Landsat preparation ----------
function qaMask(img) {
  var qa = img.select('QA_PIXEL');
  return qa.bitwiseAnd(1 << 1).eq(0)        // dilated cloud
    .and(qa.bitwiseAnd(1 << 3).eq(0))       // cloud
    .and(qa.bitwiseAnd(1 << 4).eq(0))       // cloud shadow
    .and(qa.bitwiseAnd(1 << 5).eq(0));      // snow
}
function toNdvi(img, redBand, nirBand, harmonizeOli) {
  var red = img.select(redBand).multiply(0.0000275).add(-0.2);
  var nir = img.select(nirBand).multiply(0.0000275).add(-0.2);
  var valid = red.gt(0).and(red.lt(1)).and(nir.gt(0)).and(nir.lt(1));
  // KNOWN ISSUE (found 9 Oct 2026): the two lines below use the coefficients Roy et al. (2016) give for
  // ETM+ -> OLI, but here they are applied to OLI data, i.e. in the reverse direction. They are left unchanged
  // so this script still reproduces the rasters behind the reported long series. To correct it, replace them
  // with the OLI -> ETM+ coefficients of Roy et al. (2016, Table 2), re-export, and rerun 08_long_series_wide.py.
  // The conversion tests use the unadjusted Landsat 8/9 series (oliRaw) and are not affected.
  if (harmonizeOli) {                        // Roy et al. 2016 ETM+ -> OLI coefficients (see note above)
    red = red.multiply(0.9047).add(0.0061);
    nir = nir.multiply(0.8462).add(0.0412);
  }
  var ndvi = nir.subtract(red).divide(nir.add(red)).rename('ndvi').toFloat();
  return ndvi.updateMask(qaMask(img)).updateMask(valid)
    .set('system:time_start', img.get('system:time_start'));
}
function tm(img)     { return toNdvi(img, 'SR_B3', 'SR_B4', false); }   // Landsat 5 and 7
function oliH(img)   { return toNdvi(img, 'SR_B4', 'SR_B5', true); }    // Landsat 8/9, adjusted to ETM+
function oliRaw(img) { return toNdvi(img, 'SR_B4', 'SR_B5', false); }   // Landsat 8/9, not adjusted

function ls(id) { return ee.ImageCollection(id).filterBounds(aoi); }
var l5 = ls('LANDSAT/LT05/C02/T1_L2').map(tm);
var l7 = ls('LANDSAT/LE07/C02/T1_L2').map(tm);
var l8h = ls('LANDSAT/LC08/C02/T1_L2').map(oliH);
var l9h = ls('LANDSAT/LC09/C02/T1_L2').map(oliH);
var l8r = ls('LANDSAT/LC08/C02/T1_L2').map(oliRaw);
var l9r = ls('LANDSAT/LC09/C02/T1_L2').map(oliRaw);

var allLandsat = l5.merge(l7).merge(l8h).merge(l9h);
var oliOnly = l8r.merge(l9r);

// ---------- Sentinel-2 (Cloud Score+) ----------
var csPlus = ee.ImageCollection('GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED');
var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(aoi)
  .linkCollection(csPlus, ['cs_cdf'])
  .map(function (img) {
    var ndvi = img.normalizedDifference(['B8', 'B4']).rename('ndvi').toFloat();
    return ndvi.updateMask(img.select('cs_cdf').gte(0.6))
      .set('system:time_start', img.get('system:time_start'));
  });

// ---------- yearly composites ----------
// A fully masked dummy image keeps the band present in years with no data (the band is then all nodata).
// It carries a January-1970 timestamp so the June–September calendar filter can read it (and drops it).
var dummy = ee.ImageCollection([ee.Image.constant(0).rename('ndvi').toFloat().updateMask(ee.Image.constant(0))
  .set('system:time_start', 0)]);

function yearCol(col, y) {
  return col.filterDate(ee.Date.fromYMD(y, 1, 1), ee.Date.fromYMD(y + 1, 1, 1)).merge(dummy);
}
function summer(col) { return col.filter(ee.Filter.calendarRange(6, 9, 'month')).merge(dummy); }

function toInt(img) { return img.multiply(10000).round().unmask(-32768).toInt16(); }

function stack(col, y0, y1, kind) {
  var bands = [];
  for (var y = y0; y <= y1; y++) {
    var c = yearCol(col, y);
    var img;
    if (kind === 'p90') {
      img = toInt(c.reduce(ee.Reducer.percentile([90]))).rename('p90_' + y);
    } else if (kind === 'summer') {
      img = toInt(summer(c).reduce(ee.Reducer.median())).rename('summer_' + y);
    } else {                                   // counts
      var n = c.reduce(ee.Reducer.count()).unmask(0).toInt16().rename('n_' + y);
      var ns = summer(c).reduce(ee.Reducer.count()).unmask(0).toInt16().rename('ns_' + y);
      img = n.addBands(ns);
    }
    bands.push(img);
  }
  return ee.Image.cat(bands).clip(aoi);
}

var products = [
  ['LS_p90_1990_2025',      stack(allLandsat, START, END, 'p90')],
  ['LS_summer_1990_2025',   stack(allLandsat, START, END, 'summer')],
  ['LS_counts_1990_2025',   stack(allLandsat, START, END, 'counts')],
  ['L7only_p90_2013_2021',  stack(l7, 2013, 2021, 'p90')],
  ['OLIonly_p90_2013_2025', stack(oliOnly, 2013, END, 'p90')],
  ['S2_p90_2019_2025',      stack(s2, 2019, END, 'p90')]
];

products.forEach(function (p) {
  Export.image.toDrive({
    image: p[1], description: 'StolenStrata_v2_' + p[0], folder: FOLDER,
    fileNamePrefix: 'StolenStrata_v2_' + p[0],
    region: aoi, scale: 30, crs: 'EPSG:32643', maxPixels: 1e9, fileFormat: 'GeoTIFF'
  });
});

// ---------- quick look in the Code Editor ----------
print('Scenes over the box — Landsat 5:', l5.size(), 'Landsat 7:', l7.size(), 'Landsat 8:', l8h.size(), 'Landsat 9:', l9h.size());
print('Landsat scenes per year (all sensors):',
  ee.List.sequence(START, END).map(function (y) {
    y = ee.Number(y);
    return y.format('%d').cat(': ').cat(
      ee.Number(allLandsat.filterDate(ee.Date.fromYMD(y, 1, 1), ee.Date.fromYMD(y.add(1), 1, 1)).size()).format('%d'));
  }));
Map.centerObject(aoi, 11);
var vis = {min: 0, max: 8000, palette: ['#8c510a', '#d8b365', '#f6e8c3', '#c7eae5', '#5ab4ac', '#01665e']};
Map.addLayer(products[0][1].select('p90_1995'), vis, 'p90 NDVI 1995');
Map.addLayer(products[0][1].select('p90_2015'), vis, 'p90 NDVI 2015');
Map.addLayer(products[0][1].select('p90_2025'), vis, 'p90 NDVI 2025');
