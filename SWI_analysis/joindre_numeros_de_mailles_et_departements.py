import os
import glob
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

'''
Le SWI UNIFORME de MétéoFrance est fourni sur la grille SAFRAN. Cette grille est composée de plusieurs milliers de points.
Le fichier de métadonnées donne les coordonnées de chaque point (maille).
Nous avons besoin d’identifier le département dans lequel se trouve chaque point pour pouvoir faire une étude par département.
Ce code joint les métadonnées SWI UNIFORME et le découpage départemental issu de la BDTOPO de l’IGN.
Le résultat est un fichier CSV (sep = ';') contenant la liste des mailles, le nom du département, le numéro INSEE de département et le numéro INSEE de la région.
'''

#Le chemin du répertoire où je stocke mes données
bddpath='/media/cl-ment-devenet/Partage/bdd'

### On récupère donc les métadonnées de la grille SAFRAN
metadonnees_path=glob.glob(os.path.join(bddpath,"METEOFRANCE/SWI/*meta*"))[0]
df_metadonnees=pd.read_csv(metadonnees_path,sep=';',header=4)

### On récupère ensuite les limites administratives des départements (France métropolitaine)
limit_depts_path=glob.glob(os.path.join(bddpath,"IGN/BDTOPO/Source/ADMIN*/ADMIN*/1_*/*/DEPARTEMENT.shp"))[0]
limit_depts=gpd.read_file(limit_depts_path)

### Petite transformation du dataframe des métadonnées SAFRAN en Geodataframe
geometry = [Point(xy) for xy in zip(df_metadonnees['lambx93'], df_metadonnees['lamby93'])]
gdf_metadonnees = gpd.GeoDataFrame(df_metadonnees, geometry=geometry, crs=limit_depts.crs)

### Jointure des deux jeux de données
gdf_result = gpd.sjoin(
    gdf_metadonnees[['#num_maille','lambx93','lamby93','geometry']],
    limit_depts,
    how='left'
    )

### Les mailles litoralles dont le centre est en mer n’intersectent aucun département
### Il faut donc une étape supplémentaire pour celles-ci
### D’abord on isole ces mailles
coast_points = gdf_result[gdf_result['INSEE_DEP'].isna()]

### On fait cette fois un joint par plus proche voisin
nearest_join = gpd.sjoin_nearest(
    coast_points[['#num_maille','lambx93','lamby93','geometry']],
    limit_depts,
    how='left',
    distance_col='distance_to_nearest'
    )

### On met à jour le Geodataframe résultant de la première étape avec les valeurs des points cotiers.
gdf_result.update(nearest_join)

### On dispose à présent de la liste des mailles de la grille SAFRAN labellisée avec le département et la région
### On enregistre ces métadonnées améliorées
### La géométrie ne peut pas être enregistrée tel quel au format CSV et comme on n’en a plus besoin on la laisse tomber.
gdf_result.drop(columns='geometry').to_csv(metadonnees_path[:-4]+'_wt_dep_reg.csv', index=False,sep=';')
print(f"Fichier enregistré sous : {os.path.abspath(metadonnees_path[:-4]+'_wt_dep_reg.csv')}")