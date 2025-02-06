import os
import sys
import textwrap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.colors as mcolors

# IMPORTATIONS de scripts maison

SAA_dir="/media/cl-ment-devenet/Partage/work/TEF/code/SAA_analysis/"
sys.path.append(SAA_dir)

SWI_dir="/media/cl-ment-devenet/Partage/work/TEF/code/SWI_analysis/"
sys.path.append(SWI_dir)

from main_SWI import Retrieve_data_SWI
from main_SAA import Retrieve_data_SAA

# Un script pour combiner les données SAA et SWI UNIFORME
# L’objectif est de rechercher une correlation entre les rendements agricoles et le SWI UNIFORME

#FONCTIONS
## Plot_TS_and_scatter_SAA_SWI(SWI,SAA,cultures_a_tracer,months,month_names,offset,indicateur_dict,metadonnees,depts,annees,cultures,anom:bool=False)
## Plot_scatter_SAA_SWI(SWI,SAA,departements_a_tracer,cultures_a_tracer,months,month_names,offset,anom:bool=False)
## Boxplot_SWI(SWI,SAA,annees,months,culture_a_tracer,offset:int=0,sort_by:str='SAA',figsize=(20,15))

def Plot_TS_and_scatter_SAA_SWI(SWI,SAA,cultures_a_tracer,months,month_names,offset,indicateur_dict,metadonnees,depts,annees,cultures,anom:bool=False):
    '''
    Cette fonction trace une figure composée de 2 subplots côte-à-côte par département

    INPUTS
    SWI (dict={str:pandas.DataFrame})   Les données de SWI issues de la fonction Retrieve_data_SWI
    SAA (dict={str:dict={str:pandas.DataFrame}})    Les données de SWI issues de la fonction Retrieve_data_SAA
    cultures_a_tracer (list=[str])  La liste des cultures à tracer. Numéro à deux chiffres passé en tant que chaîne de caractère (e.g. ['01','04']). La nomenclature est propre à cette fonction. Passez une liste vide pour que le programme vous présente la liste.
    months (list=[int]) La liste des numéros de mois de SWI à prendre en compte (la valeur tracée sera la moyenne de ces mois)
    month_names (dict={int:str})    Le dictionnaire des numéros et noms de mois ({1:'janvier';…})
    offset (int)    Le nombre d’années d’écart entre rendements et SWI (e.g. 1 pour le SWI de l’année précédent les rendements)
    indicateur_dict (dict={'indic': str, 'titre': str, 'unit': str}) Le dictionnaire contenant le nom de l’indicateur SAA à tracer ('REND', 'SURF', ou 'PROD'), le nom complet qui sera utilisé dans le titre de la figure et l’unité
    metadonnees (pandas.DataFrame) Le dataframe contenant pour chaque maille de la grille SAFRAN : son numéro, ses coordonnées, le nom du département, le numéro du département, le numéro de la région. Ces données sont issues du fichier CSV créé par le script joindre_numeros_de_mailles_et_departements.py
    depts (list=[str]) La liste des départements à tracer (liste de strings à 2 digits)
    annees (list=[int]) La liste des années à tracer (dans le cas où offset est non nul, ce sont les années des rendements qu’il faut passer)
    cultures (list[str]) La liste des numéros et noms complets des cultures. Cette liste sert à la création des titres et légendes.
    anom (bool) (opt, default=False) Présentation des résultats en anomalie par rapport à la moyenne (anom=True) ou en valeurs absolues (anom=False)

    OUTPUTS
    Affichage de la figure sur la sortie principale
    Enregistrement de la figure au format PNG dans le dossier courant
    '''

    unit = indicateur_dict['unit']
    departement_name=metadonnees[metadonnees.loc[:,'INSEE_DEP']==depts[0]]['NOM'].values[0]
    titre_offset=' de l’année précédente' if offset==1 else ''
    titre_col1=f'Séries temporelles des {indicateur_dict['titre'].lower()} et\ndu SWI UNIFORME du mois de {month_names[months[0]]}{titre_offset}{'\nANOMALIES' if anom else ''}\n{departement_name}'
    titre_col2=f'Nuage de point des {indicateur_dict['titre'].lower()} en fonction\ndu SWI UNIFORME du mois de {month_names[months[0]]}{titre_offset}{'\nANOMALIES' if anom else ''}\n{departement_name}'
    savename = f'all_depts_TS_and_scatter{'_ANOM' if anom else ''}_cult_{'-'.join(cultures_a_tracer)}_SWI-month{'-'.join([str(m) for m in months])}_offsetN-{offset}.png'

    #Paramètres de la figure
    nb_columns=2
    nb_rows=len(depts)

    plt.close()
    fig, axs = plt.subplots(nb_rows, nb_columns,clear=True,figsize=(12*nb_columns,10*nb_rows))

    SWI_ymin,SWI_ymax=0,1.2

    for i,dept in enumerate(depts):
        departement_name=metadonnees[metadonnees.loc[:,'INSEE_DEP']==dept]['NOM'].values[0]
        data_SAA=SAA[dept]
        data_SWI=SWI[dept][SWI[dept].index.isin(annees-offset)]
        if anom:
            for cult in data_SAA:
                data_SAA[cult]=data_SAA[cult]-data_SAA[cult].mean()
            data_SWI=data_SWI-data_SWI.mean()
            SWI_ymin,SWI_ymax=-0.5,0.5
        for cult in data_SAA:
            nom_culture=[c[3:] for c in cultures if cult in c][0]
            axs[i,0].plot(annees,data_SAA[cult],label=nom_culture)
            axs[i,1].scatter(data_SWI[data_SWI.index.isin(annees-offset)],data_SAA[cult],label=nom_culture)
        axs_SWI=axs[i,0].twinx()
        axs_SWI.plot(data_SWI,linestyle=':',label='SWI',color='r')
        axs_SWI.set_ylim(SWI_ymin,SWI_ymax)
        axs_SWI.set_ylabel('SWI',fontweight='bold')
        axs[i,0].set_title(departement_name,fontweight='bold')
        axs[i,1].set_title(departement_name,fontweight='bold')
        axs[i,0].set_ylabel(unit, fontweight='bold')
        axs[i,0].set_xlabel('Années', fontweight='bold')
        axs[i,1].set_ylabel(unit, fontweight='bold')
        axs[i,1].set_xlabel('SWI', fontweight='bold')
        axs[i,0].grid(visible=True)
        axs[i,1].grid(visible=True)
        main_handles, main_labels = axs[i,0].get_legend_handles_labels()
        secondary_handles, secondary_labels = axs_SWI.get_legend_handles_labels()
        handles = main_handles + secondary_handles
        labels = main_labels + secondary_labels#axs[i,0].legend()
        axs[i,0].legend(handles, labels, loc="upper right")
        axs[i,1].legend(loc="upper right")

    axs[0,0].set_title(titre_col1,fontweight='bold')
    axs[0,1].set_title(titre_col2,fontweight='bold')

    plt.savefig(savename)
    print(f'Figure enregistrée sous :\n{os.path.abspath(savename)}')
