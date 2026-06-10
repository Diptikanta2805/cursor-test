# AGENTS.md

## Cursor Cloud specific instructions

### Repository state

This repository (`cursor-test`) is a **minimal placeholder**: it contains only `README.md` with the title `cursor-test`. There is no application source code, no package manifests (`package.json`, `pyproject.toml`, etc.), no Docker/Compose setup, and no lint/test/build scripts.

### Services

| Service | Required? | Notes |
|---------|-----------|-------|
| *(none)* | — | Nothing to start or run until application code is added |

### Lint / test / build / dev

Not applicable until a stack is added. When code is introduced, document commands here and in `README.md`.

### VM environment

- **Update script**: `true` (no dependency refresh needed for an empty repo).
- **Available tooling** (VM baseline): Git, Node.js (via nvm), pnpm/npm/yarn, Python 3.12, pip.
- **Git**: Default branch is `main`; remote is `origin` on GitHub (`Diptikanta2805/cursor-test`).

### Adding an application later

When this repo gains real code, update:

1. The VM **update script** (e.g. `npm install`, `pip install -r requirements.txt`) via `.cursor/environment.json` or the SetupVmEnvironment flow.
2. This section with service startup commands, ports, and non-obvious dev gotchas.
