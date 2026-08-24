import importlib.util
import io
import json
import pathlib
import sys
import tempfile
import unittest
from unittest import mock


SCRIPT_PATH = pathlib.Path(__file__).parents[1] / "tools" / "inspect_azure_env.py"


def load_module():
    spec = importlib.util.spec_from_file_location("inspect_azure_env", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class InspectAzureEnvTests(unittest.TestCase):
    def test_loads_dotenv_names_without_values(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "settings.env"
            path.write_text(
                "MODEL_NAME=gpt-model\nASKLEGAL_API_KEY=never-print-this\n",
                encoding="utf-8",
            )

            names = module.load_names(path)

        self.assertEqual(names, ["ASKLEGAL_API_KEY", "MODEL_NAME"])
        self.assertNotIn("never-print-this", repr(names))

    def test_loads_azure_json_array_names(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "settings.json"
            path.write_text(
                json.dumps(
                    [
                        {"name": "PINECONE_INDEX", "value": "HK-v7", "slotSetting": False},
                        {"name": "ANSWER_MODEL", "value": "model", "slotSetting": False},
                    ]
                ),
                encoding="utf-8",
            )

            names = module.load_names(path)

        self.assertEqual(names, ["ANSWER_MODEL", "PINECONE_INDEX"])

    def test_classifies_likely_secret_names(self):
        module = load_module()

        self.assertTrue(module.is_likely_secret("AZURE_OPENAI_API_KEY"))
        self.assertTrue(module.is_likely_secret("AZURE_OPENAI_KEY"))
        self.assertTrue(module.is_likely_secret("DATABASE_CONNECTION_STRING"))
        self.assertTrue(module.is_likely_secret("DATABASE_URL"))
        self.assertFalse(module.is_likely_secret("ANSWER_MODEL"))
        self.assertFalse(module.is_likely_secret("MAX_COMPLETION_TOKENS"))
        self.assertFalse(module.is_likely_secret("MAX_TOKEN_BUDGET"))
        self.assertFalse(module.is_likely_secret("PINECONE_INDEX"))

    def test_main_never_prints_values(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "settings.env"
            path.write_text(
                "PINECONE_INDEX=HK-v7\nAPI_KEY=super-secret-value\n",
                encoding="utf-8",
            )
            output = io.StringIO()

            with mock.patch("sys.stdout", output):
                result = module.main([str(path)])

        self.assertEqual(result, 0)
        self.assertIn("PINECONE_INDEX", output.getvalue())
        self.assertIn("API_KEY", output.getvalue())
        self.assertNotIn("HK-v7", output.getvalue())
        self.assertNotIn("super-secret-value", output.getvalue())


if __name__ == "__main__":
    unittest.main()
