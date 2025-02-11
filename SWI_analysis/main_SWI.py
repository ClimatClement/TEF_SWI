import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from config import BDD_SWI_AVEC_DEPARTEMENTS, BDD_SWI_DATA_PATH, OUTPUT_DATA_PATH
from fonctions_communes.fonctions import sel_options

#FONCTIONS

def Retrieve_data_SWI(departements_a_tracer:list=[],months:list=[]):
    '''
    Cette fonction permet de récupérer les données de SWI UNIFORME de MétéoFrance.
    Cette fonction est conçue spécifiquement pour alimenter la fonction `Plot_data()` associée.
    
    INPUTS
    - departements_a_tracer (list) Optionnel La liste des numéros de départements à récupérer. Numéro à deux chiffres passé en tant que chaîne de
    caractères (e.g. ['02','08','77'])
    - months (list) Optionnel La liste des numéros (int) de mois à récupérer ; si plusieurs mois demandés, la fonction renvoie le SWI moyen ; si
    liste vide, la moyenne annuelle est renvoyée.

    OUTPUTS
    data (dict) Le dictionnaire des données récupérées. data={'dept':[valeurs]}
    months IDEM INPUT
    departements_a_tracer IDEM INPUT
    metadonnees (pandas.DataFrame) Le dataframe contenant pour chaque maille de la grille SAFRAN : son numéro, ses coordonnées, le nom du département, le numéro du département, le numéro de la région. Ces données sont issues du fichier CSV créé par le script joindre_numeros_de_mailles_et_departements.py
    '''

    metadonnees=pd.read_csv(BDD_SWI_AVEC_DEPARTEMENTS,sep=';')

    #Traitement des cas où les arguments departements_a_tracer et months ne sont pas passés.
    if len(departements_a_tracer)==0:
        departements_a_tracer = sel_options(sorted((metadonnees['INSEE_DEP']+' - '+metadonnees['NOM']).unique()))
    if len(months)==0:
        months = [int(x) for x in sel_options(np.arange(1,13),'mois')]

    #Début d’extraction
    data={}
    for dept in departements_a_tracer:
        #Identification des numéros de mailles couvrant le département à extraire
        mailles_a_recup = metadonnees[metadonnees.loc[:,'INSEE_DEP']==str(dept)]['#num_maille'].values
        mini_num_maille = min(mailles_a_recup)
        maxi_num_maille = max(mailles_a_recup)

        #Réduction de la liste des fichiers de données à lire à ceux contenant les mailles recherchées
        all_fpaths=[fp for fp in Path.glob(BDD_SWI_DATA_PATH, '*')]    #Liste de tous les fichiers de données
        files_to_open=[]
        for fname in all_fpaths:
            prem_maille = int(fname.name.split('.')[1].split('-')[0])    #Numéro de la première maille disponible dans ce fichier
            der_maille = int(fname.name.split('.')[1].split('-')[1])     #Numéro de la dernière maille disponible dans ce fichier
            if not ((prem_maille<mini_num_maille)&(der_maille<mini_num_maille))|((prem_maille>maxi_num_maille)&(der_maille>maxi_num_maille)):   #Vérification que le fichier contient au moins une maille recherchée
                files_to_open.append(fname)

        #Ouverture des fichiers de données et enregistrement des données des mailles recherchées dans un dataframe temporaire
        initialized=False
        for fname in files_to_open:
            temp_df=pd.read_csv(fname,sep=';').drop(columns=['LAMBX','LAMBY'])
            temp_df=temp_df[temp_df['NUMERO'].isin(mailles_a_recup)]
            if not initialized:
                raw_data=temp_df.copy()
                initialized=True
            else:
                raw_data=pd.concat([raw_data,temp_df])

        #Nettoyage et mise en forme des données (type floats et date)
        raw_data['SWI_UNIF_MENS3']=raw_data['SWI_UNIF_MENS3'].str.replace(",",".").astype(float)
        raw_data=raw_data.groupby('DATE').mean()['SWI_UNIF_MENS3'].reset_index()
        raw_data['new_date']=pd.to_datetime(raw_data['DATE'], format='%Y%m').dt.date
        raw_data['new_date']=pd.to_datetime(raw_data['new_date'], errors='coerce')

        #Réduction aux mois de la liste months
        filtered_data=raw_data[raw_data['new_date'].dt.month.isin(months)].copy()
        
        #Moyenne annuelle des mois sélectionnés
        filtered_data['year']=filtered_data['new_date'].dt.year
        
        #Enregistrement des données du département dans le dictionnaire data
        data[dept]=filtered_data.groupby('year').mean()['SWI_UNIF_MENS3']

    return(data,months,departements_a_tracer,metadonnees)

def Plot_data(data,months,departements_a_tracer,metadonnees):
    '''
    Cette fonction permet de tracer les données extraites par la fonction Retrieve_data_SWI()
    Elle trace les séries temporelles de l’indicateur choisi et fait un graph par département réunis dans une unique figure
    
    INPUTS
    data (dict) Le dictionnaire des données récupérées. data={'dept':pd.DataFrame()}}
    months (list) La liste des numéros (int) de mois constituant les données (utilisé pour le titre et le nom d’enregistrement)
    departements_a_tracer IDEM INPUT
    metadonnees Le dataframe contenant pour chaque maille de la grille SAFRAN : son numéro, ses coordonnées, le nom du département, le numéro du département, le numéro de la région. Ces données sont issues du fichier CSV créé par le script joindre_numeros_de_mailles_et_departements.py

    OUTPUTS
    Affichage de la figure sur la sortie principale
    Enregistrement de la figure au format PNG dans le dossier courant
    '''

    #Paramètres du titre et du nom d’enregistrement
    titre = f'Soil Wetness Indicator (SWI) UNIFORM\nfor months {months}'
    indicateur_name = 'SWI_UNIF'
    unit = '-'
    savename = OUTPUT_DATA_PATH / f'{indicateur_name}_dep_{"-".join(departements_a_tracer)}_month_{"-".join([str(m) for m in months])}.png'

    #Paramètres de la figure
    nb_subplots=len(departements_a_tracer)
    nb_columns=nb_subplots if nb_subplots <=3 else 3
    nb_rows=math.ceil(nb_subplots/nb_columns)

    plt.close() #On ferme tout plot pré-existant par précaution

    fig, axs = plt.subplots(nb_rows, nb_columns,sharex=True,sharey=True,clear=True,figsize=(12*nb_columns,10*nb_rows))
    fig.suptitle(titre,fontweight='bold',fontsize=20)

    #Gestion du cas où il n’y aurait qu’une région, donc qu’un graph à tracer
    if not isinstance(axs,np.ndarray):
        axs=np.array([axs])
    else:
        axs=np.array(axs).ravel()

    #Boucle pour chaque région
    for i,dept in enumerate(departements_a_tracer):
        departement_name=metadonnees[metadonnees.loc[:,'INSEE_DEP']==dept]['NOM'].values[0]

        annees=data[dept].index
        axs[i].plot(annees,data[dept])
        axs[i].set_xlim(2000,2024)
        axs[i].set_title(departement_name)
        axs[i].set_ylabel(unit, fontweight='bold')
        axs[i].set_xlabel('Années', fontweight='bold')
        axs[i].grid(visible=True)

    plt.savefig(savename)
    print(f'Figure enregistrée sous :\n{(savename)}')
    plt.show()

#EXECUTION
#Le bloc est commenté pour qu’il ne s’exécute pas lors de l’appel du script par correl.py

Plot_data(*Retrieve_data_SWI(
               departements_a_tracer=['02','10','27','28','45','51','60','77','78','89','91','95']
               ))