import importlib.util
import pathlib
import sys
import types
import unittest
from unittest.mock import Mock, patch


APP_PATH = pathlib.Path(__file__).parents[2] / "frontend" / "app.py"


if "requests" not in sys.modules:
    sys.modules["requests"] = types.ModuleType("requests")
    sys.modules["requests"].post = Mock()
    sys.modules["requests"].RequestException = RuntimeError


def load_app():
    if "requests" not in sys.modules:
        sys.modules["requests"] = types.ModuleType("requests")
        sys.modules["requests"].post = Mock()

    spec = importlib.util.spec_from_file_location("calculator_frontend_app", APP_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.app.template_folder = str(APP_PATH.parent / "templates")
    return module


class FrontendAppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_app()
        cls.client = cls.module.app.test_client()

    def test_index_renders_calculator_page(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Flask Calculator</title>", response.data)
        self.assertIn(b'id="operation"', response.data)

    @patch.object(sys.modules["requests"], "post")
    def test_calculate_proxies_payload_and_status(self, post):
        backend_response = Mock()
        backend_response.status_code = 200
        backend_response.json.return_value = {"result": 15}
        post.return_value = backend_response

        response = self.client.post(
            "/api/calculate",
            json={"num1": 10, "num2": 5, "operation": "add"},
        )

        post.assert_called_once_with(
            "http://backend-service:5001/calculate",
            json={"num1": 10, "num2": 5, "operation": "add"},
            timeout=5,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"result": 15})

    @patch.object(sys.modules["requests"], "post")
    def test_calculate_preserves_backend_error_status(self, post):
        backend_response = Mock()
        backend_response.status_code = 400
        backend_response.json.return_value = {"error": "Cannot divide by zero"}
        post.return_value = backend_response

        response = self.client.post("/api/calculate", json={"operation": "divide"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Cannot divide by zero"})

    @patch.object(sys.modules["requests"], "post")
    def test_calculate_returns_error_when_backend_request_fails(self, post):
        post.side_effect = self.module.requests.RequestException("backend unavailable")

        response = self.client.post("/api/calculate", json={"operation": "add"})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json(), {"error": "backend unavailable"})


if __name__ == "__main__":
    unittest.main()