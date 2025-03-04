from scipy.io import netcdf_file
import numpy as np

from config import BDD_SWI_DRIAS_PATH


def charger_donnees_debits_drias():
    nc = netcdf_file(BDD_SWI_DRIAS_PATH,'r')
    print(nc.variables)
    jours = nc.variables["time"]
    debits = nc.variables["debit"]
    print(debits[:])
    print(np.c_[jours[:], debits[:,0]]) #station 0
    nc.close()

