# -*- coding: utf-8 -*-
# import keywords from the namelist
from namelist import lib_path, prec_keys_TS, TS_path, tag_name, lonlim, latlim, fcst_keys, tssc_keys, \
                     filename_08Z, TS_prefix_08Z, NCEP_path_08Z, EC_path_08Z, GRAPES_path_08Z, output_name_08Z, \
                     filename_20Z, TS_prefix_20Z, NCEP_path_20Z, EC_path_20Z, GRAPES_path_20Z, output_name_20Z

from sys import path, argv
path.insert(0, lib_path)

# local scripts
import micpas_tool as mt
import ensemble_tool as et
from utility import ini_dicts, subtrack_precip_lev, subtrack_precip_lev_heavy

# other modules
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

# -------------------- #
# variable names: 
#    "cmpt" ---> Components of multi-model, multi-center forecasts
#    "tssc" ---> TS scores
#    "prec_keys" ---> Precipitation rate threshlds

def dummy_module(delta_day, day0):
    '''
    dummy module for opertional test
    '''
    date_ref = datetime.utcnow()+relativedelta(days=delta_day)
    print('The main routine runs at '+date_ref.strftime('%Y%m%d'))
    return date_ref.day

def main(delta_day, day0, key):
    '''
    The main routine of ensemble precipitation post-porcessing. 
    '''
    if key == 20:
        TS_prefix = TS_prefix_20Z
        NCEP_path = NCEP_path_20Z
        EC_path = EC_path_20Z
        GRAPES_path = GRAPES_path_20Z
        filename = filename_20Z
        output_name = output_name_20Z
    else:
        TS_prefix = TS_prefix_08Z
        NCEP_path = NCEP_path_08Z
        EC_path = EC_path_08Z
        GRAPES_path = GRAPES_path_08Z
        filename = filename_08Z
        output_name = output_name_08Z

    # UTC time corrections & filename creation
    date_ref = datetime.utcnow()+relativedelta(days=delta_day)
    date_ref_delay = date_ref-relativedelta(days=1) # use yesterday's forecast
    date_BJ = date_ref_delay+relativedelta(hours=8)

    print('Ensemble post-processing starts at ['+date_ref.strftime('%Y%m%d-%H:%M%p')+'] UTC')
    name_today = []

    name_today.append(datetime.strftime(date_BJ, EC_path))
    name_today.append(datetime.strftime(date_BJ, NCEP_path))
    name_today.append(datetime.strftime(date_BJ, GRAPES_path))

    print('Import all micaps files')

    lon, lat = mt.genrate_grid(lonlim=lonlim, latlim=latlim)

    # =========== import gridded data =========== #

    ## Initializing dictionaries

    cmpt_keys = ['EC', 'NCEP', 'GRAPES']

    dict_var = {}; dict_interp = {}; dict_header = {}
    dict_var = ini_dicts(dict_var, cmpt_keys)
    dict_interp = ini_dicts(dict_interp, cmpt_keys)

    ## Fill dictionaries with data    
    for fcst_key in fcst_keys:

        lead = np.float(fcst_key)

        if lead%24 == 0:
            subpath = '/pre24/'
        else:
            subpath = '/pre03/'

        for i, name in enumerate(name_today):

            # identify the file path
            temp_name = name+subpath+datetime.strftime(date_BJ, filename)+fcst_key

            # read from micaps (will return false if it failed)
            temp = mt.micaps_import(temp_name)

            if temp == False:
                print(temp_name+' not found. Exit ...')
                return day0
            else:
                dict_var[cmpt_keys[i]][fcst_key] = temp[2]

        # modify the input file head and use it as the output file head
        temp[3][0] = temp[3][0].replace("FZMOS", tag_name)
        dict_header[fcst_key] = temp[3]

    # Get latlon info
    dict_latlon = {}
    for i, name in enumerate(name_today):
        dict_latlon[cmpt_keys[i]] = {}

    for i, name in enumerate(name_today):
        for fcst_key in fcst_keys:

            lead = np.float(fcst_key)

            if lead%24 == 0:
                subpath = '/pre24/'
            else:
                subpath = '/pre03/'

            temp_name = name+subpath+datetime.strftime(date_BJ, filename)+fcst_key
            dict_latlon[cmpt_keys[i]][fcst_key] = mt.micaps_import(temp_name, export_data=False)

    # diff_latlon = 0
    # diff_latlon += np.sum(np.abs(dict_latlon['EC']['024'][0] - lon)) + np.sum(np.abs(dict_latlon['EC']['024'][1] - lat))
    # diff_latlon += np.sum(np.abs(dict_latlon['NCEP']['024'][0] - lon)) + np.sum(np.abs(dict_latlon['NCEP']['024'][1] - lat))
    # diff_latlon += np.sum(np.abs(dict_latlon['GRAPES']['024'][0] - lon)) + np.sum(np.abs(dict_latlon['GRAPES']['024'][1] - lat))

    # interpolate to the output latlon if they mismatched

    print('Warning: input and output coordinates mismatched. Fixing with bilinear interpolation.')

    lon, lat = mt.genrate_grid(lonlim=lonlim, latlim=latlim)

    for key, val in dict_var.items():
        for fcst_key in fcst_keys:
            dict_interp[key][fcst_key] = interp2d_wraper(dict_latlon[key][fcst_key][0], dict_latlon[key][fcst_key][1], val[fcst_key], lon, lat)

    # ========== Ensemble Caliberation ========== #

    print('Estimating calibration weights')

    # ---------- Extracting weights ---------- #
    # initialization
    # W[precip threshold][fcst lead time][model component]

    print('\tExtracting TS for {} mm events'.format(prec_keys_TS))

    W = {}; W = ini_dicts(W, prec_keys_TS)

    for prec_key in prec_keys_TS:
        W[prec_key] = ini_dicts(W[prec_key], tssc_keys)

    for prec_key in prec_keys_TS:
        for tssc_key in tssc_keys:

            # retreive ts files by the fcst delay
            date_temp = date_ref - relativedelta(days=int(tssc_key)/24) # from fcst horizon (i.e., hours) to days

            # reading TS from selected files + TS moving average
            ## The moving averaging considers 10 days backward 
            data_ma, flag_TS = et.read_ts(date_temp.strftime(TS_prefix), TS_path+prec_key+'/', lead=tssc_key)

            # saving weights to the dictionary
            # case: no TS files (flag_TS=False)
            if np.logical_not(flag_TS):
                print("TS files do not exist. Exit.")
                return day0 # <--- exit if no TS files

            # case: TS filled with NaNs (vals = 9999.0)
            ## Use TS=0.5
            elif np.isnan(data_ma.values[-1, 1:].astype(np.float)).sum() >= 3:
                print('Warning: TS filled with NaNs, use average.')
                for cmpt_key in cmpt_keys:
                    W[prec_key][tssc_key][cmpt_key] = 0.5
                flag_heavy = False

            # case: regular (good quality) weights
            else:
                for cmpt_key in cmpt_keys:
                    temp = data_ma[cmpt_key][9:10].values
                    if np.isnan(temp):
                        temp = 0.0
                    W[prec_key][tssc_key][cmpt_key] = temp

    # Calculate ensembles
    print('Preparing output')
    output = {}

    # get all the result at the current day
    print('Total: '+str(len(fcst_keys)))

    thres = prec_keys_TS[0]

    for i in range(len(fcst_keys)):

        print('Calculating '+fcst_keys[i])
        # --------------------------------------------------- #
        # 0, 25, 50 mm cases
        # initialization (three sets of weights: [0, 25, 50])
        W0 = 0.0; W25 = 0.0; W50 = 0.0

        W_EC = W[thres][tssc_keys[i]]['EC']
        W_NCEP = W[thres][tssc_keys[i]]['NCEP']
        W_GRAPES = W[thres][tssc_keys[i]]['GRAPES']

        data0_EC, data25_EC, data50_EC = subtrack_precip_lev(dict_interp['EC'][fcst_keys[i]])
        data0_NCEP, data25_NCEP, data50_NCEP = subtrack_precip_lev(dict_interp['NCEP'][fcst_keys[i]])
        data0_GRAPES, data25_GRAPES, data50_GRAPES = subtrack_precip_lev(dict_interp['GRAPES'][fcst_keys[i]])

        precip0 = 0.5*data0_EC + 0.5*data0_NCEP
        precip25 = (1/3)*data25_EC + (1/3)*data25_NCEP + (1/3)*data50_GRAPES
        precip50 = (W_EC*data50_EC + W_NCEP*data50_NCEP + W_GRAPES*data50_GRAPES)/(W_EC+W_NCEP+W_GRAPES)

        output[fcst_keys[i]] = precip0 + precip25 + precip50

        # =========================================== #

    # Preparing MICAPS file output
    for fcst_key in fcst_keys:
        metadata = mt.micaps_change_header(lon.shape, dict_header[fcst_key], lonlim, latlim)
        mt.micaps_export(datetime.strftime(date_BJ, output_name)+fcst_key+'.txt', metadata, output[fcst_key])

    print('Ensemble post-processing complete')
    
    return date_ref.day

day_out = main(int(argv[1]), int(argv[2]), int(argv[3]))
with open('shaG_history.log', 'w') as fp:
    fp.write(str(day_out).zfill(2)) # exporting the day of completion (and where to restart if fails)

