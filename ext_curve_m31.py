import glob
import importlib
import sys, os

import numpy as np
import scipy.optimize as op

import matplotlib.pyplot as plt
import matplotlib as mpl

import astropy.units as u

import emcee

from dust_extinction.averages import G03_SMCBar
from dust_extinction.parameter_averages import F19

import measure_extinction
from measure_extinction.stardata import StarData
from measure_extinction.extdata import ExtData
from measure_extinction.modeldata import ModelData
from measure_extinction.utils.fit_model import FitInfo

from measure_extinction.utils.helpers import get_full_starfile
from measure_extinction.utils.fit_model import get_best_fit_params, get_percentile_params

m31_list = [
# "m31_e1_j004354.05+412626.0",
# "m31_e2_j004413.84+414903.9",
# "m31_e3_j004420.52+411751.1",
# "m31_e4_j004427.47+415150.0",
# "m31_e5_j004431.66+413612.4",
"m31_e6_j004438.71+415553.5",
# "m31_e7_j004454.37+412823.9",
# "m31_e8_j004511.82+415025.3",
# "m31_e9_j004511.85+413712.9", # some problem with walkers
## "m31_e10_j004512.73+413726.4", # No STIS data
## "m31_e11_j004535.40+414431.5", # No STIS data
# "m31_e12_j004539.00+415439.0",
# "m31_e13_j004539.70+415054.8",
# "m31_e14_j004543.46+414513.6",
# "m31_e15_j004546.81+415431.7",
]

file_path = "/Users/pyanchulova/Documents/extstar_data/"
savefile_path = "/Users/pyanchulova/Documents/ext-science/figs/"
folder = ""

if not os.path.isdir(savefile_path + folder):
    print("making new dir", (savefile_path + folder))
    os.system("mkdir " + savefile_path + folder)

# Karl-level STIS data location
karl_data_path = "~/../../user/kgordon/Python_git/extstar_data/STIS_Data/"


def main(modinfo, starname=m31_list[0]):
    """
    """

    fstarname = f"{starname}.dat"
    velocity = -109.3  # M31 radial velocity from NED
    relband = "ACS_F475W"
    relband_str = "$F475W$"
    starstr = starname.split("m31_")[1].split("_")[0]
    print(starname, starstr)

    # Get reddened star data
    reddened_star, band_names, data_names = get_red_star(fstarname, file_path)


def get_red_star(starname=m31_list[0]):
    """
    """

    fstarname = f"{starname}.dat"

    # get the observed reddened star data
    reddened_star = StarData(fstarname, path=f"{file_path}/DAT_files/")
    band_names = reddened_star.data["BAND"].get_band_names()
    data_names = reddened_star.data.keys()
    print("band names", band_names)
    print("data names", data_names)
    print("starname", fstarname)

    return reddened_star, band_names, data_names


def set_weights(data_names, reddened_star):
    """
    """
    # cropping info for weights
    #  bad regions are defined as those where we know the models do not work
    #  or the data is bad
    # pnames = ["logT","logg","logZ","Av","Rv","C2","C3","C4","x0","gamma","HI_gal","HI_mw"]
    ex_regions = [
        [8.23 - 0.1, 8.23 + 0.1],  # geocoronal line
        [8.7, 10.0],  # bad data from STIS
        [3.55, 3.6],
        [3.80, 3.90],
        [4.15, 4.3],
        [6.4, 6.6],
        [7.1, 7.3],
        [7.45, 7.55],
        [7.65, 7.75],
        [7.9, 7.95],
        [8.05, 8.1],
    ] / u.micron

    weights = {}
    for cspec in data_names:
        weights[cspec] = np.full(len(reddened_star.data[cspec].fluxes), 0.0)
        gvals = reddened_star.data[cspec].npts > 0
        # Originally:
        # weights[cspec][gvals] = 1.0 / reddened_star.data[cspec].uncs[gvals].value
        # New:
        weights[cspec][gvals] = 1.0 / reddened_star.data[cspec].uncs[gvals].value

        x = 1.0 / reddened_star.data[cspec].waves
        for cexreg in ex_regions:
            weights[cspec][np.logical_and(x >= cexreg[0], x <= cexreg[1])] = 0.0

    # make the photometric bands have higher weight
    weights["BAND"] *= 10000.0
    print("weight arrays set")
    return weights