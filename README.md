# MPI-Globe

A multi-model (ECMWF, GEFS, GRAPES) precipitation ensemble post-processing system operated at the Beijing Meteorological Service; it provides global-scale precipitation guidence out to 10 days with 0.125 degree grid spacing.

The post-processing routine is operated two times per day on 00 and 12 UTC (08 and 20 Beijing Time). In each operation, the system processes 3 hourly (03, 06, ..., 072), 6 hourly (06, 12, ..., 240), and daily (24, 48, ..., 240) precipitation ensembles, producing ascii files that can be accessed through the Chinese Meteorological Administration (CMS), Meteorological Information Comprehensive Analysis Process System (MICAPS).

* `namelist.py`: the operational configuration file.
* `ensemble_08Z_exe.bash` the 08Z operational routine.
* `ensemble_20Z_exe.bash` the 20Z operational routine. 

# Contributors

* Yingkai Sha <yingkai@eoas.ubc.ca>
* Uji Murakumo

