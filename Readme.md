# Introduction
This is a tool to identify polygons from noisy point clouds, using a genetic algorithm-based optimizer. It can take as its input data a CSV file of data points (one point per line) or a PNG image of the sonar data, where pixels with non-zero red values are considered to be data points. 

# Requirements:
* Python (2.7 tested)
* Numpy
* Matplotlib
* PyTables

# Usage:
	python identify.py Test_data/data.csv
OR
	python identify.py Test_images/sample_pent.png


