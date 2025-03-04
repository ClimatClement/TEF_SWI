import pandas
from pandas.core.interchange.dataframe_protocol import DataFrame

from config import BDD_SIM2_PATH, PERIODES_FICHIERS_SIM2, BDD_MAILLES_AVEC_DEPARTEMENTS_PATH, BDD_SIM2_PAR_DEPARTEMENTS_ET_JOURS_PATH
from fonctions_communes.reinitialiser_dossier import reinitialiser_dossier


def charger_donnees_sim2_par_departements_et_jours():
    df = pandas.DataFrame()
    for f in BDD_SIM2_PAR_DEPARTEMENTS_ET_JOURS_PATH.glob('*'):
        df = pandas.concat([df, pandas.read_csv(f, sep=";", dtype={"INSEE_DEP": "str"})])
    df['DATE'] = pandas.to_datetime(df['DATE'], format='%Y%m%d')
    return df.reset_index(drop=True)


def calculer_donnees_sim2_par_departements() -> None:
    reinitialiser_dossier(BDD_SIM2_PAR_DEPARTEMENTS_ET_JOURS_PATH)
    for p in PERIODES_FICHIERS_SIM2:
        df_swi = _charger_donnees_sim2(p)
        df_mailles = pandas.read_csv(BDD_MAILLES_AVEC_DEPARTEMENTS_PATH, sep=";")
        df = pandas.merge(df_swi, df_mailles.loc[:, ["#num_maille", "INSEE_DEP", "lambx","lamby"]],
                      left_on=["LAMBX","LAMBY"],
                      right_on=["lambx","lamby"])
        df = df.groupby(["INSEE_DEP", "DATE"])[["SWI_Q"]].mean()
        df.to_csv(BDD_SIM2_PAR_DEPARTEMENTS_ET_JOURS_PATH / f"{p}.csv", sep=";")


def _charger_donnees_sim2(periode: str) -> DataFrame:
    fichier = f"QUOT_SIM2_{periode}.csv.gz"
    print(f"...chargement fichier {fichier}")
    df = pandas.read_csv(BDD_SIM2_PATH / fichier, compression="gzip", sep=";")
    return df.loc[:, ['LAMBX','LAMBY','DATE','SWI_Q']]
