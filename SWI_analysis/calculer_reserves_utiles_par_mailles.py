import geopandas
import pandas
import shapely
from geopandas import GeoDataFrame
from pandas import DataFrame

from config import BDD_SWI_METADATA_PATH, OUTPUT_DATA_PATH, BDD_RESERVES_UTILES, CRS_PROJET

#Numéros classes → réserves moyennes en mm
DICTIONNAIRE_CLASSES_RESERVES_UTILES = {
    1: 25,  #<50mm
    2: 75,  #50-100mm
    3: 125, #100-150mm
    4: 175, #150-200mm
    5: 225, #>200mm
    9: 0    #Lacs, villes
}

def creer_df_reserves_utiles():
    print("## Calcul des reserves utiles des mailles ##")
    gdf_grilles_mailles = _creer_gdf_grilles_mailles()
    gdf_grilles_mailles.to_file(OUTPUT_DATA_PATH / 'mailles.shp')

    gdf_reserves_utiles = _charger_gdf_reserves_utiles()

    gdf_intersection_mailles_et_reserves_utiles = _intersecter_mailles_et_reserves_utiles(gdf_grilles_mailles, gdf_reserves_utiles)
    gdf_intersection_mailles_et_reserves_utiles.to_file(OUTPUT_DATA_PATH / 'intersection.shp')

    df_reserves_utiles = _calculer_df_reserves_utiles(gdf_intersection_mailles_et_reserves_utiles)
    df_reserves_utiles.to_csv(OUTPUT_DATA_PATH / 'mailles_avec_reserves_utiles_estimees.csv', sep=";", index=False)


def _creer_gdf_grilles_mailles() -> GeoDataFrame:
    df_mailles = pandas.read_csv(BDD_SWI_METADATA_PATH, sep=';', header=4)

    taille_maille = 8000 #metres

    # lambx,lamby : coordonnées de la maille en Lambert 2 étendu, en hectomètres
    df_mailles['geometry'] = [
        shapely.geometry.box(x1, y1, x2, y2) for (x1, y1, x2, y2) in zip(
            100 * df_mailles['lambx'] - taille_maille / 2,
            100 * df_mailles['lamby'] - taille_maille / 2,
            100 * df_mailles['lambx'] + taille_maille / 2,
            100 * df_mailles['lamby'] + taille_maille / 2)
    ]
    gdf_grilles_mailles = geopandas.GeoDataFrame(df_mailles, crs="EPSG:27572").to_crs(CRS_PROJET)
    return gdf_grilles_mailles


def _charger_gdf_reserves_utiles() -> GeoDataFrame:
    gdf_reserves_utiles = geopandas.read_file(BDD_RESERVES_UTILES).to_crs(CRS_PROJET)
    gdf_reserves_utiles["reserve_mm"] = gdf_reserves_utiles["classe"].map(DICTIONNAIRE_CLASSES_RESERVES_UTILES)
    return gdf_reserves_utiles


def _intersecter_mailles_et_reserves_utiles(gdf_grille_mailles: GeoDataFrame, gdf_reserves_utiles: GeoDataFrame) -> GeoDataFrame:
    return (
        geopandas.overlay(gdf_grille_mailles, gdf_reserves_utiles, how="intersection")
        .assign(
            superficie_km2=lambda x: x.geometry.area * 10 ** -6,
        )
    )


def _calculer_df_reserves_utiles(gdf_intersection_mailles_et_reserves_utiles: GeoDataFrame) -> DataFrame:
    df_intersection_mailles_et_reserves_utiles = gdf_intersection_mailles_et_reserves_utiles.drop(columns='geometry').set_index("#num_maille")
    df_intersection_mailles_et_reserves_utiles["produit_reserve_mm_superficie_km2"] = df_intersection_mailles_et_reserves_utiles["reserve_mm"] * df_intersection_mailles_et_reserves_utiles["superficie_km2"]
    df_mailles = df_intersection_mailles_et_reserves_utiles.loc[:, ["lambx93", "lamby93"]].drop_duplicates()
    df_mailles["reserve_mm"] = df_intersection_mailles_et_reserves_utiles.groupby("#num_maille")["produit_reserve_mm_superficie_km2"].sum() / df_intersection_mailles_et_reserves_utiles.groupby(
        "#num_maille")["superficie_km2"].sum()
    return df_mailles.reset_index()
