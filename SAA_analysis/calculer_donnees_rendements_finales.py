import pandas
from pandas import DataFrame

from config import BDD_RENDEMENTS_PATH, ANNEES
from fonctions_communes.calculer_ecarts_a_la_moyenne import calculer_ecarts_a_la_moyenne


def calculer_donnees_rendements() -> DataFrame:
    df = importer_donnees_rendements()
    df = calculer_ecarts_a_la_moyenne(df, on=['INSEE_DEP', 'ESPECES'], colonne='CULT_REND', colonne_ponderation='CULT_SURF')
    df = calculer_ecarts_a_la_moyenne(df, on=['INSEE_DEP', 'ESPECES'], colonne='CULT_SURF')

    return df


def importer_donnees_rendements() -> DataFrame:
    df_rendements = pandas.read_csv(BDD_RENDEMENTS_PATH, sep=';', compression="zip", encoding ="ISO-8859-1", decimal=",")
    df_rendements = df_rendements.rename(columns={'ANNEE': 'annee', 'DEP': 'INSEE_DEP', 'CULT_SURF(ha)': 'CULT_SURF', 'CULT_REND(qx/t)': 'CULT_REND',
                                                  'CULT_PROD(t)': 'CULT_PROD'})
    df_rendements['INSEE_DEP'] = df_rendements['INSEE_DEP'].str.strip()
    df_rendements['DEPARTEMENT'] = df_rendements['DEPARTEMENT'].str.strip()
    df_rendements['ESPECES'] = df_rendements['ESPECES'].str.strip()

    df_rendements = df_rendements.loc[df_rendements.annee.isin(ANNEES)]

    return df_rendements