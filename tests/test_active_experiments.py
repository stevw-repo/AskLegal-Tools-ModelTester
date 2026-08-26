import importlib.util
import pathlib
import sys
import unittest


REPO_ROOT = pathlib.Path(__file__).parents[1]
SCRIPT_PATH = REPO_ROOT / "tools" / "run_experiment.py"


def load_runner_module():
    spec = importlib.util.spec_from_file_location("active_experiment_runner", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ActiveExperimentTests(unittest.TestCase):
    def test_active_experiments_and_inputs_validate(self):
        runner = load_runner_module()
        experiment_paths = sorted(REPO_ROOT.glob("experiments/*/*/experiment.yaml"))
        self.assertTrue(experiment_paths, "No active experiments found.")

        for experiment_path in experiment_paths:
            with self.subTest(experiment=experiment_path.parent.name):
                experiment = runner.load_experiment(experiment_path)
                jurisdiction = experiment["jurisdiction"]
                self.assertEqual(experiment_path.parent.parent.name, jurisdiction)
                self.assertEqual(
                    experiment["api"]["base_url"], "https://api-dev.ask.legal"
                )
                self.assertTrue(experiment["suite"].startswith(f"suites/{jurisdiction}/"))

                suite_path = runner.resolve_repo_path(experiment["suite"], "Suite")
                questions = runner.load_questions(suite_path)
                question_ids = {item["id"] for item in questions}

                if experiment.get("expectations"):
                    expectations_path = runner.resolve_repo_path(
                        experiment["expectations"], "Expectations"
                    )
                    runner.load_expectations(expectations_path, question_ids)

                runner.resolve_repo_path(experiment["rubric"], "Rubric")
                for arm in experiment["arms"].values():
                    runner.collect_prompt_files(arm["configuration"])


if __name__ == "__main__":
    unittest.main()
