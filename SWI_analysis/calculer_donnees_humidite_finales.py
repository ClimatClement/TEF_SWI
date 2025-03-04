import pandas

from SIM2.calculer_donnees_sim2 import charger_donnees_sim2_par_departements_et_jours
from config import ANNEES, BDD_DATA_HUMIDITES_PAR_DEPARTEMENTS_ET_MOIS_PATH
from fonctions_communes.calculer_ecarts_a_la_moyenne import calculer_ecarts_a_la_moyenne


VARIABLE = 'SWI_MENSUEL'
VARIABLE_UTILISEE = 'SWI_M'

def calculer_donnees_humidite(mois: int):
    df_indicateurs_humidite = pandas.read_csv(BDD_DATA_HUMIDITES_PAR_DEPARTEMENTS_ET_MOIS_PATH, sep=";")
    df_indicateurs_humidite = df_indicateurs_humidite.loc[
        df_indicateurs_humidite.annee.isin(ANNEES) &
        (df_indicateurs_humidite.mois == mois),
        ['INSEE_DEP', 'annee', 'SWI_UNIF_MENS3', 'reserve_mm', 'humidite_mm']
    ]

    df_indicateurs_swi_sim2 = charger_donnees_sim2_par_departements_et_jours()
    df_indicateurs_swi_sim2['annee'] = df_indicateurs_swi_sim2.DATE.dt.year
    df_indicateurs_swi_sim2['mois'] = df_indicateurs_swi_sim2.DATE.dt.month
    df_indicateurs_swi_sim2 = df_indicateurs_swi_sim2.groupby(["INSEE_DEP", "annee", "mois"])[["SWI_Q"]].mean().reset_index()
    df_indicateurs_swi_sim2 = df_indicateurs_swi_sim2.rename(columns={"SWI_Q": "SWI_M"})
    df_indicateurs_swi_sim2['SWI_M3'] = df_indicateurs_swi_sim2['SWI_M'].rolling(window=3, min_periods=1).mean()
    df_indicateurs_swi_sim2 = df_indicateurs_swi_sim2.loc[
        df_indicateurs_swi_sim2.annee.isin(ANNEES) &
        (df_indicateurs_swi_sim2.mois == mois),
        ['INSEE_DEP', 'annee', 'SWI_M', 'SWI_M3']
    ]
    df_indicateurs_humidite = pandas.merge(df_indicateurs_humidite, df_indicateurs_swi_sim2, on=["INSEE_DEP", "annee"])

    df_indicateurs_humidite[VARIABLE] = df_indicateurs_humidite[VARIABLE_UTILISEE]
    df_indicateurs_humidite['humidite_mm'] = (df_indicateurs_humidite[VARIABLE] * df_indicateurs_humidite['reserve_mm']).round()

    for c in ['SWI_UNIF_MENS3', 'SWI_M', 'SWI_M3', VARIABLE, 'humidite_mm']:
        df_indicateurs_humidite = calculer_ecarts_a_la_moyenne(
            df_indicateurs_humidite,
            on=['INSEE_DEP'],
            colonne=c
        )
    return df_indicateurs_humidite
