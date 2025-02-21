import shutil
from pathlib import Path

def reinitialiser_dossier(nom_dossier: Path):
    if nom_dossier.exists():
        for contenu in nom_dossier.iterdir():
            if contenu.is_file():
                contenu.unlink()
            elif contenu.is_dir():
                shutil.rmtree(contenu)
    else:
        nom_dossier.mkdir(parents=True)