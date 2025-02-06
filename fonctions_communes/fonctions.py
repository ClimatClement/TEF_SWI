def sel_options(options,options_name:str='département'):
    '''
    Cette fonction permet de demander à l’utilisateur de sélectionner une ou plusieur options.

    INPUT
    options (list) La liste des options disponibles
    options_name (str) La dénomination du paramètre à sélectionner pour compléter le texte affiché à l’écran pour l’utilisateur

    OUTPUT
    user_choice (list) la liste des numéros entrés par l’utilisateur (dtype str)
    '''
    #D’abord j’affiche la liste des options
    print()
    print('**LISTE DES OPTIONS**')
    for opts in options:
        print(opts)
    print()

    #Ensuite je demande à l’utilisateur d’entrer les numéros de régions de son choix (un ou plusieurs)
    user_choice=[]
    while user_choice==[]: #Tant qu’on n’a pas de réponse valide
        user_choice = input(f"Choix des {options_name} à tracer.\nEntrez les numéros de {options_name} séparées par des virgules (e.g. 02,05,06)\n(q pour quitter)\n\n>>>>",)

        if user_choice=='q': #Fin d’exécution
            return('Programme interrompu par l’utilisateur')
        
        #Transformation de l’entrée utilisateur en liste
        user_choice=[ele for ele in user_choice.split(',') if ele!='']

        #Vérification que toutes les entrées de l’utilisateur sont bien des numéros
        try:
            test=[int(i) for i in user_choice]
        #Message d’erreur et réinitialisation de la liste de régions
        except:
            print(f'Saisie incorrecte :\n{user_choice}\nVous devez entrer un ou plusieurs numéros séparés par des virgules.\n')
            user_choice=[]

    return(user_choice)

def sel_indicateur (indicateur:str='0'):
    '''
    Cette fonction permet de demander à l’utilisateur de sélectionner un indicateur parmis : rendements, production, et surfaces
    
    INPUT
    indicateur (str)(optionnel: defaut = '0') '1' rendements, '2' production, '3' surface

    OUTPUT
    indicateur (str)
    '''
    while indicateur not in ['1','2','3']:
        print()
        indicateur=input('Quel indicateur voulez-vous tracer ?\n1 RENDEMENTS (q/ha)\n2 PRODUCTION (q)\n3 SURFACES (ha)\n>>>>')
    return(indicateur)