# Contributing

If you are planning on contributing to AiiDA-FANS, please consider the following guidelines. Additionally, it is strongly recommended to use the pixi package manager to install the appropriate development environment. After cloning this repository, simply run `pixi install` and use the default environment.

## Development
1. Branch off `dev` with a name appropriate for what you are working on (e.g. `feat/myfeature` or `bug/badbug`).
2. Implement, commit, and push your changes.
3. Open a Pull Request into `dev` (e.g. `dev ← feat/myfeature`), then merge and delete your branch.

## Release
1. Open a Pull Request `main ← dev`, then merge but do **not** delete `dev`.
2. Draft a new Release and assign it a new Tag according to the new version number (e.g. `v1.2.3`).
3. Generate release notes and publish the Release.
