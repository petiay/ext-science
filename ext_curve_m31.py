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

