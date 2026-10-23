# TP Flask — gestion de tâches

Application pédagogique Flask : liste, détails, filtres, ajout et validation
de tâches, messages flash, session, actions terminer/supprimer et API JSON.

## Prérequis

- Python 3.11 ou plus récent
- Git

Les commandes suivantes sont prévues pour un terminal Linux/macOS, depuis le
dossier du projet.

## Installation

À faire une seule fois :

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip show Flask
```

Après activation, le préfixe `(.venv)` doit apparaître dans l’invite du
terminal. Si `python3` n’existe pas, essayez `python` à la place.

Dans PowerShell sous Windows, activez l’environnement avec :

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Lancer l’application

Depuis la racine du projet et avec `.venv` activé :

```bash
python -m flask --app app run --debug
```

Ouvrez ensuite <http://127.0.0.1:5000/>.

`--debug` active le rechargement automatique et les erreurs détaillées :
réservez-le au développement, jamais à un déploiement en production.
Arrêtez le serveur avec `Ctrl+C`.

### Si le port 5000 est déjà utilisé

Il peut rester une ancienne instance du serveur. Si c’est votre terminal qui
l’exécute, arrêtez-la avec `Ctrl+C`. Sinon, lancez ce projet sur un autre port :

```bash
python -m flask --app app run --debug --port 5001
```

Ouvrez alors <http://127.0.0.1:5001/>. Ne terminez pas un processus inconnu :
utilisez le port alternatif ou identifiez d’abord le programme concerné.

La commande doit inclure `run` et le nom du module, `--app app`. Par exemple,
`flask --app run --debug` est incorrect : Flask ne reçoit pas la commande
`run` à la bonne position.

## Vérifier le projet

Depuis la racine du dépôt, avec l’environnement activé :

```bash
python -m unittest discover -v
```

## Routes disponibles

- `/` : liste des tâches et filtres `toutes`, `actives`, `terminees`
- `/taches/<id>` : détail d’une tâche
- `/taches/ajouter` : formulaire d’ajout
- `/taches/<id>/basculer` : terminer ou réactiver une tâche (POST)
- `/taches/<id>/supprimer` : supprimer une tâche (POST)
- `/api/taches` : liste des tâches au format JSON

Les tâches sont conservées en mémoire : elles sont réinitialisées au
redémarrage du serveur. Le journal de découverte [JOURNAL.md](./JOURNAL.md)
est à compléter à partir de vos propres essais.
