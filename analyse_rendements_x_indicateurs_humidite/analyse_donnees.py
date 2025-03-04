import geopandas
import pandas
from matplotlib import pyplot as plt
from pandas.plotting import scatter_matrix
from pathlib import Path

from SAA_analysis.calculer_donnees_rendements_finales import calculer_donnees_rendements
from SWI_analysis.calculer_donnees_humidite_finales import VARIABLE
from analyse_rendements_x_indicateurs_humidite.calculer_indicateurs import calculer_donnees_par_annees_et_departements, calculer_donnees_humidite, \
    calculer_donnees_moyennes_par_departements
from config import OUTPUT_DATA_PATH, BDD_CONTOURS_DEPARTEMENTS_PATH, ANNEES
from fonctions_communes.reinitialiser_dossier import reinitialiser_dossier

ESPECE = "Blé tendre d'hiver" #"Colza" | "Orge" | "Blé tendre d'hiver" | "Maïs (grain et semence)"
MOIS = 6

DOSSIER_OUTPUT = OUTPUT_DATA_PATH / 'analyses'

DOSSIER_OUTPUT_ESPECE_MOIS = DOSSIER_OUTPUT / Path(f"{ESPECE}-mois {MOIS}")
reinitialiser_dossier(DOSSIER_OUTPUT_ESPECE_MOIS)

def analyser_donnees():
    tracer_rendements_par_annees()
    tracer_cartes_moyennes_annuelles()
    tracer_cartes_par_annees()
    tracer_correlations_moyennes()
    tracer_correlations()
    tracer_correlations_par_departements()


def tracer_rendements_par_annees():
    df = calculer_donnees_rendements()

    lignes = ["Colza", "Orge", "Blé tendre d'hiver", "Maïs (grain et semence)"]
    colonnes = ['CULT_REND', 'CULT_REND_ECART_ABSOLU', 'CULT_REND_ECART_RELATIF']
    fig, axes = plt.subplots(nrows=len(lignes), ncols=len(colonnes), figsize=(20, 12))
    for l, ligne in enumerate(lignes):
        for c, colonne in enumerate(colonnes):
            df_selection = df.loc[df.ESPECES == ligne].groupby(['DEPARTEMENT'])
            for nom, groupe in df_selection:
                axes[l, c].plot(groupe['annee'], groupe[colonne], linestyle='-', lw=0.2)
                axes[l, c].set_xlabel(ligne)
                axes[l, c].set_ylabel(colonne)

    plt.legend()
    plt.savefig(DOSSIER_OUTPUT / 'rendements_par_annees.png')


def tracer_cartes_moyennes_annuelles():
    gdf_departements = calculer_donnees_moyennes_par_departements(MOIS, ESPECE)

    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(20, 12))

    gdf_departements.plot(ax=axes[0, 0], column='CULT_REND_MOYEN', cmap='viridis_r', edgecolor='black', linewidth=0.5, legend=True)
    axes[0, 0].set_title('q/ha')

    gdf_departements.plot(ax=axes[0, 1], column='CULT_SURF_MOYEN', cmap='viridis_r', edgecolor='black', linewidth=0.5, legend=True)
    axes[0, 1].set_title('ha')

    gdf_departements.plot(ax=axes[0, 2], column='reserve_mm', cmap='viridis_r', edgecolor='black', linewidth=0.5, legend=True)
    axes[0, 2].set_title('reserve_mm')

    gdf_departements.plot(ax=axes[1, 0], column='SWI_UNIF_MENS3_MOYEN', cmap='viridis_r', edgecolor='black', linewidth=0.5, legend=True)
    axes[1, 0].set_title('SWI_UNIF_MENS3')

    gdf_departements.plot(ax=axes[1, 1], column='SWI_M_MOYEN', cmap='viridis_r', edgecolor='black', linewidth=0.5, legend=True)
    axes[1, 1].set_title('SWI_M_MOYEN')

    gdf_departements.plot(ax=axes[1, 2], column='SWI_M3_MOYEN', cmap='viridis_r', edgecolor='black', linewidth=0.5, legend=True)
    axes[1, 2].set_title('SWI_M3_MOYEN')

    gdf_departements.plot(ax=axes[2, 0], column='humidite_mm_MOYEN', cmap='viridis_r', edgecolor='black', linewidth=0.5, legend=True)
    axes[2, 0].set_title('humidite_mm')

    plt.suptitle(f"{ESPECE} | mois={MOIS}")
    plt.tight_layout()
    plt.savefig(DOSSIER_OUTPUT_ESPECE_MOIS / 'cartes.png')


