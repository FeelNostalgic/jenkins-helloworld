import http.client
import os
import unittest
from urllib.error import HTTPError
from urllib.request import urlopen

import pytest

BASE_URL = "http://localhost:5000"
BASE_URL_MOCK = "http://localhost:9090"
DEFAULT_TIMEOUT = 2  # in secs

@pytest.mark.api
class TestApi(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def test_api_add(self):
        url = f"{BASE_URL}/calc/add/1/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "3", "ERROR ADD"
        )

    def test_api_substract(self):
        url = f"{BASE_URL}/calc/substract/10/6"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "4", "ERROR ADD"
        )

    def test_api_sqrt(self):
        url = f"{BASE_URL_MOCK}/calc/sqrt/64"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "8", "ERROR SQRT"
        )

    def test_api_multiply(self):
        url = f"{BASE_URL}/calc/multiply/2/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "4", "ERROR MULTIPLY"
        )

    def test_api_divide(self):
        url = f"{BASE_URL}/calc/divide/2/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "1.0", "ERROR DIVIDE"
        )

    def test_divide_by_zero(self):
        url = f"{BASE_URL}/calc/divide/2/0"
        try:
            urlopen(url, timeout=DEFAULT_TIMEOUT)
            self.fail(
                f"La API en {url} devolvió 200 OK, pero se esperaba {http.client.NOT_ACCEPTABLE}."
            )
        except HTTPError as e:
            self.assertEqual(
                e.code,
                http.client.NOT_ACCEPTABLE,
                f"ERROR: Código de estado incorrecto. Esperado: {http.client.NOT_ACCEPTABLE} ({http.client.NOT_ACCEPTABLE.name}), Recibido: {e.code}"
            )

            error_message = e.read().decode().strip()
            self.assertEqual(
                error_message,
                "ERROR: Division by zero",
                "El mensaje de error devuelto no coincide con el esperado."
            )

        except Exception as e:
            self.fail(f"Fallo de conexión o excepción inesperada: {e}")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
