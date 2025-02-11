from pathlib import Path

#Chemin des données
BDD_PATH = Path('data-input')
BDD_SWI_PATH = Path(BDD_PATH, "METEOFRANCE/SWI")
BDD_SWI_METADATA_PATH = Path(BDD_SWI_PATH, "metadonnees_swi_276.csv")
BDD_SWI_DATA_PATH = Path(BDD_SWI_PATH, "SWI_Package_1969-2023")
BDD_CONTOURS_DEPARTEMENTS_PATH = sorted(Path.glob(BDD_PATH, "**/DEPARTEMENT.shp"))[0]

OUTPUT_DATA_PATH = Path('data-output')
BDD_SWI_AVEC_DEPARTEMENTS = OUTPUT_DATA_PATH / 'metadonnees_swi_276_wt_dep_reg.csv'