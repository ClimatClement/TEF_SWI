Contact clement.devenet@climatclement.com
Projet sous licence CC BY-NC-SA 4.0

Configuration :
Python 3.12.3

Librairies :
numpy 2.0.0
pandas 2.2.3
geopandas 1.0.1
shapely 2.0.6
matplotlib 3.9.2

Arborescence:

├── fonctions_communes
│   └── fonctions.py
├── README.txt
├── recherche_de_correlation
│   └── correl.py
├── SAA_analysis
│   └── main_SAA.py
└── SWI_analysis
    ├── joindre_numeros_de_mailles_et_departements.py
    └── main_SWI.py

/!\ RÉCUPÉRATION DES DONNÉES EN LIGNE /!\
Vous devez au préalable avoir téléchargé les données suivantes et mis à jour les chemins d’accès dans les différents scripts (utilisez le mot clé "path" pour trouver les chemins à mettre à jour):
- SWI : https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Swi/SWI_Package_1969-2023.zip
- SAA fragrimer : https://visionet.franceagrimer.fr/Pages/OpenDocument.aspx?fileurl=SeriesChronologiques%2fproductions%20vegetales%2fgrandes%20cultures%2fsurfaces%2cproductions%2crendements%2fSCR-GRC-hist_dep_surface_prod_cult_cer-A25.zip&telechargersanscomptage=oui
- BDTOPO : https://data.geopf.fr/telechargement/download/ADMIN-EXPRESS/ADMIN-EXPRESS_3-2__SHP_LAMB93_FXX_2024-12-18/ADMIN-EXPRESS_3-2__SHP_LAMB93_FXX_2024-12-18.7z

