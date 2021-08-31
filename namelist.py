lib_path = 'libs/'
# =============== Domain settings =============== #
resy      = 0.125        # output latitude grid spacing
resx      = 0.125        # output longitude grid spacing

latlim    = [-90, 90]    # the latitude range of the domain
lonlim    = [0, 359.875] # the longitude range of the domain

# =========== calibration settings ============ #

prec_keys_TS = ['50',] # Lowest Thresholds for TS weighting

# forecast lead times of gridded objective analysis
fcst_keys = ['003', '006', '009', '012', '015', '018', '021', '024', 
             '027' ,'030', '033', '036', '039', '042', '045', '048', 
             '051', '054', '057', '060', '063', '066', '069', '072',
             '096', '120', '144', '168',]# '192', '216', '240']

# forecast lead times of scores (weights)
tssc_keys = ['024', '024', '024', '024', '024', '024', '024', '024', 
             '048' ,'048', '048', '048', '048', '048', '048', '048', 
             '072', '072', '072', '072', '072', '072', '072', '072',
             '096', '120', '144', '168',]# '192', '216', '240']

# ================== File path ================== #

TS_prefix_08Z = '%y%m%d08' # The prefix of TS
TS_prefix_20Z = '%y%m%d20'
TS_path   = 'U:/' # 'Test_TS/'

EC_path_08Z = 'S:/model/ECMWF_GLB/%Y%m%d08' #  # 'Test_model/ECMWF_GLB/%Y%m%d08'
NCEP_path_08Z = 'S:/model/NCEP_GLB/%Y%m%d08' #  # 'Test_model/NCEP_GLB/%Y%m%d08'
GRAPES_path_08Z = 'S:/model/GRAPES-GLB/%Y%m%d08' #  # 'Test_model/GRAPES-GLB/%Y%m%d08' 
filename_08Z = '%Y%m%d08.'

EC_path_20Z = 'S:/model/ECMWF_GLB/%Y%m%d20' # 'MPI_test_20/ECMWF_GLB/%Y%m%d20'
NCEP_path_20Z = 'S:/model/NCEP_GLB/%Y%m%d20' # 'MPI_test_20/NCEP_GLB/%Y%m%d20'
GRAPES_path_20Z = 'S:/model/GRAPES-GLB/%Y%m%d20' # 'MPI_test_20/GRAPES-GLB/%Y%m%d20'
filename_20Z = '%Y%m%d20.'

# Output filename
tag_name = 'MPI_Globe' # the name appears in the micaps file header
output_name_08Z = 'S:/mpi_globe/MPI_Globe_%Y%m%d08_' # 'MPI_Globe_%Y%m%d08_'
output_name_20Z = 'S:/mpi_globe/MPI_Globe_%Y%m%d20_' # 'MPI_Globe_%Y%m%d08_'
