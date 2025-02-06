import os
import glob
import sys
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# IMPORTATIONS de scripts maison

fonctions_dir="/media/cl-ment-devenet/Partage/work/TEF/code/fonctions_communes/"
sys.path.append(fonctions_dir)

from fonctions import *

#FONCTIONS

def Retrieve_data_SAA(departements_a_tracer=[],cultures_a_tracer=[],indicateur=''):
    '''
    Cette fonction permet de récupérer les données de production, surface et rendements du fichier fragrimer.
    Cette fonction est conçue spécifiquement pour alimenter la fonction `Plot_data()` associée.
    
    INPUTS
    departements_a_tracer (list) Optionnel La liste des numéros de départements à récupérer. Numéro à deux chiffres passé en tant que chaîne de caractère (e.g. ['02','08','77'])
    cultures_a_tracer (list) Optionnel La liste des cultures à tracer. Numéro à deux chiffres passé en tant que chaîne de caractère (e.g. ['01','04']). La nomenclature est propre à cette fonction. Passez une liste vide pour que le programme vous présente la liste.
    indicateur (str) Optionnel '1' pour le rendement, '2' pour la production ou '3' pour les surfaces cultivées.

    OUTPUTS
    data (dict) Le dictionnaire des données récupérées. data={'dept':{'cult':[valeurs]}}
    depts_num_name (list) La liste numérotée des départements de France métropolitaine
    cultures (list) La liste numérotée des cultures disponibles dans le fichier source
    indicateur_dict (dict) Le dictionnaire contenant le nom, l’unité et un titre correspondant à l’indicateur séléctionné
    annees (list) La liste des années extraites
    departements_a_tracer IDEM INPUT
    cultures_a_tracer IDEM INPUT
    '''
    #### CHEMINS D’ENREGISTREMENT DES DONNÉES
    #Le chemin du répertoire où je stocke mes données
    bddpath='/media/cl-ment-devenet/Partage/bdd'

    #Le chemin en absolu du fichier de données
    fpath=glob.glob(os.path.join(bddpath,"FRANCEAGRIMER/*dep*"))[0]

    #### CHARGEMENT DES DONNÉES
    if 'full_file' not in locals(): #Évite la réexécution de cette partie du code si les données sont déjà en cache (utilité discutable)

        #Chargement du fichier Excel complet
        full_file=pd.read_csv(fpath,sep=';',encoding = "ISO-8859-1")

        #On se débarasse des années 2024 et 2025
        full_file=full_file[full_file['ANNEE']<2024]

        #Le fichier CSV inclu plein d’espaces entre les colonnes, je les enlève là où il y en a.
        for col in full_file.columns:
            try:
                full_file[col]=[val.strip() for val in full_file[col].values]
            except:
                continue

        #Dans les colonnes de données les valeurs en point flotant sont écrites avec des virgules. Je remplace par des points.
        for col in ['CULT_SURF','CULT_REND','CULT_PROD']:
            full_file[col] = full_file[col].str.replace(",",".").astype(float)

        #Récupération de la liste des départements numérotés
        depts_num_name = np.unique(full_file['DEP']+'-'+full_file['DEPARTEMENT'].values)

        #Récupération de la liste des cultures et ajout d’une numérotation
        cultures = [f"{i:02d} {item.strip()}" for i,item in enumerate(np.unique(full_file['ESPECES'].values),start=1)]

        #Sélection par l’utilisateur des départements, cultures et indicateur à tracer si non définis au préalable
        if len(departements_a_tracer)==0:
            departements_a_tracer = sel_options(depts_num_name)
        if len(cultures_a_tracer)==0:
            cultures_a_tracer = sel_options(cultures)
        if indicateur=='':
            indicateur = sel_indicateur()

        #Dictionnaire de paramètres pour la sélection et mise en forme de l’indicateur
        formating_dict = {
        '1':{'indic':'REND','titre':'Rendements agricoles','unit':'q/ha',},
        '2':{'indic':'PROD','titre':'Production agricole','unit':'q',},
        '3':{'indic':'SURF','titre':'Surfaces cultivées','unit':'ha',},
            }

        indicateur_dict = formating_dict[indicateur]

        #Récupération des données demandées et enregistrement dans un dictionnaire data={'dept':{'cult':[valeurs de l’indicateur,]}}
        data={}
        #Boucle pour chaque département
        for dept in departements_a_tracer:
            data[dept]={}
            for cult in cultures_a_tracer:
                cult_name=[c[3:] for c in cultures if cult in c][0]
                data[dept][cult]=full_file[(full_file['DEP']==dept)&(full_file['ESPECES']==cult_name)][f'CULT_{indicateur_dict['indic']}'].values

        #Récupération de la liste des années (liste commune à tous les départements et cultures)        
        annees=full_file[(full_file['DEP']==dept)&(full_file['ESPECES']==cult_name)]['ANNEE'].values

    return(data,depts_num_name,cultures,indicateur_dict,annees,departements_a_tracer,cultures_a_tracer)

