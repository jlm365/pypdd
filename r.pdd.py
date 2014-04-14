#!/usr/bin/env python

"""
MODULE:      r.in.pdd

AUTHOR(S):   Julien Seguinot

PURPOSE:     Positive Degree Day (PDD) model for glacier mass balance

COPYRIGHT:   (c) 2013-2014 Julien Seguinot

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

#%Module
#% description: Positive Degree Day (PDD) model for glacier mass balance
#% keywords: raster pdd
#%End

#%option
#% key: temp
#% type: string
#% gisprompt: old,cell,raster
#% description: Name of input temperature raster maps
#% required: yes
#% multiple: yes
#%end
#%option
#% key: prec
#% type: string
#% gisprompt: old,cell,raster
#% description: Name of input precipitation raster maps
#% required: yes
#% multiple: yes
#%end
#%option
#% key: stdv
#% type: string
#% gisprompt: old,cell,raster
#% description: Name of input precipitation raster maps
#% required: no
#% multiple: yes
#%end

#%option
#% key: pdd
#% type: string
#% gisprompt: new,cell,raster
#% description: Name for output number of positive degree days map
#% required: no
#%end
#%option
#% key: accu
#% type: string
#% gisprompt: new,cell,raster
#% description: Name for output ice-equivalent surface accumulation map
#% required: no
#%end
#%option
#% key: snow_melt
#% type: string
#% gisprompt: new,cell,raster
#% description: Name for output ice-equivalent surface melt of snow map
#% required: no
#%end
#%option
#% key: ice_melt
#% type: string
#% gisprompt: new,cell,raster
#% description: Name for output ice-equivalent surface melt of ice map
#% required: no
#%end
#%option
#% key: melt
#% type: string
#% gisprompt: new,cell,raster
#% description: Name for output ice-equivalent surface melt map
#% required: no
#%end
#%option
#% key: runoff
#% type: string
#% gisprompt: new,cell,raster
#% description: Name for output ice-equivalent surface meltwater runoff map
#% required: no
#%end
#%option
#% key: smb
#% type: string
#% gisprompt: new,cell,raster
#% description: Name for output ice-equivalent surface mass balance map
#% required: no
#%end

import grass.script as grass
from grass.script import array
import numpy as np         # scientific module Numpy [1]
from pypdd import PDDModel # positive degree day model PyPDD [2]


### Main function ###

def main():
    """main function, called at execution time"""

    # parse arguments
    temp_maps = options['temp'].split(',')
    prec_maps = options['prec'].split(',')
    stdv_maps = options['stdv'].split(',')

    # read temperature maps
    grass.info('reading temperature maps...')
    temp = [grass.array.array()] * 12
    for i, m in enumerate(temp_maps):
        temp[i].read(m)
        grass.percent(i, 12, 1)
    temp = np.asarray(temp)

    # read precipitation maps
    grass.info('reading precipitation maps...')
    prec = [grass.array.array()] * 12
    for i, m in enumerate(prec_maps):
        prec[i].read(m)
        grass.percent(i, 12, 1)
    prec = np.asarray(prec)

    # read standard deviation maps
    if stdv_maps != ['']:
        grass.info('reading standard deviation maps...')
        stdv = [grass.array.array()] * 12
        for i, m in enumerate(stdv_maps):
            stdv[i].read(m)
            grass.percent(i, 12, 1)
        stdv = np.asarray(stdv)
    else:
        stdv = 0.0

    # run PDD model
    grass.info('running PDD model...')
    pdd = PDDModel()
    smb = pdd(temp, prec, stdv)

    # write output maps
    grass.info('writing output maps...')
    for varname in ['pdd', 'accu', 'snow_melt', 'ice_melt', 'melt',
                    'runoff', 'smb']:
        if options[varname]:
            a = grass.array.array()
            a[:] = smb[varname]

### Main program ###

if __name__ == "__main__":
    options, flags = grass.parser()
    main()

# Links
# [1] http://numpy.scipy.org
# [2] http://github.com/jsegu/pypdd

