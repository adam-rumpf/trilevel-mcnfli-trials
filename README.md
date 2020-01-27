# Computational Trial Generation for Trilevel Network Interdiction Game with Linear Interdependencies

A collection of programs used to generate test cases for the main solver of a research project of mine involving a trilevel network interdiction game on an interdependent network. See the main solver [here](https://github.com/adam-rumpf/trilevel-mcnfli). I would not expect these programs to be of use to anyone outside of my research group, but they are provided here for anyone interested.

The goal of these programs is to generate two types of computational trial: a [small example problem](#small-scale-test-network) that can be solved exactly for the purposes of testing the solution algorithm, and a collection of randomly generated test networks (along with scripts for editing and preparing the networks) for use in generating empirical computational results.

## Small-Scale Test Network

`example_network.nb` is a Mathematica notebook for generating a single test instance of the trilevel network interdiction game with linear interdependencies. The underlying network is based on the example network used in

> H. Kaul and A. Rumpf. Linear input dependence model for interdependent civil infrastructure systems with network simplex based solution algorithm. In preparation, 2020.

Small subsets of arcs are chosen to be available for protection and destruction. The network interdiction game is then solved by exhaustively searching the three-stage game tree and applying a minimax algorithm. The output file format is based on the NETGEN format used in the main [MCNFLI trial program](https://github.com/adam-rumpf/mcnfli-trials), modified to include defense bounds, destruction bounds, and the defensible and destructible arc sets.
