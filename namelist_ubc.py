lib_path = 'libs/'
# =============== Domain settings =============== #
resy      = 0.125        # output latitude grid spacing
resx      = 0.125        # output longitude grid spacing

latlim    = [-90, 90]    # the latitude range of the domain
lonlim    = [0, 359.875] # the longitude range of the domain

# =========== calibration settings ============ #

prec_keys_TS = ['50',] # Lowest Thresholds for TS weighting

# forecast lead times of gridded objective analysis
fcst_keys_03 = ['003', '006', '009', '012', '015', '018', '021', '024', 
                '027' ,'030', '033', '036', '039', '042', '045', '048', 
                '051', '054', '057', '060', '063', '066', '069', '072']

fcst_keys_06 = ['006', '012', '018', '024', '030', '036', '042', '048',
                '054', '060', '066', '072', '078', '084', '090', '096',
                '102', '108', '114', '120', '126', '132', '138', '144',
                '150', '156', '162', '168', '174', '180', '186', '192',
                '198', '204', '210', '216', '222', '228', '234', '240']

fcst_keys_24 = ['024', '048', '072', '096', '120', '144', '168', '192', '216', '240']

# forecast lead times of scores (weights)
tssc_keys_03 = ['024', '024', '024', '024', '024', '024', '024', '024', 
                '048' ,'048', '048', '048', '048', '048', '048', '048', 
                '072', '072', '072', '072', '072', '072', '072', '072']

tssc_keys_06 = ['024', '024', '024', '024', '048', '048', '048', '048',
                '072', '072', '072', '072', '096', '096', '096', '096',
                '120', '120', '120', '120', '144', '144', '144', '144',
                '168', '168', '168', '168', '192', '192', '192', '192',
                '216', '216', '216', '216', '240', '240', '240', '240']

tssc_keys_24 = ['024', '048', '072', '096', '120', '144', '168', '192', '216', '240']

# ================== File path ================== #

TS_prefix_08Z = '%y%m%d08' # The prefix of TS
TS_prefix_20Z = '%y%m%d20'
TS_path   = 'MPI_Test/TS/'

EC_path_08Z = 'MPI_Test/ECMWF_GLB/%Y%m%d08'
NCEP_path_08Z = 'MPI_Test/NCEP_GLB/%Y%m%d08'
GRAPES_path_08Z = 'MPI_Test/GRAPES-GLB/%Y%m%d08' 
filename_08Z = '%Y%m%d08.'

EC_path_20Z = 'MPI_Test/ECMWF_GLB/%Y%m%d20'
NCEP_path_20Z = 'MPI_Test/NCEP_GLB/%Y%m%d20'
GRAPES_path_20Z = 'MPI_Test/GRAPES-GLB/%Y%m%d20'
filename_20Z = '%Y%m%d20.'

# Output filename
output_name_08Z_03 = 'MPI_Globe_%Y%m%d_03_08_'
output_name_20Z_03 = 'MPI_Globe_%Y%m%d_03_20_'

output_name_08Z_06 = 'MPI_Globe_%Y%m%d_06_08_'
output_name_20Z_06 = 'MPI_Globe_%Y%m%d_06_20_'

output_name_08Z_24 = 'MPI_Globe_%Y%m%d_24_08_'
output_name_20Z_24 = 'MPI_Globe_%Y%m%d_24_20_'
