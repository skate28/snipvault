import tempfile
import unittest
from pathlib import Path

from snipvault.sessions import SessionStore


class SessionStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.path = Path(self.tmpdir.name) / "sessions.json"
        self.store = SessionStore(self.path)

    def test_start_creates_active_session_and_flag(self):
        s = self.store.start("work")
        self.assertEqual(s.id, 1)
        self.assertEqual(s.name, "work")
        self.assertIsNone(s.ended)
        self.assertEqual(self.store.active, 1)
        self.assertTrue(self.store.flag_path.exists())

    def test_start_defaults_name_when_blank(self):
        self.assertEqual(self.store.start("  ").name, "session")

    def test_cannot_start_two_sessions(self):
        self.store.start("a")
        with self.assertRaises(ValueError):
            self.store.start("b")

    def test_record_appends_only_while_active(self):
        self.store.start("w")
        self.assertTrue(self.store.record("git status"))
        self.assertTrue(self.store.record("ls"))
        self.assertEqual(len(self.store.active_session().commands), 2)

    def test_record_noop_when_no_active_session(self):
        self.assertFalse(self.store.record("git status"))

    def test_record_ignores_blank(self):
        self.store.start("w")
        self.assertFalse(self.store.record("   "))

    def test_end_finalizes_and_clears_flag(self):
        self.store.start("w")
        self.store.record("echo hi")
        s = self.store.end()
        self.assertIsNotNone(s.ended)
        self.assertIsNone(self.store.active)
        self.assertFalse(self.store.flag_path.exists())

    def test_end_without_active_raises(self):
        with self.assertRaises(ValueError):
            self.store.end()

    def test_persistence_roundtrip(self):
        self.store.start("persist")
        self.store.record("cmd one")
        self.store.end()
        reloaded = SessionStore(self.path)
        self.assertEqual(len(reloaded.all()), 1)
        s = reloaded.get(1)
        self.assertEqual(s.name, "persist")
        self.assertEqual(s.commands[0].text, "cmd one")

    def test_duration_none_while_active_then_computed(self):
        s = self.store.start("w")
        self.assertIsNone(s.duration_seconds())
        self.store.end()
        self.assertIsNotNone(self.store.get(1).duration_seconds())

    def test_get_missing_raises(self):
        with self.assertRaises(KeyError):
            self.store.get(42)

    def test_ids_increment_across_sessions(self):
        self.store.start("a")
        self.store.end()
        self.store.start("b")
        self.assertEqual(self.store.active_session().id, 2)


if __name__ == "__main__":
    unittest.main()
