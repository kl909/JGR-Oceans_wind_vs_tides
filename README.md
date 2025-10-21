# JGR-Oceans_wind_vs_tides
Scripts and matrices for JGR:Oceans publication of manuscript Unravelling Short-Term Coral Connectivity: The Dominant Influence of Tides on Larval Retention in the Great Barrier Reef

Scripts order:
1. ocean_parcels_scaled.py - runs Parcels script for releasing particles per km^2 of each reef
2. con_matrix_logged.py - creates connectivity matrix from Parcels outputs
3. trajectory_2_shp_chunked.py - creates shapefiles of particle trajectories
4. calculate_sinuosity.py - calculates sinuosity of each trajectory
5. calculate_vorticity.py - calculate vorticity of entire model model
6. calculate_vorticity_masked.py - calculate vorticity of a sector
7. diagonal_analysis.py - diagonal analysis of connectivity matrices
8. diagonal_analysis.R - statistical analysis of connectivity matrix and other variables

Examples of connectivity matrices for Cairns:
1. connectivty_matrix_cairns_tides.csv
2. connectivty_matrix_cairns_wind.csv
3. connectivty_matrix_cairns_windtides.csv

Thetis scripts are not included in this repository, please see Thetis Project for more information. Please also see OceanParcels for more information on using Parcels scripts.
