# py-ext4info

py-ext4info is a tool written in pure python to extract information from an ext4 formatted filesystem superblock and print them.

This is written purely for my own enjoyment and as practice and as a challenge to see if I am able to parse and interact with raw filesystem structure in python.

This project is also written as an exercise to better understand the pipenv workflow, as I've only used virtualenv in the past.

DO NOT USE THIS ON A PRODUCTION FILESYSTEM CONTAINING DATA YOU ARE WILLING TO LOSE

## Goals

The following are the goals that this project seeks to achieve:

* Manage a python project using pipenv
* Become familiar with the EXT4 superblock structure
* Use python's struct module to unpack the contents of an EXT4 superblock
* Print relevant information about a real filesystem in python

# TODO
* create ext4 filesystem image to work from (I don't plan to use a live ext4 filesystem until I've tested it on an image I don't care about)
* create skeleton of utility
* cleanup readme

# Sources for info
https://www.kernel.org/doc/html/latest/filesystems/ext4/index.html