#    plt.show()

def Plot_scatter_SAA_SWI(SWI,SAA,departements_a_tracer,cultures_a_tracer,months,month_names,offset,anom:bool=False):
    '''
    Description à venir
    '''
    plt.close()
    titre_offset=' de l’année précédente' if offset==1 else ''
    titre=f'Nuage de points des {indicateur_dict['titre'].lower()} en fonction\ndu SWI UNIFORME du mois de {month_names[months[0]]}{titre_offset}\npour les 10 départements de la zone d’étude{'\nANOMALIES' if anom else ''}'
    savename=f'all_depts_scatter{'_ANOM' if anom else ''}_cult_{'-'.join(cultures_a_tracer)}_SWI-month{'-'.join([str(m) for m in months])}_offestN-{offset}.png'
    colors={'11':'blue','24':'orange','13':'green'}
    fig = plt.figure(figsize=(15,15))
    for cult in cultures_a_tracer:
        c=colors[cult]
        for dept in departements_a_tracer:
            data_SAA=SAA[dept][cult]
            data_SWI=SWI[dept][SWI[dept].index.isin(annees-offset)]
            if anom:
                data_SAA=data_SAA-data_SAA.mean()
                data_SWI=data_SWI-data_SWI.mean()
            nom_culture=None
            if dept==departements_a_tracer[0]:
                nom_culture=[c[3:] for c in cultures if cult in c][0]
            plt.scatter(data_SWI[data_SWI.index.isin(annees-offset)],data_SAA,label=nom_culture,color=c)

    plt.xlabel('SWI UNIFORME',fontweight='bold')
    plt.ylabel(indicateur_dict['unit'],fontweight='bold')
    plt.title(titre,fontweight='bold')
    plt.legend()
    plt.grid()
    plt.savefig(savename)
    print(f'Figure enregistrée sous :\n{os.path.abspath(savename)}')
#    plt.show()

