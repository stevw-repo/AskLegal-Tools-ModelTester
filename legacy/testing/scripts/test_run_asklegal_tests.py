import base64
import importlib.util
import json
import os
import pathlib
import ssl
import unittest
from unittest import mock


SCRIPT_PATH = pathlib.Path(__file__).with_name("run_asklegal_tests.py")


def load_runner_module():
    spec = importlib.util.spec_from_file_location("run_asklegal_tests", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RunnerTests(unittest.TestCase):
    def test_load_suite_rejects_extra_metadata_fields(self):
        runner = load_runner_module()
        suite_path = pathlib.Path(__file__).with_name("_tmp_suite.json")
        suite_path.write_text(
            json.dumps([{"id": "sg-001", "query": "I need help.", "area": "contract"}]),
            encoding="utf-8",
        )
        try:
            with self.assertRaisesRegex(ValueError, "exactly 'id' and 'query'"):
                runner.load_suite(suite_path)
        finally:
            suite_path.unlink(missing_ok=True)

    def test_assemble_stream_response_decodes_base64_ndjson_chunks(self):
        runner = load_runner_module()
        chunks = [
            {"conversationId": "abc-123", "content": "Hello"},
            {"conversationId": "abc-123", "content": " world"},
            {"conversationId": "abc-123", "content": ""},
        ]
        raw = "\n".join(json.dumps(chunk) for chunk in chunks).encode("utf-8")
        encoded = base64.b64encode(raw)

        result = runner.assemble_stream_response(encoded)

        self.assertEqual(result.conversation_id, "abc-123")
        self.assertEqual(result.content, "Hello world")

    def test_build_ssl_context_verifies_certificates_by_default(self):
        runner = load_runner_module()

        context = runner.build_ssl_context(ca_bundle=None, insecure=False)

        self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(context.check_hostname)

    def test_build_ssl_context_disables_verification_only_when_requested(self):
        runner = load_runner_module()

        context = runner.build_ssl_context(ca_bundle=None, insecure=True)

        self.assertEqual(context.verify_mode, ssl.CERT_NONE)
        self.assertFalse(context.check_hostname)

    def test_build_ssl_context_uses_custom_ca_bundle(self):
        runner = load_runner_module()
        ca_bundle = pathlib.Path("company-ca.pem")
        sentinel = object()

        with mock.patch.object(runner.ssl, "create_default_context", return_value=sentinel) as create_context:
            context = runner.build_ssl_context(ca_bundle=ca_bundle, insecure=False)

        self.assertIs(context, sentinel)
        create_context.assert_called_once_with(cafile=str(ca_bundle))

    def test_parse_args_exposes_mutually_exclusive_tls_options(self):
        runner = load_runner_module()

        insecure_args = runner.parse_args(["--prompt-version", "sg-prompt-v1.0-a", "--insecure"])
        ca_args = runner.parse_args(
            ["--prompt-version", "sg-prompt-v1.0-a", "--ca-bundle", "company-ca.pem"]
        )

        self.assertTrue(insecure_args.insecure)
        self.assertIsNone(insecure_args.ca_bundle)
        self.assertFalse(ca_args.insecure)
        self.assertEqual(ca_args.ca_bundle, pathlib.Path("company-ca.pem"))

        with self.assertRaises(SystemExit):
            runner.parse_args(
                [
                    "--prompt-version",
                    "sg-prompt-v1.0-a",
                    "--insecure",
                    "--ca-bundle",
                    "company-ca.pem",
                ]
            )

    def test_load_api_key_prefers_cli_then_env_then_file(self):
        runner = load_runner_module()
        key_path = pathlib.Path(__file__).with_name("_tmp_api_key.txt")
        key_path.write_text("ASKLEGAL_API_KEY=file-key\n", encoding="utf-8")
        try:
            with mock.patch.dict(os.environ, {"ASKLEGAL_API_KEY": "env-key"}):
                self.assertEqual(runner.load_api_key("cli-key", key_path), "cli-key")
                self.assertEqual(runner.load_api_key(None, key_path), "env-key")
            with mock.patch.dict(os.environ, {}, clear=True):
                self.assertEqual(runner.load_api_key(None, key_path), "file-key")
        finally:
            key_path.unlink(missing_ok=True)

    def test_auth_headers_include_bearer_and_api_key_forms(self):
        runner = load_runner_module()

        headers = runner.auth_headers("secret-key")

        self.assertEqual(headers["Authorization"], "Bearer secret-key")
        self.assertEqual(headers["X-API-Key"], "secret-key")
        self.assertEqual(headers["x-access-token"], "secret-key")

    def test_run_suite_parallel_preserves_suite_order(self):
        runner = load_runner_module()
        suite = [
            {"id": "sg-001", "query": "First"},
            {"id": "sg-002", "query": "Second"},
            {"id": "sg-003", "query": "Third"},
        ]

        def fake_execute(item, *_args):
            return runner.QueryResult(item["id"], item["query"], item["id"], item["query"], "")

        with mock.patch.object(runner, "execute_query", side_effect=fake_execute):
            results = runner.run_suite(
                suite,
                "https://dev.ask.legal",
                "singapore",
                180,
                mock.Mock(),
                "key",
                0,
                3,
            )

        self.assertEqual([result.id for result in results], ["sg-001", "sg-002", "sg-003"])

    def test_parse_args_accepts_parallel_worker_count(self):
        runner = load_runner_module()

        args = runner.parse_args(["--prompt-version", "sg-prompt-v1.0-b", "--parallel", "4"])

        self.assertEqual(args.parallel, 4)

    def test_parse_args_defaults_to_parallel_execution(self):
        runner = load_runner_module()

        args = runner.parse_args(["--prompt-version", "sg-prompt-v1.0-b"])

        self.assertEqual(args.parallel, 4)


if __name__ == "__main__":
    unittest.main()
