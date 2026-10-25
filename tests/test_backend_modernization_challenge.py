"""
Challenge suite for the 2026-10 Backend Developer modernization.

Verifies: language/runtime baseline pins move to the October 2026 generation
(Go 1.27+, PHP 8.5+, Python 3.14+ with 3.15 current, Node.js 26 LTS line,
PostgreSQL 18 with PG 19 GA 2026-11-19), a Stack Currency rule exists, all
eight backend skills are versioned at 1.0.0, and the role's pattern locks
(outbox, TDD, auth) survive untouched.
"""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ROLE = ROOT / "core" / "roles" / "backend-developer.md"
SKILLS = {
    name: ROOT / "core" / "skills" / "backend" / name / "SKILL.md"
    for name in (
        "add-api-endpoint",
        "add-event-handler",
        "add-service-client",
        "build-mcp-server",
        "implement-auth",
        "implement-structured-outputs",
        "optimize-postgres",
        "scaffold-new-service",
    )
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestLanguageBaselines(unittest.TestCase):
    def test_01_stale_pins_removed(self):
        role = read(ROLE)
        self.assertNotIn("Go 1.25", role)
        self.assertNotIn("PHP 8.4+", role)
        self.assertNotIn("Python 3.13", role)

    def test_02_current_pins_present(self):
        role = read(ROLE)
        self.assertIn("Go 1.27+", role)
        self.assertIn("PHP 8.5+", role)
        self.assertIn("Python 3.14+", role)
        self.assertIn("Python Ecosystem (Python 3.14+; 3.15 current since 2026-10)", role)
        self.assertIn("(Modern PHP 8.5+)", role)

    def test_03_stack_currency_rule(self):
        role = read(ROLE)
        self.assertIn("Stack Currency (2026-10 baseline)", role)
        self.assertIn("Node.js 26", role)
        self.assertIn("2026-10-28", role)
        self.assertIn("2026-10-09", role)  # Python 3.15 release date
        self.assertIn("never adopt a day-one .0 release", role)

    def test_04_postgres_release_line(self):
        role = read(ROLE)
        self.assertIn("PostgreSQL 18", role)
        self.assertIn("2026-11-19", role)  # PG 19 GA (delayed from Sept)

    def test_05_php85_python314_features(self):
        role = read(ROLE)
        self.assertIn("pipe operator", role)
        self.assertIn("free-threaded", role)


class TestSkillVersioning(unittest.TestCase):
    def test_06_all_eight_skills_versioned(self):
        for name, path in SKILLS.items():
            body = read(path)
            self.assertIn(
                "version: 1.0.0", body, msg=f"{name} must carry version: 1.0.0"
            )

    def test_07_skills_within_line_limit(self):
        for name, path in SKILLS.items():
            line_count = len(read(path).splitlines())
            self.assertLess(line_count, 200, msg=f"{name} exceeds 200 lines")


class TestPatternLocksIntact(unittest.TestCase):
    def test_08_core_locks_survive(self):
        role = read(ROLE)
        for lock in (
            "RED-GREEN-TDD LOCK",
            "TRANSACTIONAL-OUTBOX LOCK",
            "AUTH-INVARIANT LOCK",
            "POSTGRES-POOLING-RLS LOCK",
        ):
            self.assertIn(lock, role)

    def test_09_key_patterns_survive(self):
        role = read(ROLE)
        for pattern in (
            "SELECT ... FOR UPDATE SKIP LOCKED",
            "S256",
            "CREATE INDEX CONCURRENTLY",
            "EXPLAIN (ANALYZE, BUFFERS)",
        ):
            self.assertIn(pattern, role)

    def test_10_auth_and_postgres_skills_unchanged_patterns(self):
        self.assertIn("S256", read(SKILLS["implement-auth"]))
        self.assertIn("FORCE ROW LEVEL SECURITY", read(SKILLS["implement-auth"]))
        self.assertIn("CREATE INDEX CONCURRENTLY", read(SKILLS["optimize-postgres"]))
        self.assertIn("statement_cache_size=0", read(SKILLS["optimize-postgres"]))

    def test_11_role_footer_date(self):
        self.assertIn("Last updated: 2026-10-25", read(ROLE))


if __name__ == "__main__":
    unittest.main()