def Boxplot_SWI(SWI,SAA,annees,months,culture_a_tracer,offset:int=0,sort_by:str='SAA',figsize=(20,15)):
    '''
    Description à venir
    '''
    df_SWI=pd.DataFrame(index=annees)
    df_SAA=pd.DataFrame(index=annees)
    fail_d=[]
    for d in SWI:
        try:
            df_SWI[d]=SWI[d][SWI[d].index.isin(annees-offset)].values
            df_SAA[d]=SAA[d]['11']
        except:
            fail_d.append(d)
            print(f'Dept fail : {d}')

    for d in fail_d:
        if d in df_SWI.columns:
            df_SWI=df_SWI.drop(columns=d)
        if d in df_SAA.columns:
            df_SAA=df_SAA.drop(columns=fail_d)

    if sort_by=='SWI':
        sorted_columns = df_SWI.mean().sort_values().index
    elif sort_by=='SAA':
        sorted_columns = df_SAA.mean().sort_values().index

    df_SWI_sorted = df_SWI[sorted_columns]
    values_sorted = df_SAA.mean()[sorted_columns]

    departements_names = [f"{metadonnees[metadonnees.loc[:,'INSEE_DEP']==d]['NOM'].values[0]} ({d})" for d in df_SWI_sorted.columns]

    SWI_months_title='moyens annuels' if len(months)==12 else \
                    f'du mois de {month_names[months[0]]}' if len(months)==1 else \
                    f'moyens des mois de {', '.join([month_names[m] for m in months])}'
    offset_title=f' de l’année N-{str(offset)}' if offset!=0 else ''
    SAA_culture_name=[c[3:] for c in cultures if culture_a_tracer in c][0]
    titre=f'Distribution des SWI {SWI_months_title}{offset_title} et rendements moyens annuels de {SAA_culture_name} par département et pour la période 2000-2023'
    titre_wrapped=textwrap.fill(titre,width=70)

    plt.close()
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_title(titre_wrapped,fontsize=18,fontweight='bold',y=1.1)
    bplot = ax.boxplot(df_SWI_sorted,patch_artist=True)
    ax.set_ylabel(f'SWI {SWI_months_title}',fontweight='bold')

    cmap = matplotlib.colormaps['Reds']
    norm = mcolors.Normalize(vmin=values_sorted.min(), vmax=values_sorted.max())

    for patch, col in zip(bplot['boxes'], sorted_columns):
        patch.set_facecolor(cmap(norm(values_sorted[col])))

    wrapped_depts = [textwrap.fill(dept, width=12) for dept in departements_names]
    ax.set_xticklabels(wrapped_depts,rotation=90,fontweight='bold')

    sm = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    orientation='horizontal'
    location='top'
    cbar = plt.colorbar(sm, ax=ax, orientation=orientation, location=location, pad=0.01, aspect=60*figsize[0]/20)
    cbar.ax.text(0.5, 0.5, f"Rendements moyens (q/ha) - {SAA_culture_name}",
             color='#ffffff', fontsize=10, fontweight='bold', ha='center', va='center',
             transform=cbar.ax.transAxes, rotation=0)

    plt.grid()
    plt.tight_layout()
    depts_savename = 'all' if len(df_SWI.columns)==91 else '-'.join(departements_a_tracer)
    months_savename= 'all-year' if len(months)==12 else '-'.join(np.array(months).astype(str))
    offset_savename=f'_N-{str(offset)}' if offset!=0 else ''
    savename=f'SWI_boxplot_month-{months_savename}{offset_savename}_rendements_cult-{culture_a_tracer}_depts-{depts_savename}_sort-{sort_by}.png'
    plt.savefig(savename)
    print(f'Figure enregistrée sous :\n{os.path.abspath(savename)}')
    plt.show()

#EXECUTION

#departements_a_tracer=['02','10','27','28','45','51','60','77','78','89','91','95']
departements_a_tracer=['29','14','62','77','67','21','41','85','24','63','38','64','31','34','83']
#departements_a_tracer=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11',
#       '12', '13', '14', '15', '16', '17', '18', '19', '21', '22',
#       '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33',
#       '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44',
#       '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55',
#       '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66',
#       '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77',
#       '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88',
#       '89', '90', '91', '92', '93', '94', '95']

cultures_a_tracer=['11']    #,'24','13']
indicateur='1' #Rendements
months=[6] #[1,2,3,4,5,6,7,8,9,10,11,12]
offset=0 #1

month_names={1:'janvier',
                 2:'février',
                 3:'mars',
                 4:'avril',
                 5:'mai',
                 6:'juin',
                 7:'juillet',
                 8:'août',
                 9:'septembre',
                 10:'octobre',
                 11:'novembre',
                 12:'décembre',
                 }


SWI,months,depts_SWI,metadonnees=Retrieve_data_SWI(departements_a_tracer,months)
SAA,depts_num_name,cultures,indicateur_dict,annees,depts_SAA,cultures_a_tracer=Retrieve_data_SAA(departements_a_tracer,cultures_a_tracer,indicateur)
#Plot_TS_and_scatter_SAA_SWI(SWI,SAA,cultures_a_tracer,months,month_names,offset,indicateur_dict,metadonnees,depts_SWI,annees,cultures,anom=False)
#Plot_scatter_SAA_SWI(SWI,SAA,departements_a_tracer,cultures_a_tracer,months,month_names,offset,anom=True)
Boxplot_SWI(SWI,SAA,annees,months,cultures_a_tracer[0],offset=offset,figsize=(len(departements_a_tracer)+5,15))