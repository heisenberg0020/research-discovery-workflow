"""Package structure checks, not proof of scientific quality."""

from pathlib import Path
import re
import unittest


REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / "skills" / "research-discovery-workflow"


class PackageTests(unittest.TestCase):
    def test_skill_frontmatter_and_size(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertRegex(text, r"\A---\nname: research-discovery-workflow\n")
        self.assertIn("description:", text.split("---", 2)[1])
        self.assertLess(len(text.splitlines()), 500)
        self.assertNotIn("[TODO:", text)

    def test_relative_markdown_links_resolve(self):
        for file in REPO.rglob("*.md"):
            if ".git" in file.parts:
                continue
            text = file.read_text(encoding="utf-8")
            for target in re.findall(r"\]\(([^)]+)\)", text):
                if target.startswith(("https://", "http://", "#", "mailto:")):
                    continue
                target_path = target.split("#", 1)[0]
                if not target_path:
                    continue
                with self.subTest(file=file.relative_to(REPO), target=target):
                    self.assertTrue((file.parent / target_path).is_file())

    def test_skill_reference_files_are_directly_indexed(self):
        entry = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        references = list((SKILL / "references").glob("*.md"))
        self.assertTrue(references)
        for file in references:
            with self.subTest(reference=file.name):
                self.assertIn(f"references/{file.name}", entry)
                self.assertLess(len(file.read_text(encoding="utf-8").splitlines()), 400)

    def test_authored_package_has_no_personal_paths_or_chat_ids(self):
        files = [REPO / "README.md", REPO / "AGENTS.md"]
        files += list((REPO / "docs").glob("*.md"))
        files += list(SKILL.rglob("*.md"))
        for file in files:
            text = file.read_text(encoding="utf-8")
            with self.subTest(file=file.relative_to(REPO)):
                self.assertNotIn("/Users/", text)
                self.assertNotIn("codex://threads/", text)

    def test_q5_review_precedes_q6_in_entrypoint(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertLess(text.index("| **Q5-R**"), text.index("| Q6 |"))
        self.assertIn("not_applicable", text)
        self.assertIn("pending_handoff", text)
        self.assertIn("insight-reporting.md", text)

    def test_ui_prompt_names_the_skill(self):
        metadata = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("$research-discovery-workflow", metadata)
        description = re.search(r'  short_description: "([^"\n]+)"', metadata)
        self.assertIsNotNone(description)
        self.assertGreaterEqual(len(description.group(1)), 25)
        self.assertLessEqual(len(description.group(1)), 64)

    def test_comparison_plan_precedes_comprehensive_report(self):
        entry = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertLess(entry.index("| Q7-A |"), entry.index("| Q7-B |"))
        scheme = (SKILL / "references" / "comparison-plan.md").read_text(encoding="utf-8")
        for heading in ("## 1.", "## 2.", "## 3.", "## 4."):
            self.assertIn(heading, scheme)
        self.assertIn("resource assessment", scheme)
        self.assertIn("Incomplete", scheme)
        self.assertIn("retained main research object", scheme)
        self.assertIn("do not", scheme.lower())


if __name__ == "__main__":
    unittest.main()
