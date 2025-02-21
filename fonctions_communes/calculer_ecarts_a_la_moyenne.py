import pandas
from pandas import DataFrame


def calculer_ecarts_a_la_moyenne(df: DataFrame, on: [str], colonne: str, colonne_ponderation: str = None) -> DataFrame:
    moyennes = calculer_moyennes(df, on, colonne, colonne_ponderation)

    df = pandas.merge(df, moyennes, on=on, suffixes=('', '_MOYEN'))

    df[f'{colonne}_ECART_ABSOLU'] = df[colonne] - df[f'{colonne}_MOYEN']
    df[f'{colonne}_ECART_RELATIF'] = (100 * df[f'{colonne}_ECART_ABSOLU'] / df[f'{colonne}_MOYEN']).round(2)

    return df


def calculer_moyennes(df: DataFrame, on: [str], colonne: str, colonne_ponderation: str = None) -> DataFrame:
    if colonne_ponderation != None:
        return (
            (df.assign(produit=df[colonne] * df[colonne_ponderation]).groupby(on)['produit'].sum() /
             df.groupby(on)[colonne_ponderation].sum()
             ).
            round(2).
            rename(colonne).
            reset_index()
        )
    else :
        return (
            df.
            groupby(on)[[colonne]].
            mean().
            round(2).
            reset_index()
        )
