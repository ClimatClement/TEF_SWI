import pandas

from config import ANNEES, BDD_DATA_HUMIDITES_PAR_DEPARTEMENTS_ET_MOIS_PATH
from fonctions_communes.calculer_ecarts_a_la_moyenne import calculer_ecarts_a_la_moyenne


def calculer_donnees_humidite(mois: int):
    df_indicateurs_humidite = pandas.read_csv(BDD_DATA_HUMIDITES_PAR_DEPARTEMENTS_ET_MOIS_PATH, sep=";")
    df_indicateurs_humidite = df_indicateurs_humidite.loc[
        df_indicateurs_humidite.annee.isin(ANNEES) &
        (df_indicateurs_humidite.mois == mois),
        ['INSEE_DEP', 'annee', 'SWI_UNIF_MENS3', 'reserve_mm', 'humidite_mm']
    ]
    for c in ['SWI_UNIF_MENS3', 'humidite_mm']:
        df_indicateurs_humidite = calculer_ecarts_a_la_moyenne(
            df_indicateurs_humidite,
            on=['INSEE_DEP'],
            colonne=c
        )
    return df_indicateurs_humidite
