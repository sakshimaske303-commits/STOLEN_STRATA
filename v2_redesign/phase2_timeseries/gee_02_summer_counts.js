// STOLEN STRATA v2 — Phase 2 (part B): the two exports that failed in gee_01
//   LS_summer_1990_2025   one band per year: June–September median NDVI
//   LS_counts_1990_2025   clear observations per pixel per year (n_YYYY = all year, ns_YYYY = Jun–Sep)
// Same settings as gee_01: 30 m, EPSG:32643, NDVI x 10000 as int16, nodata -32768.
// (gee_01 failed on these two because a calendarRange filter met the undated dummy image.
//  Here summer is cut by date and the dummy is merged in after all filtering.)

var aoi = ee.Geometry.Rectangle([74.75, 33.85, 75.15, 34.15]);
var START = 1990, END = 2025;
var FOLDER = 'StolenStrata_v2';

function qaMask(img) {
  var qa = img.select('QA_PIXEL');
  return qa.bitwiseAnd(1 << 1).eq(0).and(qa.bitwiseAnd(1 << 3).eq(0))
    .and(qa.bitwiseAnd(1 << 4).eq(0)).and(qa.bitwiseAnd(1 << 5).eq(0));
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
function tm(img)   { return toNdvi(img, 'SR_B3', 'SR_B4', false); }
function oliH(img) { return toNdvi(img, 'SR_B4', 'SR_B5', true); }
function ls(id) { return ee.ImageCollection(id).filterBounds(aoi); }
var allLandsat = ls('LANDSAT/LT05/C02/T1_L2').map(tm)
  .merge(ls('LANDSAT/LE07/C02/T1_L2').map(tm))
  .merge(ls('LANDSAT/LC08/C02/T1_L2').map(oliH))
  .merge(ls('LANDSAT/LC09/C02/T1_L2').map(oliH));

var dummy = ee.ImageCollection([ee.Image.constant(0).rename('ndvi').toFloat().updateMask(ee.Image.constant(0))]);
function wholeYear(y) {
  return allLandsat.filterDate(ee.Date.fromYMD(y, 1, 1), ee.Date.fromYMD(y + 1, 1, 1)).merge(dummy);
}
function summerOf(y) {                       // 1 June to 30 September
  return allLandsat.filterDate(ee.Date.fromYMD(y, 6, 1), ee.Date.fromYMD(y, 10, 1)).merge(dummy);
}
function toInt(img) { return img.multiply(10000).round().unmask(-32768).toInt16(); }

var summerBands = [], countBands = [];
for (var y = START; y <= END; y++) {
  summerBands.push(toInt(summerOf(y).reduce(ee.Reducer.median())).rename('summer_' + y));
  countBands.push(wholeYear(y).reduce(ee.Reducer.count()).unmask(0).toInt16().rename('n_' + y));
  countBands.push(summerOf(y).reduce(ee.Reducer.count()).unmask(0).toInt16().rename('ns_' + y));
}
var products = [
  ['LS_summer_1990_2025', ee.Image.cat(summerBands).clip(aoi)],
  ['LS_counts_1990_2025', ee.Image.cat(countBands).clip(aoi)]
];
products.forEach(function (p) {
  Export.image.toDrive({
    image: p[1], description: 'StolenStrata_v2_' + p[0], folder: FOLDER,
    fileNamePrefix: 'StolenStrata_v2_' + p[0],
    region: aoi, scale: 30, crs: 'EPSG:32643', maxPixels: 1e9, fileFormat: 'GeoTIFF'
  });
});
