"""Scripts for editing trilevel network interdiction game NETGEN files.

This file includes a variety of small programs for generating and editing
NETGEN files for use as computational trials. For the most part these files are
meant to follow the standard NETGEN format as described in:

    D. Klingman, A. Napier, and J. Stutz. NETGEN: A program for generating
    large scale capacitated assignment, transportation, and minimum cost flow
    network problems. Management Science, 20(5):814-821, 1974.

The output files include additional information for defining interdependencies
and defensible/destructible arc sets.

The following scripts are included:
    call_netgen -- Calls a standalone NETGEN .exe to generate an interdependent
        network instance.
    generate_trials -- Generates a set of trials
"""

import math
import os
import random

#==============================================================================
def call_netgen(file, nodes, arcs, itype, inum, seed=None, sources=None,
                sinks=None, costs=(0, 100), supply=None,
                capacities=(100, 500)):
    """Calls a local standalone NETGEN .exe file to generate a trial.

    This requires the presence of a file called "netgen.exe" in the local
    directory. This file is based on the NETGEN implementation from the MCNFLI
    project, and generates interdependent network instances with no information
    regarding the trilevel network interdiction game extension, which will be
    added to the file by the other scripts in this file.

    Requires the following positional arguments:
        file -- Name of the output file.
        nodes -- Number of nodes.
        arcs -- Number of arcs.
        itype -- Interdependency type (0 for parent nodes, 1 for parent arcs).
        inum -- Number of interdependencies.

    Accepts the following optional keyword arguments:
        seed -- Integer RNG seed for NETGEN. Defaults to a random seed.
        sources -- Number of source nodes. Defaults to 20% of all nodes
            (rounded up).
        sinks -- Number of sink nodes. Defaults to 20% of all nodes (rounded
            up).
        costs -- Tuple of arc cost lower bound and upper bound. Defaults to
            (0, 100).
        supply -- Total supply value across all source nodes. Defaults to
            10,000 per 256 nodes (rounded up).
        capacities -- Tuple of arc capacity lower bound and upper bound.
            Defaults to (100, 500).
    """

    # Set unspecified RNG seed to one based on the system time
    if seed == None:
        seed = int(10e8 * random.random())

    # Set unspecified sources and sinks
    if sources == None:
        sources = math.ceil(0.2 * nodes)
    if sinks == None:
        sinks = math.ceil(0.2 * nodes)

    # Set unspecified total supply
    if supply == None:
        supply = 10000 * math.ceil(nodes / 256)

    # Call the NETGEN program and return the exit code
    return os.system("netgen.exe "+file+" "+str(seed)+" "+str(nodes)+" "+
                     str(sources)+" "+str(sinks)+" "+str(arcs)+" "+
                     str(costs[0])+" "+str(costs[1])+" "+str(supply)+
                     " 0 0 100 100 "+str(capacities[0])+" "+str(capacities[1])+
                     " "+str(itype)+" "+str(inum))

#==============================================================================
def generate_trials():
    pass

#==============================================================================
def convert_folder():
    pass
