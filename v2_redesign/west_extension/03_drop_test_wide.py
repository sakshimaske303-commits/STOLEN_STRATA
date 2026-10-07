"""v2 extended box — second, less strict conversion test.

The strict test (p90 NDVI >= 0.35 in all early years, < 0.25 in all late years) misses most brick-kiln land: at 30 m
kiln fields are mixed pixels with weeds and sit at p90 0.25-0.45, not below 0.25. This test uses the size of the drop:
    median p90 of 2013-15 >= 0.45, median p90 of the late window < 0.40, and a fall of at least 0.20.
It catches more real change and more noise, so every figure is given with the reverse change (the same rule run
backwards) and for the two comparison strata.

Run from the repo root:  python v2_redesign/west_extension/03_drop_test_wide.py
Writes drop_test_by_stratum_wide.csv, drop_test_by_terrace_wide.csv, low_ndvi_stock_wide.csv
"""
import rasterio, numpy as np, geopandas as gpd, pandas as pd
from rasterio.features import rasterize
from rasterio.warp import transform as wxy
from shapely.geometry import box
R='data/raw/StolenStrata_v2w_'
def load(n):
    s=rasterio.open(R+n); a=s.read().astype('float32'); a[a==-32768]=np.nan; return s,{int(d[-4:]):a[i]/1e4 for i,d in enumerate(s.descriptions)}
s,OLI=load('OLIonly_p90_2013_2025.tif'); _,L7=load('L7only_p90_2013_2021.tif'); _,S2=load('S2_p90_2019_2025.tif')
T=s.transform
t=gpd.read_file('v2_redesign/west_extension/karewa_terraces_wide.gpkg').to_crs(s.crs)
p=gpd.read_file('v2_redesign/west_extension/karewa_flat_tops_wide.gpkg').to_crs(s.crs)
tid=rasterize([(g,int(i)) for g,i in zip(t.geometry,t.terrace_id)],out_shape=s.shape,transform=T); mt=tid>0
mf=(rasterize([(g,1) for g in p.geometry],out_shape=s.shape,transform=T)==1)&~mt
old=gpd.GeoSeries([box(74.75,33.85,75.15,34.15)],crs=4326).to_crs(s.crs).iloc[0]
mo=rasterize([(old,1)],out_shape=s.shape,transform=T)==1
def med(D,ys): return np.median([D[y] for y in ys],0)
def drop(D,e,l,dmin=.20,lmax=.40,emin=.45):
    a,b=med(D,e),med(D,l); return (a>=emin)&(b<lmax)&(a-b>=dmin), (b>=emin)&(a<lmax)&(b-a>=dmin)
res={}; ROWS=[]
for nm,D,e,l in [('OLI 13-15>23-25',OLI,(2013,2014,2015),(2023,2024,2025)),('OLI 13-15>19-21',OLI,(2013,2014,2015),(2019,2020,2021)),('L7 13-15>19-21',L7,(2013,2014,2015),(2019,2020,2021))]:
    c,r=drop(D,e,l); res[nm]=c
    for part,pm in [('old',mo),('ext',~mo)]:
        for sn,sm in [('terraces',mt),('other_flat',mf),('rest',~mt&~mf)]:
            ROWS.append(dict(test=nm,part=part,stratum=sn,drop_ha=c[sm&pm].sum()*.09,drop_pct=c[sm&pm].mean()*100,reverse_ha=r[sm&pm].sum()*.09,net_ha=(c[sm&pm].sum()-r[sm&pm].sum())*.09))
        print(nm,part,'| terr %.1f ha (%.2f%%) rev %.1f | flat %.1f ha (%.2f%%) rev %.1f | rest %.1f ha (%.2f%%) rev %.1f'%(
          c[mt&pm].sum()*.09,c[mt&pm].mean()*100,r[mt&pm].sum()*.09,c[mf&pm].sum()*.09,c[mf&pm].mean()*100,r[mf&pm].sum()*.09,
          c[~mt&~mf&pm].sum()*.09,c[~mt&~mf&pm].mean()*100,r[~mt&~mf&pm].sum()*.09))
c=res['OLI 13-15>23-25']
a=res['OLI 13-15>19-21']; b=res['L7 13-15>19-21']; print('L7 agrees on %.0f%% of OLI drop px on terraces (to 2019-21)'%(b[a&mt].mean()*100))
s2l=med(S2,(2023,2024,2025)); print('S2 late median on dropped terrace px: %.2f ; share <0.40: %.0f%%'%(np.nanmedian(s2l[c&mt]),(s2l[c&mt]<.40).mean()*100))
per=pd.Series(tid[c&mt]).value_counts()*.09
per=t.set_index('terrace_id')[['area_km2']].join(per.rename('ha')).fillna(0); per['pct']=per.ha/per.area_km2
pt=t.set_index('terrace_id').representative_point().to_crs(4326); per['lat']=pt.y.round(3); per['lon']=pt.x.round(3)
OUT='v2_redesign/west_extension/'; pd.DataFrame(ROWS).round(2).to_csv(OUT+'drop_test_by_stratum_wide.csv',index=False); per.sort_values('ha',ascending=False).round(3).to_csv(OUT+'drop_test_by_terrace_wide.csv'); STK=[]
print(per.sort_values('ha',ascending=False).head(15).round(2)); print('terraces >=1ha:',(per.ha>=1).sum(),'>=5ha:',(per.ha>=5).sum(),'total',per.ha.sum())
# stock: late median < 0.40 / <0.35
for thr in (.30,.35,.40):
    for nm,ys in [('2013-15',(2013,2014,2015)),('2018-20',(2018,2019,2020)),('2023-25',(2023,2024,2025))]:
        m=med(OLI,ys)<thr
        STK.append(dict(p90_below=thr,years=nm,old_box_terraces_ha=m[mt&mo].sum()*.09,old_box_terraces_pct=m[mt&mo].mean()*100,extension_terraces_ha=m[mt&~mo].sum()*.09,extension_terraces_pct=m[mt&~mo].mean()*100,other_flat_pct=m[mf].mean()*100,rest_pct=m[~mt&~mf].mean()*100))
        print('stock p90med<%.2f'%thr,nm,'| old terr %.0f ha (%.2f%%) | ext terr %.0f ha (%.2f%%) | flat %.2f%% | rest %.2f%%'%(m[mt&mo].sum()*.09,m[mt&mo].mean()*100,m[mt&~mo].sum()*.09,m[mt&~mo].mean()*100,m[mf].mean()*100,m[~mt&~mf].mean()*100))
pd.DataFrame(STK).round(2).to_csv(OUT+'low_ndvi_stock_wide.csv',index=False)
