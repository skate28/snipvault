import tempfile
import unittest
from pathlib import Path

from snipvault.storage import Vault


class VaultTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.vault_path = Path(self.tmpdir.name) / "vault.json"
        self.vault = Vault(self.vault_path)

    def test_add_assigns_incrementing_ids(self):
        first = self.vault.add("one", "python", "print(1)")
        second = self.vault.add("two", "python", "print(2)")
        self.assertEqual(first.id, 1)
        self.assertEqual(second.id, 2)

    def test_add_rejects_empty_title_and_code(self):
        with self.assertRaises(ValueError):
            self.vault.add("  ", "python", "code")
        with self.assertRaises(ValueError):
            self.vault.add("title", "python", "   ")

    def test_add_normalizes_language_and_tags(self):
        s = self.vault.add("t", "  Python ", "x", tags=[" Loops ", "", "WEB"])
        self.assertEqual(s.language, "python")
        self.assertEqual(s.tags, ["loops", "web"])

    def test_persistence_roundtrip(self):
        self.vault.add("persist me", "bash", "echo hi", tags=["shell"])
        reloaded = Vault(self.vault_path)
        self.assertEqual(len(reloaded.all()), 1)
        snippet = reloaded.get(1)
        self.assertEqual(snippet.title, "persist me")
        self.assertEqual(snippet.tags, ["shell"])

    def test_get_missing_raises(self):
        with self.assertRaises(KeyError):
            self.vault.get(99)

    def test_remove_deletes_and_persists(self):
        self.vault.add("bye", "text", "x")
        removed = self.vault.remove(1)
        self.assertEqual(removed.title, "bye")
        self.assertEqual(Vault(self.vault_path).all(), [])

    def test_search_is_case_insensitive_across_fields(self):
        self.vault.add("List trick", "python", "[x for x in y]", tags=["loops"])
        self.vault.add("Grep files", "bash", "grep -r foo .", tags=["search"])
        self.assertEqual(len(self.vault.search("LOOPS")), 1)   # tag
        self.assertEqual(len(self.vault.search("grep")), 1)    # title/code
        self.assertEqual(len(self.vault.search("python")), 1)  # language
        self.assertEqual(self.vault.search("nomatch"), [])

    def test_ids_not_reused_after_delete_of_last(self):
        self.vault.add("a", "text", "1")
        self.vault.add("b", "text", "2")
        self.vault.remove(1)
        third = self.vault.add("c", "text", "3")
        self.assertEqual(third.id, 3)


if __name__ == "__main__":
    unittest.main()
