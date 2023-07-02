# Solving the Hackerland problem

This was done in a hurry over an evening, so code documentation is sparser than ideal.
But I wanted to solve it, and I did.

## Problem

A fully connected graph of cities, with roads connecting cities, is represented as as a network of edges with varying weights.
There are edges superfluous to that necessary for a fully connected graph.
The aim of the challenge is to create an algorithm that removes all superfluous roads such that the resultant fully-connected graph has minimal possibly sum of remaining road weights.

## Solution

I solved this by using multi-objective optimisation.
There were two objectives, both to be minimised:

1. Number of unconnected pairs of cities and
2. The sum of road weights retained.

The optimisation engine (unsga3) is something I coded up an implementation to many years ago.
At the time, this algorithm had just been released and no implementation existed (I suspect the authors had a company making money off it...).
I should have created more documentation.
This is bare bones, but it works.

## Running

In a bash terminal, wse `$> make docker-build` to build the Docker container.

Run the container from a bash terminal using `$> make docker-run`.
It should create an interactive bash terminal within the container.

Attach Visual Studio Code to the running container.
This project was developed using Visual Studio Code.
You probably need to install a few python-related extensions to make it work.
I recommend running in interactive mode (there are graphs).
The main entry point to the program is `hackerland/driver.py`.

Within the container, all work resides within the directory `/home`.
unsga3 is installed to the container directory `/unsga3`.
