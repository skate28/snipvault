import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from snipvault.cli import main, parse_tags


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

    def test_help_command_shows_examples_for_each_command(self):
        code, out, _ = self.run_cli("help")
        self.assertEqual(code, 0)
        for cmd in ("add", "list", "show", "search", "rm"):
            self.assertIn(cmd, out)
        # The examples show the literal syntax to type, not just names.
        self.assertIn("snipvault add", out)
        self.assertIn("--lang", out)
        self.assertIn("--tags", out)
        self.assertIn("snipvault search keyword", out)

    def test_bare_invocation_shows_help(self):
        code, out, _ = self.run_cli()
        self.assertEqual(code, 0)
        self.assertIn("Commands:", out)
        self.assertIn("snipvault add", out)

    def test_parse_tags_accepts_commas_spaces_and_both(self):
        self.assertEqual(parse_tags(["a,b,c"]), ["a", "b", "c"])
        self.assertEqual(parse_tags(["a", "b", "c"]), ["a", "b", "c"])
        # PowerShell splitting "a, b, c" into tokens with trailing commas:
        self.assertEqual(parse_tags(["a,", "b,", "c"]), ["a", "b", "c"])
        self.assertEqual(parse_tags(["a, b, c"]), ["a", "b", "c"])
        self.assertEqual(parse_tags(None), [])
        self.assertEqual(parse_tags([]), [])

    def test_add_with_space_separated_tags(self):
        code, out, _ = self.run_cli("add", "t", "code", "--tags", "web", "api", "db")
        self.assertEqual(code, 0)
        code, out, _ = self.run_cli("search", "api")
        self.assertIn("t", out)

    def test_uninstall_prints_instructions(self):
        code, out, _ = self.run_cli("uninstall")
        self.assertEqual(code, 0)
        self.assertIn("uninstall", out.lower())
        # Shows an OS-appropriate command and preserves the user's data note.
        self.assertTrue("uninstall.ps1" in out or "uninstall.sh" in out)
        self.assertIn(".snipvault.json", out)


if __name__ == "__main__":
    unittest.main()
