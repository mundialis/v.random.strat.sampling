#!/usr/bin/env python3
#
############################################################################
#
# MODULE:      v.random.strat.sampling
# AUTHOR(S):   Hajar Benelcadi, <benelcadi at mundialis.de>
#
# PURPOSE:     sampling polygon vector data in another points vector data based on random stratified sampling
# COPYRIGHT:   (C) 2019 by Anika Bettge, mundialis
#
#              This program is free software under the GNU General Public
#              License (>=v2). Read the file COPYING that comes with GRASS
#              for details.
#
#############################################################################
#%Module
#% description: sample data
#% keyword: display
#% keyword: raster
#%End


from grass.script import core as grass

def main():
```
# import vector data in grass
v.in.ogr in=/home/hbenelcadi/geodata_dav/projekte/incora_test_Dortmund/auxilliary_data/training_data_ILS/incora_dortmund_LULC_training_merged_EPSG32632.gpkg out=d_p_36236 --o

# reproject data if not in the correct projection (in this case it was already done)
v.proj in=d_p_36236 location=Dortmund_UTM32N mapset=PERMANENT

# visualise vector table
v.db.select map=d_p_36236

# sampling
v.random restrict=d_p_36236 output=d_p_36236_tree_shrubs npoints=500 where="lulc = 'tree_shrubs'" --o
v.random restrict=d_p_36236 output=d_p_36236_water npoints=500 where="lulc = 'water'" --o
v.random restrict=d_p_36236 output=d_p_36236_non_tree_vegetation npoints=500 where="lulc = 'non_tree_vegetation'" --o
v.random restrict=d_p_36236 output=d_p_36236_built_up npoints=500 where="lulc = 'built_up'" --o

# combine vector data
v.patch -e in=d_p_36236_tree_shrubs,d_p_36236_water,d_p_36236_non_tree_vegetation,d_p_36236_built_up out=d_p_36236_sampled_all

# export in GPKG
v.out.ogr -s input=d_p_36236_sampled_all type=point output=/home/hbenelcadi/geodata_dav/projekte/incora_test_Dortmund/auxilliary_data/training_data_ILS/incora_dortmund_LULC_training_merged_sampled_all_EPSG36236.gpkg --o
```

    vectorlist = grass.parse_command('g.list', type='vector', pattern='*B*_10m')
    for rast_mapset in rasterlist_10m:
        rast = rast_mapset.split('@')[0]
        grass.run_command('g.rename', raster=rast + ',' + rast[-7:-4])

    rasterlist_20m = grass.parse_command('g.list', type='raster', pattern='*B*_20m')
    for rast_mapset in rasterlist_20m:
        rast = rast_mapset.split('@')[0]
        r_10m = rast[:-3] + '10m'
        if not r_10m in rasterlist_10m:
            grass.run_command('g.rename', raster=rast + ',' + rast[-7:-4])
        else:
            grass.run_command('g.remove', type='raster', name=rast, flags='f')

    rasterlist_60m = grass.parse_command('g.list', type='raster', pattern='*B*_60m')
    for rast_mapset in rasterlist_60m:
        rast = rast_mapset.split('@')[0]
        r_10m = rast[:-3] + '10m'
        r_20m = rast[:-3] + '20m'
        if not r_10m in rasterlist_10m and not r_20m in rasterlist_20m:
            grass.run_command('g.rename', raster=rast + ',' + rast[-7:-4])
        else:
            grass.run_command('g.remove', type='raster', name=rast, flags='f')


    grass.message('sampling DONE.')


if __name__ == "__main__":
    options, flags = grass.parser()
    main()