def Plot_data(data,depts_num_name,cultures,indicateur_dict,annees,departements_a_tracer,cultures_a_tracer):
    '''
    Cette fonction permet de tracer les données extraites par la fonction Retrieve_data_SAA()
    Elle trace les séries temporelles de l’indicateur choisi pour les cultures choisie et fait un graph par département réunis dans une unique figure
    
    INPUTS
    data (dict) Le dictionnaire des données récupérées. data={'dept':{'cult':[valeurs]}}
    depts_num_name (list) La liste numérotée des départements de France métropolitaine
    cultures (list) La liste numérotée des cultures disponibles dans le fichier source
    indicateur_dict (dict) Le dictionnaire contenant le nom, l’unité et un titre correspondant à l’indicateur séléctionné
    annees (list) La liste des années extraites
    departements_a_tracer IDEM INPUT
    cultures_a_tracer IDEM INPUT

    OUTPUTS
    Affichage de la figure sur la sortie principale
    Enregistrement de la figure au format PNG dans le dossier courant
    '''
    #Paramètres de mise en forme
    indicateur_name = indicateur_dict['indic']
    titre = indicateur_dict['titre']
    unit = indicateur_dict['unit']
    savename = f'{indicateur_name}_dep_{'-'.join(departements_a_tracer)}_cult_{'-'.join(cultures_a_tracer)}.png'

    #Paramètres de la figure
    nb_subplots=len(departements_a_tracer)
    nb_columns=nb_subplots if nb_subplots <=3 else 3
    nb_rows=math.ceil(nb_subplots/nb_columns)

    #Début du tracé
    plt.close()
    fig, axs = plt.subplots(nb_rows, nb_columns,sharex=True,sharey=True,clear=True,figsize=(29,21))
    fig.suptitle(titre,fontweight='bold',fontsize=20)

    #Gestion du cas où il n’y aurai qu’une région, donc qu’un graph à tracer
    if not isinstance(axs,np.ndarray):
        axs=np.array([axs])
    else:
        axs=np.array(axs).ravel()

    #Boucle pour chaque région
    for i,dept in enumerate(departements_a_tracer):
        departement_name=[c for c in depts_num_name if dept in c][0]
        #Boucle par culture
        for cult in cultures_a_tracer:
            cult_name=[c[3:] for c in cultures if cult in c][0]
            axs[i].plot(annees,data[dept][cult],label=cult_name)

        axs[i].legend()
        axs[i].set_title(departement_name)
        axs[i].set_ylabel(unit, fontweight='bold')
        axs[i].set_xlabel('Années', fontweight='bold')
        axs[i].grid(visible=True)

    plt.savefig(savename)
    print(f'Figure enregistrée sous :\n{os.path.abspath(savename)}')
    plt.show()

#EXECUTION
#Le bloc est commenté pour qu’il ne s’exécute pas lors de l’appel du script par correl.py

#Plot_data(*Retrieve_data_SAA(
#    departements_a_tracer=['02','10','27','28','45','51','60','77','78','89','91','95'],
#    cultures_a_tracer=['11','24','13'],
#    indicateur='1'
#    ))