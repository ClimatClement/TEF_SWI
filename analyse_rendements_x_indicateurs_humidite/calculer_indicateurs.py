import geopandas
import pandas
from pandas.core.interchange.dataframe_protocol import DataFrame

from SAA_analysis.calculer_donnees_rendements_finales import calculer_donnees_rendements
from SWI_analysis.calculer_donnees_humidite_finales import calculer_donnees_humidite
from config import BDD_CONTOURS_DEPARTEMENTS_PATH


def calculer_donnees_moyennes_par_departements(mois: int, espece: str):
    gdf_departements = geopandas.read_file(BDD_CONTOURS_DEPARTEMENTS_PATH)

    df_donnees_humidite = calculer_donnees_humidite(mois=mois)
    df_selection = df_donnees_humidite.loc[df_donnees_humidite.annee == 2023] #attention, pour la Corse, données apd 2017
    gdf_departements = pandas.merge(gdf_departements, df_selection, on="INSEE_DEP", how="left")

    df_donnees_rendements = calculer_donnees_rendements()
    df_selection = df_donnees_rendements.loc[(df_donnees_rendements.annee == 2023) & (df_donnees_rendements.ESPECES == espece)]
    gdf_departements = pandas.merge(gdf_departements, df_selection, on="INSEE_DEP", how="left")

    gdf_departements.loc[:, ['INSEE_DEP']].drop_duplicates().sort_values(by="INSEE_DEP")
    return gdf_departements


def calculer_donnees_par_annees_et_departements(mois: int) -> DataFrame:
    df_indicateurs_humidite = calculer_donnees_humidite(mois)
    df_rendements = calculer_donnees_rendements()

    df = pandas.merge(
        df_rendements,
        df_indicateurs_humidite,
        on=['annee', 'INSEE_DEP']
    )

    return df



