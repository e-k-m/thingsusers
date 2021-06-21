import unittest

import flask

import common

url_for = flask.url_for
HEADERS = {"content-type": "application/json"}


class TestUsers(common.TestFixure):
    def test_register(self):
        payload = {
            "email": "bob@bob.com",
            "username": "bob",
            "password": "bob",
        }
        resp = self.client.post(
            url_for("users.register_user"), json=payload, headers=HEADERS
        )
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.json["id"])
        self.assertEqual(resp.json["username"], payload["username"])
        self.assertEqual(resp.json["email"], payload["email"])
        self.assertTrue(resp.json["accessToken"])
        self.assertTrue(resp.json["refreshToken"])
        self.assertTrue("password" not in resp.json)

    def test_register_bad_payload(self):
        payload = {
            "email": "bob@bob.com",
            "username": "bob",
        }
        resp = self.client.post(
            url_for("users.register_user"), json=payload, headers=HEADERS
        )
        self.assertEqual(resp.status_code, 400)

        payload = {
            "email": "bobbob.com",
            "username": "bob",
            "password": "bob",
        }
        resp = self.client.post(
            url_for("users.register_user"), json=payload, headers=HEADERS
        )
        self.assertEqual(resp.status_code, 400)

    def test_register_twice(self):
        payload = {
            "email": "bob@bob.com",
            "username": "bob",
            "password": "bob",
        }
        resp = self.client.post(
            url_for("users.register_user"), json=payload, headers=HEADERS
        )
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.json["id"])
        self.assertEqual(resp.json["username"], payload["username"])
        self.assertEqual(resp.json["email"], payload["email"])
        self.assertTrue(resp.json["accessToken"])
        self.assertTrue(resp.json["refreshToken"])
        self.assertTrue("password" not in resp.json)

        payload = {
            "email": "bob@bob.com",
            "username": "bob",
            "password": "bob",
        }
        resp = self.client.post(
            url_for("users.register_user"), json=payload, headers=HEADERS
        )
        self.assertEqual(resp.status_code, 400)

    def test_login(self):
        payload = {
            "email": self.should_user.email,
            "password": common.PASSWORD,
        }

        resp = self.client.post(
            url_for("users.login_user"), json=payload, headers=HEADERS
        )
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.json["id"])
        self.assertEqual(resp.json["username"], self.should_user.username)
        self.assertEqual(resp.json["email"], self.should_user.email)
        self.assertTrue(resp.json["accessToken"])
        self.assertTrue(resp.json["refreshToken"])
        self.assertTrue("password" not in resp.json)

        payload = {
            "username": self.should_user.username,
            "password": common.PASSWORD,
        }

        resp = self.client.post(
            url_for("users.login_user"), json=payload, headers=HEADERS
        )
        self.assertEqual(resp.status_code, 201)

    def test_login_bad_payload(self):
        payload = {
            "password": common.PASSWORD,
        }

        resp = self.client.post(
            url_for("users.login_user"), json=payload, headers=HEADERS
        )
        self.assertEqual(resp.status_code, 400)

    def test_info(self):
        payload = {
            "email": self.should_user.email,
            "password": common.PASSWORD,
        }

        resp = self.client.post(
            url_for("users.login_user"), json=payload, headers=HEADERS
        )
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.json["accessToken"])

        token = resp.json["accessToken"]

        resp = self.client.get(
            url_for("users.info_user"),
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json["id"])
        self.assertEqual(resp.json["username"], self.should_user.username)
        self.assertEqual(resp.json["email"], self.should_user.email)
        self.assertTrue("password" not in resp.json)
        self.assertTrue("accessToken" not in resp.json)
        self.assertTrue("refreshToken" not in resp.json)

    def test_info_bad_payload(self):
        resp = self.client.get(url_for("users.info_user"))
        self.assertEqual(resp.status_code, 401)
        self.assertTrue("error" in resp.json and "code" in resp.json["error"])

        resp = self.client.get(
            url_for("users.info_user"),
            headers={"Authorization": "Bearer junk"},
        )
        self.assertEqual(resp.status_code, 422)
        self.assertTrue("error" in resp.json and "code" in resp.json["error"])

    def test_refresh(self):
        payload = {
            "email": self.should_user.email,
            "password": common.PASSWORD,
        }

        resp = self.client.post(
            url_for("users.login_user"), json=payload, headers=HEADERS
        )
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.json["refreshToken"])

        token = resp.json["refreshToken"]
        resp = self.client.get(
            url_for("users.refresh_user"),
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.json["id"])
        self.assertEqual(resp.json["username"], self.should_user.username)
        self.assertEqual(resp.json["email"], self.should_user.email)
        self.assertTrue(resp.json["accessToken"])
        self.assertTrue("password" not in resp.json)
        self.assertTrue("refreshToken" not in resp.json)

    def test_refresh_bad_payload(self):
        payload = {
            "email": self.should_user.email,
            "password": common.PASSWORD,
        }

        resp = self.client.post(
            url_for("users.login_user"), json=payload, headers=HEADERS
        )
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.json["refreshToken"])

        token = resp.json["accessToken"]
        resp = self.client.get(
            url_for("users.refresh_user"),
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(resp.status_code, 422)

        resp = self.client.get(url_for("users.refresh_user"),)
        self.assertEqual(resp.status_code, 401)
        self.assertTrue("error" in resp.json and "code" in resp.json["error"])

    def test_update(self):
        payload = {
            "email": self.should_user.email,
            "password": common.PASSWORD,
        }

        resp = self.client.post(
            url_for("users.login_user"), json=payload, headers=HEADERS
        )

        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.json["accessToken"])
        self.assertTrue(resp.json["id"])
        self.assertTrue(resp.json["username"])

        id_ = resp.json["id"]
        token = resp.json["accessToken"]
        username = resp.json["username"]
        payload = {
            "username": username,
            "email": "yal@yal.com",
            "password": "hacker",
        }

        resp = self.client.put(
            url_for("users.update_user", id_=id_),
            json=payload,
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.json["id"])
        self.assertEqual(resp.json["email"], payload["email"])
        self.assertEqual(resp.json["username"], payload["username"])
        self.assertTrue("password" not in resp.json)
        self.assertTrue("accessToken" not in resp.json)
        self.assertTrue("refreshToken" not in resp.json)

    def test_update_bad_payload(self):
        payload = {
            "email": self.should_user.email,
            "password": common.PASSWORD,
        }

        resp = self.client.post(
            url_for("users.login_user"), json=payload, headers=HEADERS
        )

        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.json["accessToken"])
        self.assertTrue(resp.json["id"])
        self.assertTrue(resp.json["username"])

        id_ = resp.json["id"]
        token = resp.json["accessToken"]
        payload = {"email": "yal@yal.com"}

        resp = self.client.put(
            url_for("users.update_user", id_=id_),
            json=payload,
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(resp.status_code, 400)

        resp = self.client.put(
            url_for("users.update_user", id_=id_), json=payload,
        )

        self.assertEqual(resp.status_code, 401)
        self.assertTrue("error" in resp.json and "code" in resp.json["error"])

    def test_delete(self):
        payload = {
            "email": self.should_user.email,
            "password": common.PASSWORD,
        }

        resp = self.client.post(
            url_for("users.login_user"), json=payload, headers=HEADERS
        )
        self.assertEqual(resp.status_code, 201)

        token = resp.json["accessToken"]

        resp = self.client.delete(
            url_for("users.delete_user", id_=self.should_user.id),
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(resp.data)

        payload = {
            "email": self.should_user.email,
            "password": common.PASSWORD,
        }

        resp = self.client.post(
            url_for("users.login_user"), json=payload, headers=HEADERS
        )
        self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
