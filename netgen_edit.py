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
    call_netgen() -- Calls a standalone NETGEN .exe to generate an
        interdependent network instance.
    generate_trials() -- Generates a set of trials with identical parameters
        but different random seeds.
    convert_file() -- Converts an MCNFLI NETGEN file into the format required
        for the trilevel extension.
    convert_folder() -- Converts all MCNFLI NETGEN files in a folder into the
        format required for the trilevel extension.
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
        file -- Name of the output file (excluding the file extension).
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
    return os.system("netgen.exe "+file+".min "+str(seed)+" "+str(nodes)+" "+
                     str(sources)+" "+str(sinks)+" "+str(arcs)+" "+
                     str(costs[0])+" "+str(costs[1])+" "+str(supply)+
                     " 0 0 100 100 "+str(capacities[0])+" "+str(capacities[1])+
                     " "+str(itype)+" "+str(inum))

#==============================================================================
def generate_trials(file, num, nodes, arcs, itype, inum, sources=None,
                sinks=None, costs=(0, 100), supply=None,
                capacities=(100, 500)):
    """Generates a set of trials using the same parameters.

    This function acts as a driver for call_netgen() to generate a set of
    trials using the same set of parameters but different random seeds.

    Requires the following positional arguments:
        file -- Base name of the output file (excluding the file extension).
            All generated trials will be given the specified name followed by a
            unique number.
        num -- Number of files to generate.
        nodes -- Number of nodes.
        arcs -- Number of arcs.
        itype -- Interdependency type (0 for parent nodes, 1 for parent arcs).
        inum -- Number of interdependencies.

    Accepts the following optional keyword arguments:
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

    # Set unspecified sources and sinks
    if sources == None:
        sources = math.ceil(0.2 * nodes)
    if sinks == None:
        sinks = math.ceil(0.2 * nodes)

    # Set unspecified total supply
    if supply == None:
        supply = 10000 * math.ceil(nodes / 256)

    # Main loop
    i = 1
    while i <= num:
        # Generate file name by concatenating a number
        fname = file + str(i).zfill(math.ceil(math.log10(num+1)))

        # Use call_netgen() to generate a trial with an unspecified seed
        code = call_netgen(fname, nodes, arcs, itype, inum, sources=sources,
                sinks=sinks, costs=costs, supply=supply, capacities=capacities)

        # If return code indicates unsuccessful execution, repeat loop
        if code != 0:
            continue

        print("File "+str(i)+" / "+str(num)+" generated.")

        i += 1

#==============================================================================
def convert_file(file, defnum, attnum, defset=[], attset=[], temp="save.tmp"):
    """Converts an MCNFLI problem file into a trilevel game problem file.

    The file format for the trilevel network interdiction game is almost
    completely identical to that of the standard interdependent network file,
    except that we add comment lines to explain the new attributes, we add
    defense and attack bounds to the objective line, and we add sets of
    defensible and destructible arcs to the end of the file.

    Requires the following positional arguments:
        file -- Full name of the file to be converted (including the file
            extension).
        defnum -- Number of arcs that can be defended during Stage 1.
        attnum -- Number of arcs that can be attacked during Stage 2.

    Accepts the following optional keyword arguments:
        defset -- List of defensible arc IDs (beginning at index 1). Defaults
            to the empty list, which is treated as allowing all arcs to be
            defended.
        attset -- List of destructible arc IDs (beginning at index 1). Defaults
            to the empty list, which is treated as allowing all arcs to be
            destroyed. All defensible arcs are assumed to be attackable, so
            only arcs that can be attacked but not defended need be listed.
        temp -- Name of a temporary file used during the file conversion
            process. Defaults to "save.tmp". As a temporary file this only
            really needs to be changed if that name is already in use within
            the same directory.
    """

    # Read input file while writing edited copy to a temporary file
    with open(file, 'r') as fin:
        with open(temp, 'w') as fout:
            i = 0 # current line number
            for line in fin:
                i += 1

                # Write edited contents for specific lines
                if i == 2:
                    # Replace interdependent network comment
                    print("c Modified to generate trilevel interdiction",
                          file=fout)
                    print("c games on interdependent networks", file=fout)
                elif i == 23:
                    # Add trilevel game information at end of comments
                    print("c   Interdiction Game Moves -", file=fout)
                    print("c     Defense Limit:      "+str(defnum), file=fout)
                    print("c     Attack Limit:       "+str(attnum), file=fout)
                    if len(defset) > 0:
                        print("c     Defensible Arc Set: "+str(len(defset)),
                              file=fout)
                    else:
                        print("c     Defensible Arc Set: All", file=fout)
                    if len(attset) > 0:
                        print("c     Attackable Arc Set: "+str(len(attset)),
                              file=fout)
                    else:
                        print("c     Attackable Arc Set: All", file=fout)
                    print(line[:-1], file=fout)
                elif line[0] == 'p':
                    # Add defense/attack limits to end of objective line
                    print(line[:-1]+" "+str(defnum)+" "+str(attnum), file=fout)
                else:
                    # Otherwise copy the line exactly
                    print(line[:-1], file=fout)

            # Add additional lines for the defensible and destructible arc sets
            if len(defset) > 0:
                for a in defset:
                    print("d "+str(a), file=fout)
                if len(attset) > 0:
                    for a in attset:
                        print("r "+str(a), file=fout)

    print("File contents written to temporary file.")

    # Overwrite original file with temporary file
    with open(temp, 'r') as fin:
        with open(file, 'w') as fout:
            for line in fin:
                print(line[:-1], file=fout)

    print("Input file overwritten.")

    # Delete temporary file
    os.remove(temp)
    print("Temporary file deleted.")

#==============================================================================
def convert_folder(folder, defnum, attnum, defset=[], attset=[],
                   temp="save.tmp"):
    """Converts a folder of MCNFLI problem files into trilevel game files.

    Applies convert_file() to all .min files in a specified directory. Only the
    top level of the specified folder will be affected, not any of its
    subfolders.

    Requires the following positional arguments:
        folder -- Name of the folder whose contents should be converted.
        defnum -- Number of arcs that can be defended during Stage 1.
        attnum -- Number of arcs that can be attacked during Stage 2.

    Accepts the following optional keyword arguments:
        defset -- List of defensible arc IDs (beginning at index 1). Defaults
            to the empty list, which is treated as allowing all arcs to be
            defended.
        attset -- List of destructible arc IDs (beginning at index 1). Defaults
            to the empty list, which is treated as allowing all arcs to be
            destroyed. All defensible arcs are assumed to be attackable, so
            only arcs that can be attacked but not defended need be listed.
        temp -- Name of a temporary file used during the file conversion
            process. Defaults to "save.tmp". As a temporary file this only
            really needs to be changed if that name is already in use within
            the specified directory.
    """

    # Get list of file names in the specified folder
    for (_, _, files) in os.walk(folder):
        break

    num = len(files) # number of files to process

    # Process each file
    i = 1
    for f in files:
        convert_file(folder+"/"+f, defnum, attnum, defset=defset,
                     attset=attset, temp=temp)
        print("File "+str(i)+" / "+str(num)+" processed.")
        i += 1
