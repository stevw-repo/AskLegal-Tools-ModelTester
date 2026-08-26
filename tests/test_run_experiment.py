import base64
import io
import importlib.util
import json
import os
import pathlib
import ssl
import sys
import tempfile
import unittest
from http import client as http_client
from unittest import mock


SCRIPT_PATH = pathlib.Path(__file__).parents[1] / "tools" / "run_experiment.py"


def load_runner_module():
    spec = importlib.util.spec_from_file_location("run_experiment", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class RunnerTests(unittest.TestCase):
    def test_load_experiment_accepts_two_configured_arms(self):
        runner = load_runner_module()
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "experiment.yaml"
            path.write_text(
                """
format_version: 1
name: hk-v7-v8
jurisdiction: hong-kong
api:
  base_url: https://api-dev.ask.legal
  jurisdiction: hongkong
suite: suites/hong-kong/general-v1/questions.json
rubric: rubrics/legal-analysis-v1.md
arms:
  arm-a:
    label: HK-v7
    configuration:
      index: HK-v7
  arm-b:
    label: HK-v8
    configuration:
      index: HK-v8
""".lstrip(),
                encoding="utf-8",
            )

            experiment = runner.load_experiment(path)

        self.assertEqual(experiment["arms"]["arm-a"]["configuration"]["index"], "HK-v7")

    def test_load_experiment_requires_two_arms(self):
        runner = load_runner_module()
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "experiment.yaml"
            path.write_text(
                """
format_version: 1
name: one-arm
jurisdiction: hong-kong
api:
  base_url: https://api-dev.ask.legal
  jurisdiction: hongkong
suite: suite.json
rubric: rubric.md
arms:
  arm-a:
    label: A
    configuration:
      index: HK-v7
""".lstrip(),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "at least two arms"):
                runner.load_experiment(path)

    def test_load_experiment_rejects_unknown_api_fields(self):
        runner = load_runner_module()
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "experiment.yaml"
            path.write_text(
                """
format_version: 1
name: comparison
jurisdiction: hong-kong
api:
  base_url: https://api-dev.ask.legal
  jurisdiction: hongkong
  api_key: do-not-store-this
suite: suite.json
rubric: rubric.md
arms:
  arm-a:
    label: A
    configuration:
      model: gpt-5.4
  arm-b:
    label: B
    configuration:
      model: gpt-5.6-terra
""".lstrip(),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "api has unsupported fields"):
                runner.load_experiment(path)

    def test_load_experiment_rejects_secret_configuration_fields(self):
        runner = load_runner_module()
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "experiment.yaml"
            path.write_text(
                """
format_version: 1
name: comparison
jurisdiction: hong-kong
api:
  base_url: https://api-dev.ask.legal
  jurisdiction: hongkong
suite: suite.json
rubric: rubric.md
arms:
  arm-a:
    label: A
    configuration:
      model: gpt-5.4
      azure_openai_key: do-not-store-this
  arm-b:
    label: B
    configuration:
      model: gpt-5.6-terra
""".lstrip(),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "prohibited secret field"):
                runner.load_experiment(path)

    def test_load_questions_rejects_extra_fields(self):
        runner = load_runner_module()
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "questions.json"
            path.write_text(
                json.dumps([{"id": "hk-001", "query": "Help.", "area": "contract"}]),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "exactly 'id' and 'query'"):
                runner.load_questions(path)

    def test_load_expectations_supports_optional_gold_answer(self):
        runner = load_runner_module()
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "expectations.json"
            path.write_text(
                json.dumps(
                    [
                        {
                            "id": "hk-001",
                            "must_cover": ["Limitation"],
                            "gold_answer": None,
                        }
                    ]
                ),
                encoding="utf-8",
            )

            loaded = runner.load_expectations(path, {"hk-001"})

        self.assertEqual(loaded[0]["must_cover"], ["Limitation"])

    def test_load_expectations_rejects_unknown_question_id(self):
        runner = load_runner_module()
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "expectations.json"
            path.write_text(json.dumps([{"id": "hk-999"}]), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "does not match"):
                runner.load_expectations(path, {"hk-001"})

    def test_assemble_stream_response_decodes_base64_ndjson(self):
        runner = load_runner_module()
        chunks = [
            {"conversationId": "abc", "content": "Hello"},
            {"conversationId": "abc", "content": " world"},
        ]
        raw = "\n".join(json.dumps(chunk) for chunk in chunks).encode()

        conversation_id, content = runner.assemble_stream_response(base64.b64encode(raw))

        self.assertEqual(conversation_id, "abc")
        self.assertEqual(content, "Hello world")

    def test_build_ssl_context_verifies_by_default(self):
        runner = load_runner_module()

        context = runner.build_ssl_context(None, False)

        self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(context.check_hostname)

    def test_auth_headers_normalize_bearer_prefix(self):
        runner = load_runner_module()

        headers = runner.auth_headers("Bearer persistent-key")

        self.assertEqual(headers["Authorization"], "Bearer persistent-key")
        self.assertEqual(headers["X-API-Key"], "persistent-key")
        self.assertEqual(headers["x-access-token"], "persistent-key")

    def test_load_api_key_reads_ignored_env_file(self):
        runner = load_runner_module()
        with tempfile.TemporaryDirectory() as directory:
            env_file = pathlib.Path(directory) / ".env"
            env_file.write_text("ASKLEGAL_API_KEY=persistent-key\n", encoding="utf-8")

            with mock.patch.dict(os.environ, {}, clear=True):
                key = runner.load_api_key(env_file)

        self.assertEqual(key, "persistent-key")

    def test_load_api_key_environment_overrides_env_file(self):
        runner = load_runner_module()
        with tempfile.TemporaryDirectory() as directory:
            env_file = pathlib.Path(directory) / ".env"
            env_file.write_text("ASKLEGAL_API_KEY=file-key\n", encoding="utf-8")

            with mock.patch.dict(os.environ, {"ASKLEGAL_API_KEY": "environment-key"}):
                key = runner.load_api_key(env_file)

        self.assertEqual(key, "environment-key")

    def test_run_suite_parallel_preserves_question_order(self):
        runner = load_runner_module()
        questions = [
            {"id": "hk-001", "query": "First"},
            {"id": "hk-002", "query": "Second"},
        ]

        def fake_execute(item, *_args):
            return runner.QueryResult(item["id"], item["query"], "", item["query"], "", 1, b"")

        with mock.patch.object(runner, "execute_question", side_effect=fake_execute):
            results = runner.run_suite(
                questions, "https://api-dev.ask.legal", "hongkong", 180, mock.Mock(), "key", 0, 2
            )

        self.assertEqual([result.id for result in results], ["hk-001", "hk-002"])

    def test_run_suite_parallel_applies_submission_delay(self):
        runner = load_runner_module()
        questions = [
            {"id": "hk-001", "query": "First"},
            {"id": "hk-002", "query": "Second"},
        ]

        def fake_execute(item, *_args):
            return runner.QueryResult(item["id"], item["query"], "", "Answer", "", 1, b"")

        with mock.patch.object(runner, "execute_question", side_effect=fake_execute):
            with mock.patch.object(runner.time, "sleep") as sleep:
                runner.run_suite(
                    questions,
                    "https://api-dev.ask.legal",
                    "hongkong",
                    180,
                    mock.Mock(),
                    "key",
                    0.25,
                    2,
                )

        sleep.assert_called_once_with(0.25)

    def test_execute_question_marks_empty_answer_as_failed(self):
        runner = load_runner_module()
        stream = runner.StreamResult("conversation", "", b"raw-response")

        with mock.patch.object(runner, "run_query", return_value=stream):
            result = runner.execute_question(
                {"id": "hk-001", "query": "Question"},
                "https://api-dev.ask.legal",
                "hongkong",
                180,
                mock.Mock(),
                "key",
                retries=0,
            )

        self.assertIn("empty response", result.error)
        self.assertEqual(result.raw_body, b"raw-response")

    def test_execute_question_retries_http_500_then_succeeds(self):
        runner = load_runner_module()
        server_error = runner.error.HTTPError(
            "https://api-dev.ask.legal/api/ai/embedChat",
            500,
            "Internal Server Error",
            {},
            io.BytesIO(b'{"success":false}'),
        )
        success = runner.StreamResult("conversation", "Answer", b"raw-answer")

        with mock.patch.object(
            runner, "run_query", side_effect=[server_error, success]
        ) as run_query:
            with mock.patch.object(runner.time, "sleep") as sleep:
                result = runner.execute_question(
                    {"id": "hk-001", "query": "Question"},
                    "https://api-dev.ask.legal",
                    "hongkong",
                    180,
                    mock.Mock(),
                    "key",
                    retries=2,
                    retry_delay=2,
                )

        self.assertEqual(result.response, "Answer")
        self.assertEqual(result.attempts, 2)
        self.assertEqual(run_query.call_count, 2)
        sleep.assert_called_once_with(2)

    def test_execute_question_retries_http_429_then_succeeds(self):
        runner = load_runner_module()
        rate_error = runner.error.HTTPError(
            "https://api-dev.ask.legal/api/ai/embedChat",
            429,
            "Too Many Requests",
            {},
            io.BytesIO(b'{"message":"try later"}'),
        )
        success = runner.StreamResult("conversation", "Answer", b"raw-answer")

        with mock.patch.object(
            runner, "run_query", side_effect=[rate_error, success]
        ) as run_query:
            with mock.patch.object(runner.time, "sleep"):
                result = runner.execute_question(
                    {"id": "hk-001", "query": "Question"},
                    "https://api-dev.ask.legal",
                    "hongkong",
                    180,
                    mock.Mock(),
                    "key",
                )

        self.assertEqual(result.response, "Answer")
        self.assertEqual(result.attempts, 2)
        self.assertEqual(run_query.call_count, 2)

    def test_execute_question_retries_transport_error_then_succeeds(self):
        runner = load_runner_module()
        success = runner.StreamResult("conversation", "Answer", b"raw-answer")

        with mock.patch.object(
            runner,
            "run_query",
            side_effect=[http_client.IncompleteRead(b"partial", 10), success],
        ) as run_query:
            with mock.patch.object(runner.time, "sleep"):
                result = runner.execute_question(
                    {"id": "hk-001", "query": "Question"},
                    "https://api-dev.ask.legal",
                    "hongkong",
                    180,
                    mock.Mock(),
                    "key",
                )

        self.assertEqual(result.response, "Answer")
        self.assertEqual(result.attempts, 2)
        self.assertEqual(run_query.call_count, 2)

    def test_execute_question_retries_empty_response_then_succeeds(self):
        runner = load_runner_module()
        empty = runner.StreamResult("conversation", "", b"raw-empty")
        success = runner.StreamResult("conversation", "Answer", b"raw-answer")

        with mock.patch.object(
            runner, "run_query", side_effect=[empty, success]
        ) as run_query:
            with mock.patch.object(runner.time, "sleep"):
                result = runner.execute_question(
                    {"id": "hk-001", "query": "Question"},
                    "https://api-dev.ask.legal",
                    "hongkong",
                    180,
                    mock.Mock(),
                    "key",
                )

        self.assertEqual(result.response, "Answer")
        self.assertEqual(result.attempts, 2)
        self.assertEqual(run_query.call_count, 2)

    def test_execute_question_stops_after_two_retries(self):
        runner = load_runner_module()

        def server_error():
            return runner.error.HTTPError(
                "https://api-dev.ask.legal/api/ai/embedChat",
                500,
                "Internal Server Error",
                {},
                io.BytesIO(b'{"success":false}'),
            )

        with mock.patch.object(
            runner,
            "run_query",
            side_effect=[
                server_error(),
                server_error(),
                server_error(),
                runner.StreamResult("", "late", b""),
            ],
        ) as run_query:
            with mock.patch.object(runner.time, "sleep") as sleep:
                result = runner.execute_question(
                    {"id": "hk-001", "query": "Question"},
                    "https://api-dev.ask.legal",
                    "hongkong",
                    180,
                    mock.Mock(),
                    "key",
                    retries=2,
                    retry_delay=2,
                )

        self.assertIn("HTTPError 500", result.error)
        self.assertEqual(result.attempts, 3)
        self.assertEqual(run_query.call_count, 3)
        self.assertEqual(sleep.call_args_list, [mock.call(2), mock.call(4)])

    def test_execute_question_does_not_retry_http_402(self):
        runner = load_runner_module()
        quota_error = runner.error.HTTPError(
            "https://api-dev.ask.legal/api/ai/embedChat",
            402,
            "Payment Required",
            {},
            io.BytesIO(b'{"status":"error","message":"Insufficient tokens"}'),
        )

        with mock.patch.object(runner, "run_query", side_effect=quota_error) as run_query:
            with mock.patch.object(runner.time, "sleep") as sleep:
                result = runner.execute_question(
                    {"id": "au-007", "query": "Question"},
                    "https://api-dev.ask.legal",
                    "australia",
                    180,
                    mock.Mock(),
                    "key",
                    retries=2,
                    retry_delay=2,
                )

        self.assertIn("HTTPError 402", result.error)
        self.assertEqual(result.attempts, 1)
        self.assertEqual(run_query.call_count, 1)
        sleep.assert_not_called()

    def test_execute_question_does_not_retry_ordinary_http_401(self):
        runner = load_runner_module()
        auth_error = runner.error.HTTPError(
            "https://api-dev.ask.legal/api/ai/embedChat",
            401,
            "Unauthorized",
            {},
            io.BytesIO(b'{"message":"Invalid API key"}'),
        )

        with mock.patch.object(runner, "run_query", side_effect=auth_error) as run_query:
            with mock.patch.object(runner.time, "sleep") as sleep:
                result = runner.execute_question(
                    {"id": "hk-001", "query": "Question"},
                    "https://api-dev.ask.legal",
                    "hongkong",
                    180,
                    mock.Mock(),
                    "key",
                )

        self.assertIn("HTTPError 401", result.error)
        self.assertEqual(result.attempts, 1)
        self.assertEqual(run_query.call_count, 1)
        sleep.assert_not_called()

    def test_execute_question_retries_prisma_pool_timeout_401(self):
        runner = load_runner_module()
        pool_error = runner.error.HTTPError(
            "https://api-dev.ask.legal/api/ai/embedChat",
            401,
            "Unauthorized",
            {},
            io.BytesIO(b"Timed out fetching a new connection from the connection pool"),
        )
        success = runner.StreamResult("conversation", "Answer", b"raw-answer")

        with mock.patch.object(
            runner, "run_query", side_effect=[pool_error, success]
        ) as run_query:
            with mock.patch.object(runner.time, "sleep") as sleep:
                result = runner.execute_question(
                    {"id": "hk-001", "query": "Question"},
                    "https://api-dev.ask.legal",
                    "hongkong",
                    180,
                    mock.Mock(),
                    "key",
                    retries=2,
                    retry_delay=2,
                )

        self.assertEqual(result.response, "Answer")
        self.assertEqual(result.attempts, 2)
        self.assertEqual(run_query.call_count, 2)
        sleep.assert_called_once_with(2)

    def test_existing_run_directory_is_never_overwritten(self):
        runner = load_runner_module()
        with tempfile.TemporaryDirectory() as directory:
            run_dir = pathlib.Path(directory) / "arm-a"
            run_dir.mkdir()

            with mock.patch.object(runner, "REPO_ROOT", pathlib.Path(directory)):
                with self.assertRaisesRegex(FileExistsError, "Run already exists"):
                    runner.ensure_run_available(run_dir)

    def test_parse_args_requires_arm(self):
        runner = load_runner_module()

        args = runner.parse_args(["experiment.yaml", "--arm", "arm-b", "--dry-run"])

        self.assertEqual(args.arm, "arm-b")
        self.assertEqual(args.parallel, 5)
        self.assertEqual(args.retries, 2)
        self.assertEqual(args.retry_delay, 2)
        self.assertTrue(args.dry_run)

    def test_main_rejects_negative_retry_values(self):
        runner = load_runner_module()

        for option in ("--retries", "--retry-delay"):
            with self.subTest(option=option):
                stderr = io.StringIO()
                with mock.patch("sys.stderr", stderr):
                    result = runner.main(
                        ["experiment.yaml", "--arm", "arm-a", option, "-1"]
                    )

                self.assertEqual(result, 2)
                self.assertIn("cannot be negative", stderr.getvalue())

    def test_main_rejects_non_finite_retry_delay(self):
        runner = load_runner_module()

        for value in ("nan", "inf"):
            with self.subTest(value=value):
                stderr = io.StringIO()
                with mock.patch("sys.stderr", stderr):
                    result = runner.main(
                        [
                            "experiment.yaml",
                            "--arm",
                            "arm-a",
                            "--retry-delay",
                            value,
                        ]
                    )

                self.assertEqual(result, 2)
                self.assertIn("finite", stderr.getvalue())

    def test_main_dry_run_validates_without_creating_run_files(self):
        runner = load_runner_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / "prompts" / "hong-kong").mkdir(parents=True)
            (root / "suites" / "hong-kong" / "general-v1").mkdir(parents=True)
            (root / "rubrics").mkdir()
            experiment_dir = root / "experiments" / "hong-kong" / "comparison"
            experiment_dir.mkdir(parents=True)

            (root / "prompts" / "hong-kong" / "answer-v1.md").write_text(
                "Prompt", encoding="utf-8"
            )
            (root / "suites" / "hong-kong" / "general-v1" / "questions.json").write_text(
                json.dumps([{"id": "hk-001", "query": "Question"}]), encoding="utf-8"
            )
            (root / "rubrics" / "legal-analysis-v1.md").write_text(
                "Rubric", encoding="utf-8"
            )
            experiment_path = experiment_dir / "experiment.yaml"
            experiment_path.write_text(
                """
format_version: 1
name: comparison
jurisdiction: hong-kong
api:
  base_url: https://api-dev.ask.legal
  jurisdiction: hongkong
suite: suites/hong-kong/general-v1/questions.json
rubric: rubrics/legal-analysis-v1.md
arms:
  arm-a:
    label: A
    configuration:
      index: HK-v7
      answer_prompt: prompts/hong-kong/answer-v1.md
  arm-b:
    label: B
    configuration:
      index: HK-v8
      answer_prompt: prompts/hong-kong/answer-v1.md
""".lstrip(),
                encoding="utf-8",
            )

            with mock.patch.object(runner, "REPO_ROOT", root):
                with mock.patch.object(runner, "ensure_run_available") as ensure:
                    with mock.patch("sys.stdout", new_callable=io.StringIO):
                        result = runner.main(
                            [str(experiment_path), "--arm", "arm-a", "--dry-run"]
                        )

            self.assertEqual(result, 0)
            ensure.assert_not_called()
            self.assertFalse((experiment_dir / "runs").exists())

    def test_write_run_saves_jsonl_raw_stream_and_manifest(self):
        runner = load_runner_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            experiment_path = root / "experiment.yaml"
            suite_path = root / "questions.json"
            rubric_path = root / "rubric.md"
            experiment_path.write_text("experiment", encoding="utf-8")
            suite_path.write_text("[]", encoding="utf-8")
            rubric_path.write_text("rubric", encoding="utf-8")
            run_dir = root / "runs" / "arm-a"
            experiment = {
                "name": "comparison",
                "jurisdiction": "hong-kong",
                "api": {"base_url": "https://api-dev.ask.legal", "jurisdiction": "hongkong"},
                "arms": {
                    "arm-a": {"label": "A", "configuration": {"index": "HK-v7"}}
                },
            }
            results = [
                runner.QueryResult(
                    "hk-001",
                    "Question",
                    "conversation",
                    "Answer",
                    "",
                    25,
                    b'{"content":"Answer"}\n',
                    attempts=2,
                )
            ]

            with mock.patch.object(runner, "REPO_ROOT", root):
                runner.write_run(
                    run_dir,
                    experiment_path,
                    experiment,
                    "arm-a",
                    suite_path,
                    None,
                    rubric_path,
                    [],
                    results,
                    "2026-08-24T00:00:00+00:00",
                    1,
                    180,
                    0.5,
                    "enabled",
                    retries=2,
                    retry_delay=2,
                )

            response = json.loads((run_dir / "responses.jsonl").read_text(encoding="utf-8"))
            manifest = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))

        self.assertEqual(response["response"], "Answer")
        self.assertEqual(response["raw_file"], "raw/hk-001.ndjson")
        self.assertEqual(response["attempts"], 2)
        self.assertEqual(manifest["configuration"]["index"], "HK-v7")
        self.assertEqual(manifest["summary"]["succeeded"], 1)
        self.assertEqual(manifest["execution"]["retries"], 2)
        self.assertEqual(manifest["execution"]["retry_delay_seconds"], 2)


if __name__ == "__main__":
    unittest.main()
