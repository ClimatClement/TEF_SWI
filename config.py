from pathlib import Path

CRS_PROJET = "EPSG:2154" #Lambert-93

ANNEES = list(range(2000, 2024))

#Chemin des données
BDD_PATH = Path('data-input')

BDD_SWI_DRIAS_PATH = Path(BDD_PATH, 'DRIAS EAU', "debit_France_SAFRAN-France_MF-SIM2_day_19760801-20220731.nc")

BDD_SIM2_PATH = Path(BDD_PATH, 'METEOFRANCE', "SIM2")
PERIODES_FICHIERS_SIM2 = ["2000-2009", "2010-2019", "2020-202501"]

BDD_SWI_PATH = Path(BDD_PATH, "METEOFRANCE", "SWI Uniforme")
BDD_SWI_METADATA_PATH = Path(BDD_SWI_PATH, "metadonnees_swi_276.csv")
BDD_SWI_DATA_PATH = Path(BDD_SWI_PATH, "SWI_Package_1969-2023")

BDD_CONTOURS_DEPARTEMENTS_PATH = sorted(Path.glob(BDD_PATH, "**/DEPARTEMENT.shp"))[0]

BDD_RESERVES_UTILES_PATH = Path(BDD_PATH, "GIS SOL", "bdgsf_classe_ru", "bdgsf_classe_ru.shp")

BDD_RENDEMENTS_PATH = Path(BDD_PATH, "FRANCEAGRIMER", "SCR-GRC-hist_dep_surface_prod_cult_cer-A25.zip")

OUTPUT_DATA_PATH = Path('data-output')
BDD_MAILLES_AVEC_DEPARTEMENTS_PATH = OUTPUT_DATA_PATH / 'mailles_avec_departements.csv'
BDD_DEPARTEMENTS_PATH = OUTPUT_DATA_PATH / 'departements.csv'
BDD_MAILLES_AVEC_RESERVES_UTILES_PATH = OUTPUT_DATA_PATH / 'mailles_avec_reserves_utiles_estimees.csv'
BDD_DATA_HUMIDITES_PAR_DEPARTEMENTS_ET_MOIS_PATH = OUTPUT_DATA_PATH / 'donnees_humidite_par_departements_et_mois.csv'
BDD_SIM2_PAR_DEPARTEMENTS_ET_JOURS_PATH = OUTPUT_DATA_PATH / 'donnees_sim2_journalieres_par_departements'