import os
import secrets

from flask import (Flask, abort, flash, redirect, render_template,
                   jsonify, request, session, url_for)

app = Flask(__name__)
# Clé secrète : nécessaire pour flash et session (mission 6).
# En vrai projet, on la lit dans une variable d'environnement.
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex()

PRIORITES = ("basse", "normale", "haute")
FILTRES = ("toutes", "actives", "terminees")

taches = [
    {"id": 1, "titre": "<b>Essai</b>",
     "priorite": "haute", "terminee": False},
    {"id": 2, "titre": "Installer Flask",
     "priorite": "normale", "terminee": True},
    {"id": 3, "titre": "Lire la doc Jinja2",
     "priorite": "basse", "terminee": False},
]


@app.route("/")
def index():
    # Mission 6 : le filtre vient de l'URL, sinon de la session, sinon "toutes"
    filtre = request.args.get("filtre") or session.get("filtre", "toutes")
    if filtre not in FILTRES:
        filtre = "toutes"
    session["filtre"] = filtre

    if filtre == "actives":
        visibles = [t for t in taches if not t["terminee"]]
    elif filtre == "terminees":
        visibles = [t for t in taches if t["terminee"]]
    else:
        visibles = taches

    restantes = sum(1 for t in taches if not t["terminee"])
    return render_template("taches.html", taches=visibles, filtre=filtre,
                           restantes=restantes)


@app.route("/taches/<int:id>")  # Mission 2 : convertisseur int
def tache(id):
    for t in taches:
        if t["id"] == id:
            return render_template("tache.html", tache=t)
    abort(404)  # vraie erreur 404, pas une page "introuvable" en 200


@app.route("/taches/ajouter", methods=["GET", "POST"])
def ajouter():
    erreur = None
    titre = ""
    priorite = "normale"
    if request.method == "POST":
        titre = request.form.get("titre", "").strip()
        priorite = request.form.get("priorite", "normale")

        # Validation côté serveur
        if not titre:
            erreur = "Le titre est obligatoire."
        elif len(titre) > 80:
            erreur = "Le titre ne doit pas dépasser 80 caractères."
        elif priorite not in PRIORITES:
            erreur = "Priorité invalide."

        if erreur is None:
            nouvel_id = max((t["id"] for t in taches), default=0) + 1
            taches.append({"id": nouvel_id, "titre": titre,
                           "priorite": priorite, "terminee": False})
            flash("Tâche ajoutée")
            # Redirection après POST : F5 ne recrée pas de doublon
            return redirect(url_for("index"))

    return render_template("ajouter.html", erreur=erreur, titre=titre,
                           priorite=priorite, priorites=PRIORITES)


@app.post("/taches/<int:id>/basculer")
def basculer_tache(id):
    tache_a_modifier = next((t for t in taches if t["id"] == id), None)
    if tache_a_modifier is None:
        abort(404)

    tache_a_modifier["terminee"] = not tache_a_modifier["terminee"]
    flash("Tâche marquée comme terminée." if tache_a_modifier["terminee"]
          else "Tâche réactivée.")
    return redirect(url_for("index"))


@app.post("/taches/<int:id>/supprimer")
def supprimer_tache(id):
    index_tache = next((i for i, t in enumerate(taches) if t["id"] == id), None)
    if index_tache is None:
        abort(404)

    taches.pop(index_tache)
    flash("Tâche supprimée.")
    return redirect(url_for("index"))


@app.get("/api/taches")
def api_taches():
    return jsonify(taches)


@app.errorhandler(404)
def page_introuvable(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run()
