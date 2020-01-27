# Computational Trial Generation for Trilevel Network Interdiction Game with Linear Interdependencies

A collection of programs used to generate test cases for the main solver of a research project of mine involving a trilevel network interdiction game on an interdependent network. See the main solver [here](https://github.com/adam-rumpf/trilevel-mcnfli). I would not expect these programs to be of use to anyone outside of my research group, but they are provided here for anyone interested.

The goal of these programs is to generate two types of computational trial: a [small example problem](#small-scale-test-network) that can be solved exactly for the purposes of testing the solution algorithm, and a collection of [randomly generated test networks](#netgen-files) (along with scripts for editing and preparing the networks) for use in generating empirical computational results.

## Small-Scale Test Network

`example_network.nb` is a Mathematica notebook for generating a single test instance of the trilevel network interdiction game with linear interdependencies. The underlying network is based on the example network used in

> H. Kaul and A. Rumpf. Linear input dependence model for interdependent civil infrastructure systems with network simplex based solution algorithm. In preparation, 2020.

Small subsets of arcs are chosen to be available for protection and destruction. The network interdiction game is then solved by exhaustively searching the three-stage game tree and applying a minimax algorithm. The output file format is based on the NETGEN format used in the main [MCNFLI trial program](https://github.com/adam-rumpf/mcnfli-trials), modified to include defense bounds, destruction bounds, and the defensible and destructible arc sets.

## NETGEN Files

`netgen_edit.py` is a collection of Python functions for generating and editing random test instances. The implementation of NETGEN is taken from the main [MCNFLI trial program](https://github.com/adam-rumpf/mcnfli-trials). Specifically, the structure of a problem `.min` file is as follows:

* Comment lines begin with `c` and are ignored by the solver.
* The objective line begins with a `p` and contains the following information in order:
  * `min` or `max` to indicate the problem sense
  * number of nodes
  * number of arcs
  * `a` or `n` to indicate whether arcs or nodes are treated as parents
  * number of arcs that can be defended in stage 1
  * number of arcs that can be destroyed in stage 2
* Node definitions begin with an `n` and contain the following information in order:
  * node ID
  * supply value, assumed to be `0` for unlisted nodes
* Arc definitions begin with an `a` and contain the following information in order:
  * node ID of tail
  * node ID of head
  * lower flow bound
  * upper flow bound
  * unit flow cost
* Interdependencies begin with an `i` and contain the following information in order:
  * parent ID (node ID if parent type `n` or arc ID if parent type `a`)
  * child ID (always an arc ID)
* Defensible and destructible arc definitions begin with a `d` or `r`, respectively, and consist only of arc IDs. If no defensible or destructible arcs are listed, then all arcs are assumed to be available.

Node IDs and arc IDs are both assumed to begin with `1`. In the case of arcs, the IDs used are assumed to correspond to their position within the complete arc list.
