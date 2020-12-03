#!/usr/bin/env python3
#
############################################################################
#
# MODULE:      v.random.strat.sampling
# AUTHOR(S):   Hajar Benelcadi and Anika Bettge
#
# PURPOSE:     Sampling points from polygon vector data based on random stratified sampling
# COPYRIGHT:   (C) 2019 by Hajar Benelcadi and Anika Bettge, mundialis
#
#              This program is free software under the GNU General Public
#              License (>=v2). Read the file COPYING that comes with GRASS
#              for details.
#
#############################################################################
#%module
#% description: sample data
#% keyword: vector
#% keyword: sampling
#% keyword: statistics
#% keyword: random
#% keyword: point pattern
#% keyword: stratified random sampling
#%end

#%option G_OPT_V_INPUT
#%end

#%option G_OPT_DB_COLUMN
#% description: Name of column with class information
#%end

#%option G_OPT_V_OUTPUT
#%end

#%option
#% key: npoints
#% type: integer
#% required: yes
#% description: Number of points to be created for each class
#% answer: 100
#%end

#%option G_OPT_DB_COLUMN
#% key: intcolumn
#% required: no
#% description: Name of column to create new integer class information
#%end

from grass.script import core as grass
import os


def cleanup(rm_vectors):
    grass.message(_("Cleaning up..."))
    nuldev = open(os.devnull, 'w')
    for rm_v in rm_vectors:
        grass.run_command(
            'g.remove', flags='f', type='vector', name=rm_v, quiet=True, stderr=nuldev)


def main():
    input = options['input']
    output = options['output']
    column = options['column']
    npoints = options['npoints']
    intcolumn = options['intcolumn']

    # sampling
    grass.message("Sampling for each class separately...")
    classes = grass.parse_command(
        'v.db.select', map=input,
        column=column, flags='c')

    class_outputs = []
    for cl in classes:
        random_output = 'v_random_strat_sampling_%s_%s' % (cl.replace('-', '_'), str(os.getpid()))
        where_str = "%s = '%s'" % (column, cl)
        try:
            grass.run_command(
                'v.random', restrict=input, where=where_str, layer='1',
                output=random_output, npoints=npoints)
            class_outputs.append(random_output)
        except:
            grass.fatal("... an error occured!")

    # combine vector data
    grass.message("Combining separately sampled vector data...")
    grass.run_command(
        'v.patch', flags='e', input=','.join(class_outputs), output=output, quiet=True)

    # renameing columns
    tmp_columns_dict = grass.parse_command('v.info', map=output, flags='c')
    tmp_columns = [x.split('|')[1] for x in tmp_columns_dict]
    input_columns_dict = grass.parse_command('v.info', map=input, flags='c')
    input_columns = [x.split('|')[1] for x in input_columns_dict]
    for tmp_col in tmp_columns:
        if tmp_col == "cat":
            continue
        elif tmp_col.endswith("_cat"):
            grass.run_command(
                "v.db.dropcolumn", map=output, columns=tmp_col, quiet=True)
        else:
            for incol in input_columns:
                if tmp_col.endswith("_%s" % incol):
                    grass.run_command(
                        "v.db.renamecolumn", map=output, quiet=True,
                        column="%s,%s" % (tmp_col, incol))

    # create new column for integer values
    if intcolumn:
        grass.run_command(
            'v.db.addcolumn', map=output, columns='%s INT' % intcolumn)
        classcolumnname = '%s_%s' % (input, column)
        for cl, num in zip(classes, range(len(classes))):
            where_str = "%s = '%s'" % (classcolumnname, cl)
            grass.run_command(
                'v.db.update', map=output, column=intcolumn, value=num+1,
                where=where_str, quiet=True)

    cleanup(class_outputs)
    grass.message("Sampling DONE <%s>" % output)


if __name__ == "__main__":
    options, flags = grass.parser()
    main()
