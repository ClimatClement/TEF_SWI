import pandas
from pathlib import Path

from pandas import DataFrame

from config import (BDD_SWI_DATA_PATH, BDD_MAILLES_AVEC_DEPARTEMENTS_PATH, BDD_MAILLES_AVEC_RESERVES_UTILES_PATH,
                    BDD_DATA_HUMIDITES_PAR_DEPARTEMENTS_ET_MOIS_PATH)


def calculer_donnees_humidite_par_departements_et_mois() -> None:
    df_mailles = _importer_donnees_mailles().rename(columns={'#num_maille': 'NUMERO'})
    df_swi = _importer_donnees_swi()
    df = pandas.merge(df_swi, df_mailles, on="NUMERO")
    df = (df.
          groupby(['NOM', 'INSEE_DEP', 'INSEE_REG', 'annee', 'mois', 'annee_mois'])[['SWI_UNIF_MENS3', 'reserve_mm']].
          mean().
          reset_index()
          )
    df.to_csv(BDD_DATA_HUMIDITES_PAR_DEPARTEMENTS_ET_MOIS_PATH, index=False, sep=";", float_format="%.2f")


def _importer_donnees_mailles() -> DataFrame:
    df_mailles_avec_departements = pandas.read_csv(BDD_MAILLES_AVEC_DEPARTEMENTS_PATH, sep=";")
    df_mailles_avec_reserves_utiles = pandas.read_csv(BDD_MAILLES_AVEC_RESERVES_UTILES_PATH, sep=";").loc[:, ["#num_maille", "reserve_mm"]]
    return pandas.merge(df_mailles_avec_departements, df_mailles_avec_reserves_utiles, on="#num_maille")


def _importer_donnees_swi() -> DataFrame:
    df_swi = pandas.DataFrame()
    for f in sorted(Path.glob(BDD_SWI_DATA_PATH, '*')):
        print(f'   lecture fichier : {f}')
        df_swi = pandas.concat([df_swi, pandas.read_csv(f, sep=";", decimal=',').drop(columns=["LAMBX","LAMBY"])])
    df_swi['date'] = pandas.to_datetime(df_swi['DATE'], format='%Y%m')
    df_swi['annee'] = df_swi['date'].dt.year
    df_swi['mois'] = df_swi['date'].dt.month
    df_swi['annee_mois'] = df_swi['annee'].astype(str) + '-' + df_swi['mois'].astype(str).str.zfill(2)
    return df_swi

