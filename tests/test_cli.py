import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from snipvault.cli import main


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.vault_path = str(Path(self.tmpdir.name) / "vault.json")

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(["--vault", self.vault_path, *args])
        return code, out.getvalue(), err.getvalue()

    def test_add_then_list(self):
        code, out, _ = self.run_cli("add", "hello", "print('hi')", "--lang", "python")
        self.assertEqual(code, 0)
        self.assertIn("added snippet 1", out)

        code, out, _ = self.run_cli("list")
        self.assertEqual(code, 0)
        self.assertIn("hello", out)
        self.assertIn("python", out)

    def test_show_prints_raw_code(self):
        self.run_cli("add", "greet", "print('hi')", "--lang", "python")
        code, out, _ = self.run_cli("show", "1")
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "print('hi')")

    def test_show_missing_id_errors(self):
        code, _, err = self.run_cli("show", "42")
        self.assertEqual(code, 1)
        self.assertIn("no snippet with id 42", err)

    def test_add_empty_title_errors(self):
        code, _, err = self.run_cli("add", "   ", "x")
        self.assertEqual(code, 1)
        self.assertIn("title must not be empty", err)

    def test_search_and_rm(self):
        self.run_cli("add", "loop trick", "[x for x in y]", "--lang", "python",
                     "--tags", "loops,tricks")
        self.run_cli("add", "grep files", "grep -r foo .", "--lang", "bash")

        code, out, _ = self.run_cli("search", "loops")
        self.assertEqual(code, 0)
        self.assertIn("loop trick", out)
        self.assertNotIn("grep files", out)

        code, out, _ = self.run_cli("rm", "1")
        self.assertEqual(code, 0)
        self.assertIn("removed snippet 1", out)

        code, out, _ = self.run_cli("list")
        self.assertNotIn("loop trick", out)

    def test_list_empty_vault(self):
        code, out, _ = self.run_cli("list")
        self.assertEqual(code, 0)
        self.assertIn("(no snippets)", out)


if __name__ == "__main__":
    unittest.main()
