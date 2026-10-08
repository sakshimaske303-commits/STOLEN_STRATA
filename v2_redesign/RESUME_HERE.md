# Where the work stands: 7 October 2026, late evening

## Start here tomorrow

The second accuracy sample is two thirds labelled. 27 of its 120 points are left. Finish them, then the two samples are pooled
and the paper, summary, dashboard and portfolios get the new numbers.

**Files, all in `v2_redesign/west_extension/`**
- `accuracy_sample2_points.kml`: open in Google Earth Pro. Points 121 to 240.
- `accuracy_sample2_labels_in_progress.csv`: the record so far. 93 points confirmed, 2 marked `recheck`.
- `accuracy_sample2_key.csv`: which stratum each point belongs to. **Do not open until all 120 are labelled.**

**How each point is labelled (same as today)**
Two screenshots per place: the old image and the newest one. Switch the Roads layer off.
- Old image: slider on 9/2014. Read the date from the status bar, not the slider. April and June images show ploughed
  fields and do not settle "vegetated"; use September.
- Newest image: slider fully to the right. Read the date from the status bar; at many places the newest image is 2022 or 2023.
- Recorded per point: `before_label` (vegetated / not_vegetated), `now_class` (kiln = inside a kiln field, vegetated, built_up,
  road, bare_other), the two dates, and what is seen. For this sample only "inside a kiln field: yes or no" is recorded,
  not the close-zoom split of the first sample.

**The 27 points left**

A. One-word answers, no screenshot needed (9)
| Point | Question |
|---|---|
| 160 | 2014: bare construction ground or green scrub? |
| 165 | 2014 and now: house, trees or field? |
| 177 | both dates: on the road or on the ground beside it? |
| 180 | both dates: trees or road? |
| 184 | both dates: grass, pale strip or runway? |
| 191 | both dates: road, grass verge or drain? |
| 201, 215 | 2014: on the dirt track or on grass? |
| 210 | 2014: green or bare? (now: bare vacant plot among new houses) |

B. Need the 9/2014 image, the earlier one was April or June with ploughed fields (9)
123, 134, 173, 189, 198, 203, 217, 223, 233. For all of these the present state is already clear (kiln field, except 173 and 134).

C. Need a close view from directly above, both dates (7)
161, 164, 181, 186, 205, 234, 236. For 181 both images so far were winter images; use summer ones.

D. Re-check on the image of 28 July 2026 (2)
140, 154. Recorded as inside the kiln field from the July 2026 image, but on the image of 10 May 2023 both were still green
fields. Look again with the slider fully right: kiln ground or field?

**Things noticed while labelling, to check against the numbers once the key is opened**
- New kiln fields on land that was fields or orchard in 2013-2015 at several places outside the two belts named in the paper
  (points 238; 168 and 203; 233; 139; 125, 171, 197, 226 at Sholipora; 127, 135, 142, 150; 189 and 223 at Charangam).
- Existing kiln fields spreading over neighbouring orchard and fields (129, 137, 147, 159, 190, 196, and 148 and 195 across a gully).
  On the Bandagam side this happened after 2014, which the paper currently calls the older and slower belt.
- Reasons other than kilns: buildings and yards on the airfield and in settlements (169, 172, 176, 219, 230, 231), a road
  corridor (221, 224), paddy or grass turned into young orchard with bare soil between small trees (124, 149, 163, 183),
  saffron land that is bare in every summer image (152, 193), cleared ground with no kiln in view (128, 187).

## After the 120 are done
1. Open the key, pool with the first sample (60 strict, 120 drop-only, 60 unflagged), rerun the estimates.
2. Update paper Section 3.5 and 4.5, the limitations, abstract and conclusion; executive summary; README; dashboard; both portfolios.
3. Development Log entry (this is an addition to the research).
4. Then the remaining optional work: kiln-field outlines drawn by hand for an independent area figure; geology check west
   of 74.66 E; a second labeller; the 460-point terrace sample.

## Not yet pushed
STOLEN_STRATA, GEOSPATIAL-PORTFOLIO and Satellite-Econometrics-Portfolio all have changes from 7 October that are on disk
and not on GitHub: the before check of the first sample (Table 4), the district kiln list, the removed-flat-tops check,
corrected source statements, the root Streamlit theme, and the files of the second sample.

## Done on 7 October
- Before check of the 85 flagged points of the first sample: 72 vegetated in 2013-2014 imagery, 12 not, 1 unclear; kiln
  estimate restricted to points vegetated before is about 134 ha (`accuracy_before_pass.csv`, `10_before_check_result.py`).
- The flat tops removed by review hold 0.09 ha of strict conversion and none by the drop test (`11_removed_flat_tops_check.py`).
- Sources: the tribunal filing (OA 364/2024) and the district list of kilns (OA 594/2022, 4 October 2023) read in full; press
  reports checked against extracts; six statements corrected. The district list names kilns in the Bandagam-Batapora villages.
- Second sample drawn (`12_accuracy_sample_supplement.py`) and 93 of 120 points labelled.
