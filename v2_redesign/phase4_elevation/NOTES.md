# v2 Phase 4 — elevation gate test (2 Oct 2026): FAILED with free data

Question: can freely available height data show the ground lowering on the 89 ha converted block (Phase 2)?

- **DEMs are all too early.** SRTM (2000), AW3D30 (2006–11) and Copernicus (2011–15) all predate the 2017 onset.
  Their differences on the converted block match the unconverted rest of terraces 5 and 3 to within noise
  (NMAD 0.6–1.3 m), as expected: nothing had happened yet.
- **GEDI (2019–2025) has almost no shots there.** 9 cells with good shots on the converted block, all from 2019,
  none in any later year. Median GEDI − TanDEM-X: −0.32 m on those 9, −0.49 m on the unconverted part of the same
  terraces that year. No detectable lowering, but 9 shots cannot support any conclusion either way.
- GEDI itself is precise enough on the flat terrace tops (NMAD about 0.7 m), so the limit is coverage, not accuracy.

Verdict: the paper cannot make a volume or depth claim. It can say "vegetated → persistently bare", not "excavated".

What could still be tried: ICESat-2 ATL08 tracks (2018–2025, needs a NASA Earthdata download), or a recent
stereo / commercial DEM. Neither is in hand.
