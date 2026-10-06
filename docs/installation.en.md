# Installation, first use, and updates

[中文](installation.md) · [Compatibility](compatibility.en.md)

Use an Agent host that can read local Skill files. Optional repository helpers use the **Python 3.10+ standard library**, with no pip dependencies or extra API key. The host supplies models and search tools. This guide is an optional aid; the [frozen Skill](../skills/research-discovery-workflow/SKILL.md) remains the authoritative workflow.

## 1. Get the files

### Clone

```sh
git clone https://github.com/heisenberg0020/research-discovery-workflow.git
cd research-discovery-workflow
```

This gets the default branch. To pin v1.2.0, use `git clone --branch v1.2.0 --depth 1 https://github.com/heisenberg0020/research-discovery-workflow.git`. Replace the tag if you choose another published version.

### Release ZIP: check before extracting

Download the custom assets `research-discovery-workflow-1.2.0.zip`, `manifest.json`, and `SHA256SUMS` from the **same version** on [Releases](https://github.com/heisenberg0020/research-discovery-workflow/releases), keeping all three in one directory. For another version, replace `1.2.0` in every ZIP and directory name below with the downloaded version. GitHub's automatic “Source code (zip)” is a different archive and does not use this asset layout.

In the download directory, use one of these commands. **Both the ZIP and manifest must pass before extraction.**

```sh
# macOS, when shasum is available
shasum -a 256 -c SHA256SUMS
```

```sh
# Linux or another environment with sha256sum
sha256sum -c SHA256SUMS
```

If the command is unavailable, a file is missing, or a check fails, resolve that before using this download. The checks establish consistency with the checksum file. A downloaded `SHA256SUMS` is **not an authenticity signature**; it cannot by itself establish a trusted origin or detect replacement of all assets together.

After the checks pass, use your archive tool, or:

```sh
unzip research-discovery-workflow-1.2.0.zip
cd research-discovery-workflow-1.2.0
```

The archive's top-level directory is `research-discovery-workflow-1.2.0/`; its Skill entry is `skills/research-discovery-workflow/SKILL.md`. Keep the three downloaded assets outside the extracted directory. Download checksum checks require no source Git repository. Windows users can compare both SHA-256 values with an available checksum tool; these shell instructions and host loading are not Windows compatibility certification.

## 2. Select and check Python

Your executable may be named `python3`, `python`, or use an absolute path. The name alone does not establish the version. In a macOS/Linux shell, select your actual executable, run the check, and reuse the variable:

```sh
RDW_PYTHON=python3  # Replace with python or the actual executable's full path as needed
"$RDW_PYTHON" -c 'import sys; print(sys.executable); print(sys.version); raise SystemExit(0 if sys.version_info >= (3, 10) else "Python 3.10+ is required")'
```

The check must succeed with Python 3.10 or newer before using the helpers. Windows launchers depend on the installation, for example `py -3`; check the actual version there too. The shell variable examples are not PowerShell syntax. Reading the intact Skill directly requires no Python; see the [explicit-read fallback](compatibility.en.md#explicit-read-fallback).

## 3. Preview, then install

Run from the cloned or extracted package root, reusing the checked `RDW_PYTHON` in the same terminal:

```sh
"$RDW_PYTHON" scripts/install.py --dry-run
"$RDW_PYTHON" scripts/install.py
```

The default destination is `$CODEX_HOME/skills` when `CODEX_HOME` is set, otherwise `$HOME/.codex/skills`. The helper does not change environment variables or global host configuration. Preview writes nothing; installation copies files.

An existing `research-discovery-workflow` target, including a symlink, causes refusal rather than replacement or automatic upgrade. The installed payload contains the frozen entry, references, metadata, and preparation helper, plus the repository MIT license. It excludes examples, tests, and research results.

To choose a different destination:

```sh
"$RDW_PYTHON" scripts/install.py --dest ./local-skills --dry-run
"$RDW_PYTHON" scripts/install.py --dest ./local-skills
```

The resulting entry is `./local-skills/research-discovery-workflow/SKILL.md`. Whether a host discovers a custom destination depends on that host. Reload or restart its Skill list as supported. A successful copy does not establish successful host loading.

## 4. Optional: check reading only

Send this prompt to the host if useful. This is a usage diagnostic, not a new research stage or a prerequisite for the workflow.

```text
This request only checks whether research-discovery-workflow is readable. Do not start research.
Locate the actual SKILL.md available to you and report its real path; do not infer loading from the Skill name alone.
Read that entry and locate its local references as instructed. Report the references read and any missing or unreadable files.
Describe the host's actual search, file-access, fresh-context, and memory-control capabilities and limits. Mark anything you cannot verify as unverified.
Do not create a research workspace, run the preparation helper, search for papers, generate research candidates, or execute Q0–Q7.
If automatic discovery is unavailable, report that and wait for an explicit file path.
```

If automatic loading is unavailable, use the [explicit-read fallback](compatibility.en.md#explicit-read-fallback), keeping the whole Skill directory and its references intact.

## 5. Start in a fresh context

Copy the [English neutral brief](../examples/neutral-brief.en.md) to a personal file and fill it with your real interests, boundaries, and resource facts. Start a fresh, non-forked chat, supply the brief and a clean output workspace, and use the [frozen English first-run prompt](QUICKSTART.en.md#one-run). Installation and the optional reading check do not start research. State any actual limitations on memory or file access.

Optionally prepare a workspace. The parent must exist and the target must not exist:

```sh
mkdir -p ./runs
"$RDW_PYTHON" skills/research-discovery-workflow/scripts/prepare_run.py \
  --root ./runs/pass-1 --brief ./my-neutral-brief.md --pass-number 1
```

Replace the brief filename with your completed file. This path runs from the package root; use the actual installed path when invoking an installed copy. Success means preparation only: **research has not started**. The frozen English guide covers two passes, delayed handoff, and first use without prior results.

## Updates and existing copies

Repository distribution versions retain the byte-frozen Workflow v1.0.0. Updating an existing Skill does not add research capabilities; see the [changelog](../CHANGELOG.md).

If you choose to replace an installation, first inspect and back up any personal changes, then choose the new directory and switch method. The installer has no `--force` and does not delete the old copy. You can try a new custom destination first; the host may need its own discovery configuration.

## Optional inventory verification and maintainer builds

After checking download hashes, extracting, and inspecting the local helper, you can check the archive's complete file inventory. If the three downloaded assets are one directory above the extracted root:

```sh
"$RDW_PYTHON" scripts/build_release.py --verify ../research-discovery-workflow-1.2.0.zip
```

`--verify` requires no Git repository, performs no extraction or installation, and starts no research. It checks archive consistency with the external manifest, not authenticity or research quality.

Only **building** a release requires Git, clean committed source, an existing parent directory, and a nonexistent output directory:

```sh
"$RDW_PYTHON" scripts/check_repo.py
"$RDW_PYTHON" -m unittest discover -s tests -v
mkdir -p ./dist
"$RDW_PYTHON" scripts/build_release.py --output ./dist/v1.2.0
"$RDW_PYTHON" scripts/build_release.py --verify ./dist/v1.2.0/research-discovery-workflow-1.2.0.zip
```

The build takes its version from `VERSION`; match the example paths to that actual version. It includes only committed public files, excluding local runs and caches.
