import glob
from measure_extinction.modeldata import ModelData

file_path = "/Users/pyanchulova/Documents/extstar_data/"

def main(band_names, data_names):
    """

    """
    tlusty_models_fullpath = glob.glob("{}/Models/tlusty_*v10.dat".format(file_path))
    # tlusty_models_fullpath = tlusty_models_fullpath[0:10]
    tlusty_models = [
        tfile[tfile.rfind("/") + 1 : len(tfile)] for tfile in tlusty_models_fullpath
    ]

    # get the models with just the reddened star band data and spectra
    modinfo = ModelData(
        tlusty_models,
        path="{}/Models/".format(file_path),
        band_names=band_names,
        spectra_names=data_names,
    )

    print("log(Teff) range:", modinfo.temps_min, modinfo.temps_max)
    print("log(g) range:", modinfo.gravs_min, modinfo.gravs_max)
    print("log(Z) range:", modinfo.mets_min, modinfo.mets_max)

    return modinfo