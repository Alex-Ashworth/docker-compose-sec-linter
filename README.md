# Docker Compose Security Linter

> Work in progress.

A small Python CLI for inspecting Docker Compose services and highlighting potentially unsafe or incomplete configuration.

Current checks focus on image or build sources, restart policies, privileged mode, and writable short-syntax volume mounts.

The linter currently scans the bundled `src/compose_linter/core/compose_.yml` file. Support for passing a Compose file path to the CLI is not yet implemented.
