import unittest

from app import app, taches


class TaskAppTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        taches[:] = [
            {"id": 1, "titre": "Réviser les décorateurs",
             "priorite": "haute", "terminee": False},
            {"id": 2, "titre": "Installer Flask",
             "priorite": "normale", "terminee": True},
            {"id": 3, "titre": "Lire la doc Jinja2",
             "priorite": "basse", "terminee": False},
        ]
        self.client = app.test_client()

    def test_list_filters_and_session(self):
        response = self.client.get("/?filtre=actives")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Réviser les décorateurs".encode(), response.data)
        self.assertNotIn("Installer Flask".encode(), response.data)

        response = self.client.get("/")
        self.assertIn("Lire la doc Jinja2".encode(), response.data)
        self.assertNotIn("Installer Flask".encode(), response.data)

        response = self.client.get("/?filtre=invalide")
        self.assertIn("Installer Flask".encode(), response.data)

    def test_detail_and_not_found(self):
        response = self.client.get("/taches/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Réviser les décorateurs".encode(), response.data)
        self.assertEqual(self.client.get("/taches/999").status_code, 404)

    def test_task_title_html_is_escaped(self):
        taches[0]["titre"] = "<b>Essai</b>"

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"&lt;b&gt;Essai&lt;/b&gt;", response.data)
        self.assertNotIn(b"<b>Essai</b>", response.data)

    def test_add_validation_redirect_and_flash(self):
        response = self.client.post(
            "/taches/ajouter",
            data={"titre": "  Nouvelle tâche  ", "priorite": "haute"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/")
        self.assertEqual(taches[-1]["titre"], "Nouvelle tâche")

        response = self.client.get("/")
        self.assertIn("Tâche ajoutée".encode(), response.data)
        self.assertNotIn("Tâche ajoutée".encode(), self.client.get("/").data)

        response = self.client.post(
            "/taches/ajouter", data={"titre": " ", "priorite": "normale"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Le titre est obligatoire.".encode(), response.data)
        self.assertEqual(len(taches), 4)

        response = self.client.post(
            "/taches/ajouter",
            data={"titre": "x" * 81, "priorite": "normale"},
        )
        self.assertIn("80 caractères".encode(), response.data)
        self.assertEqual(len(taches), 4)

        response = self.client.post(
            "/taches/ajouter",
            data={"titre": "Priorité invalide", "priorite": "urgente"},
        )
        self.assertIn("Priorité invalide.".encode(), response.data)
        self.assertEqual(len(taches), 4)

    def test_toggle_delete_and_api(self):
        response = self.client.post("/taches/1/basculer")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(taches[0]["terminee"])

        response = self.client.get("/api/taches")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, taches)

        response = self.client.post("/taches/1/supprimer")
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(1, [tache["id"] for tache in taches])
        self.assertEqual(self.client.post("/taches/999/basculer").status_code, 404)
        self.assertEqual(self.client.post("/taches/999/supprimer").status_code, 404)


if __name__ == "__main__":
    unittest.main()
