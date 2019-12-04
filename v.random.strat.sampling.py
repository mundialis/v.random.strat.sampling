#!/usr/bin/env python3
#
############################################################################
#
# MODULE:      v.random.strat.sampling
# AUTHOR(S):   Hajar Benelcadi and Anika Bettge
#
# PURPOSE:     sampling polygon vector data in another points vector data based on random stratified sampling
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
#% description: Name of input vector map
#% required : yes
#%end

#%option G_OPT_DB_COLUMN
#% key: column
#% description: Name of column with class information
#% required : yes
#%end

#%option G_OPT_V_OUTPUT
#% key: output
#% description: Name of output vector map
#% required : yes
#%end

#%option
#% key: npoints
#% type: integer
#% required: yes
#% description: Number of points to be created for each class
#% answer: 100
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

    # sampling
    grass.message("Sampling for each class separately...")
    classes = grass.parse_command(
        'v.db.select', map=input,
        column=column, flags='c')

    class_outputs = []
    for cl in classes:
        random_output = 'v_random_strat_sampling_%s_%s' % (cl, str(os.getpid()))
        where_str = "%s = '%s'" % (column, cl)
        grass.run_command(
            'v.random', restrict=input, where=where_str,
            output=random_output, npoints=npoints)
        class_outputs.append(random_output)

    # combine vector data
    grass.message("Compining sampled vector data...")
    grass.run_command(
        'v.patch', flags='e', input=','.join(class_outputs), output=output)

    cleanup(class_outputs)
    grass.message("Sampling DONE <%s>" % output)


if __name__ == "__main__":
    options, flags = grass.parser()
    main()
