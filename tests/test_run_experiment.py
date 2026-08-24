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
  base_url: https://dev.ask.legal
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
  base_url: https://dev.ask.legal
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
                questions, "https://dev.ask.legal", "hongkong", 180, mock.Mock(), "key", 0, 2
            )

        self.assertEqual([result.id for result in results], ["hk-001", "hk-002"])

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
        self.assertTrue(args.dry_run)

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
  base_url: https://dev.ask.legal
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
                with mock.patch("sys.stdout", new_callable=io.StringIO):
                    result = runner.main([str(experiment_path), "--arm", "arm-a", "--dry-run"])

            self.assertEqual(result, 0)
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
                "api": {"base_url": "https://dev.ask.legal", "jurisdiction": "hongkong"},
                "arms": {
                    "arm-a": {"label": "A", "configuration": {"index": "HK-v7"}}
                },
            }
            results = [
                runner.QueryResult(
                    "hk-001", "Question", "conversation", "Answer", "", 25, b'{"content":"Answer"}\n'
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
                )

            response = json.loads((run_dir / "responses.jsonl").read_text(encoding="utf-8"))
            manifest = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))

        self.assertEqual(response["response"], "Answer")
        self.assertEqual(response["raw_file"], "raw/hk-001.ndjson")
        self.assertEqual(manifest["configuration"]["index"], "HK-v7")
        self.assertEqual(manifest["summary"]["succeeded"], 1)


if __name__ == "__main__":
    unittest.main()
