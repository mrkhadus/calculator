import importlib.util
import pathlib
import unittest


APP_PATH = pathlib.Path(__file__).parents[2] / "backend" / "app.py"


def load_app():
    spec = importlib.util.spec_from_file_location("calculator_backend_app", APP_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.app


class BackendAppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = load_app()
        cls.client = cls.app.test_client()

    def test_health_returns_ok(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_supported_operations(self):
        cases = (
            ("add", 15),
            ("subtract", 5),
            ("multiply", 50),
            ("divide", 2),
        )

        for operation, expected in cases:
            with self.subTest(operation=operation):
                response = self.client.post(
                    "/calculate",
                    json={"num1": 10, "num2": 5, "operation": operation},
                )

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.get_json(), {"result": expected})

    def test_calculate_accepts_numeric_strings(self):
        response = self.client.post(
            "/calculate",
            json={"num1": "1.5", "num2": "2.25", "operation": "add"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"result": 3.75})

    def test_calculate_rejects_missing_or_invalid_input(self):
        cases = (
            {},
            {"num1": 1, "num2": 2},
            {"num1": "not-a-number", "num2": 2, "operation": "add"},
        )

        for payload in cases:
            with self.subTest(payload=payload):
                response = self.client.post("/calculate", json=payload)

                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    response.get_json(),
                    {"error": "num1, num2 and a valid operation are required"},
                )

    def test_calculate_rejects_unsupported_operation(self):
        response = self.client.post(
            "/calculate",
            json={"num1": 1, "num2": 2, "operation": "power"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Unsupported operation"})

    def test_calculate_rejects_division_by_zero(self):
        response = self.client.post(
            "/calculate",
            json={"num1": 10, "num2": 0, "operation": "divide"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Cannot divide by zero"})


if __name__ == "__main__":
    unittest.main()