def tracer_cartes_par_annees():
    gdf_departements = geopandas.read_file(BDD_CONTOURS_DEPARTEMENTS_PATH)

    df = calculer_donnees_par_annees_et_departements(MOIS)
    df_selection = df.loc[(df.ESPECES == ESPECE)]

    n_colonnes = 2
    fig, axes = plt.subplots(nrows=len(ANNEES), ncols=n_colonnes, figsize=(10, 80))
    for a, annee in enumerate(ANNEES):
        gdf = pandas.merge(gdf_departements, df_selection.loc[df_selection.annee == annee], on="INSEE_DEP", how="left")
        gdf.plot(ax=axes[a, 0], column='CULT_REND_ECART_RELATIF', cmap='RdBu', edgecolor='black', linewidth=0.5, legend=True, vmin=-30, vmax=30)
        axes[a, 0].set_title(f'{annee} - CULT_REND_ECART_RELATIF')
        gdf.plot(ax=axes[a, 1], column=f'{VARIABLE}_ECART_RELATIF', cmap='RdBu', edgecolor='black', linewidth=0.5, legend=True, vmin=-30,
                 vmax=30)
        axes[a, 1].set_title(f'{annee} - {VARIABLE}_ECART_RELATIF {MOIS}')

    plt.suptitle(f"CULT_REND_ECART_RELATIF - {ESPECE} - mois {MOIS}")
    plt.savefig(DOSSIER_OUTPUT_ESPECE_MOIS / f'cartes-annuelles.png')


def tracer_correlations_moyennes():

    df_departements = calculer_donnees_moyennes_par_departements(MOIS, ESPECE).drop(columns=['geometry'])

    scatter_matrix(df_departements.loc[:, ['CULT_REND_MOYEN', f'{VARIABLE}_ECART_RELATIF', 'reserve_mm', 'humidite_mm_MOYEN']], alpha=0.8, figsize=(6,
                                                                                                                                                    6), diagonal='kde')
    plt.tight_layout()
    plt.savefig(DOSSIER_OUTPUT_ESPECE_MOIS / 'correlations_moyennes.png')


def tracer_correlations():

    df = calculer_donnees_par_annees_et_departements(mois=MOIS)

    df_selection = df.loc[
        (df.ESPECES == ESPECE)
    ]

    lignes = [VARIABLE, 'humidite_mm', f'{VARIABLE}_ECART_ABSOLU', f'{VARIABLE}_ECART_RELATIF']
    colonnes = ['CULT_REND', 'CULT_REND_ECART_ABSOLU', 'CULT_REND_ECART_RELATIF']
    fig, axes = plt.subplots(nrows=len(lignes), ncols=len(colonnes), figsize=(20, 12))
    df_selection.loc[:, 'couleur']  = '#0008884d'
    df_selection.loc[df_selection.CULT_SURF > df_selection.CULT_SURF.median(), 'couleur'] = '#0064284d'
    for l, ligne  in enumerate(lignes):
        for c, colonne  in enumerate(colonnes):
            axes[l, c].scatter(df_selection[ligne], df_selection[colonne], s=0.5, c=df_selection['couleur'])
            axes[l, c].set_xlabel(ligne)
            axes[l, c].set_ylabel(colonne)
    plt.legend()
    plt.savefig(DOSSIER_OUTPUT_ESPECE_MOIS / 'correlations.png')


def tracer_correlations_par_departements():
    departements = ['24', '28', '83', '62', '77', '21', '64', '41'] #[]

    df = calculer_donnees_par_annees_et_departements(mois=MOIS)

    df_selection = df.loc[df.ESPECES == ESPECE]
    if len(departements) > 0:
        df_selection = df_selection.loc[df_selection.INSEE_DEP.isin(departements)]

    lignes = [VARIABLE, 'humidite_mm']
    colonnes = ['CULT_REND', 'CULT_REND_ECART_ABSOLU', 'CULT_REND_ECART_RELATIF']
    fig, axes = plt.subplots(nrows=len(lignes), ncols=len(colonnes), figsize=(20, 12))
    groupes = df_selection.groupby(['DEPARTEMENT'])
    for l, ligne  in enumerate(lignes):
        for c, colonne  in enumerate(colonnes):
            for nom, groupe in groupes:
                axes[l, c].plot(groupe[ligne], groupe[colonne], marker='o', linestyle='-', markersize=1, label=nom)
                axes[l, c].set_xlabel(ligne)
                axes[l, c].set_ylabel(colonne)
    plt.legend()
    plt.savefig(DOSSIER_OUTPUT_ESPECE_MOIS / 'correlations_par_departements.png')
