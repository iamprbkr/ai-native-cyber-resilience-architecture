from pathlib import Path

import pytest
import yaml


class TestPlaybookYAML:
    PLAYBOOKS_DIR = Path(__file__).resolve().parent.parent.parent / "playbooks"

    def test_all_playbooks_valid_yaml(self) -> None:
        for yaml_file in sorted(self.PLAYBOOKS_DIR.glob("*.yaml")):
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
            assert data is not None, f"Empty YAML: {yaml_file.name}"

    def test_index_contains_all_playbooks(self) -> None:
        with open(self.PLAYBOOKS_DIR / "index.yaml") as f:
            index = yaml.safe_load(f)

        registered = {pb["id"] for pb in index["playbooks"]}
        playbook_files = {f.stem for f in self.PLAYBOOKS_DIR.glob("*.yaml") if f.stem != "index"}

        for pb_id in registered:
            assert pb_id in [
                p.stem for p in self.PLAYBOOKS_DIR.glob("*.yaml")
            ], f"Playbook {pb_id} has no file"

    def test_each_playbook_has_required_fields(self) -> None:
        for yaml_file in self.PLAYBOOKS_DIR.glob("*.yaml"):
            if yaml_file.stem == "index":
                continue
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
            pb = data.get("playbook", data)
            assert "id" in pb, f"Missing id in {yaml_file.name}"
            assert "trigger" in pb, f"Missing trigger in {yaml_file.name}"
            assert "containment" in pb or "immediate_containment" in pb, f"Missing containment in {yaml_file.name}"
