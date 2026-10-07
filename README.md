# NeoNova — AI Assistant

AI assistant portfolio with conversational chat, persistent memory, feedback and agent orchestration. The documentation describes a **Python / FastAPI** backend, **React** frontend and **PostgreSQL** storage.

## Start here

| Guide | Purpose |
| --- | --- |
| [Getting started](docs/guides/GETTING_STARTED.md) | Prerequisites, environment configuration and local setup |
| [Architecture](docs/architecture/ARCHITECTURE.md) | Backend/frontend boundaries and design |
| [API reference](docs/architecture/API.md) | HTTP interfaces |
| [Testing](docs/testing/TESTING.md) | Documented verification workflows |
| [Known issues](docs/troubleshooting/KNOWN_ISSUES.md) | Limitations and workarounds |
| [Full documentation index](docs/README.md) | Configuration, operations and additional guides |

## Local setup

```bash
git clone https://github.com/full-stack-dev-johncastrosanabria/NeoNova.git
cd NeoNova
cp .env.docker.example .env
```

Configure the required services and model-provider settings using the setup guide. Docker Compose configuration is included in the repository.

## Versioned snapshots

Historical releases use the tags `ai` and `ia`. Follow the documentation packaged with a tag when reproducing that snapshot; the current branch may contain later documentation changes.

This is a portfolio source project. Use its testing and known-issues guides when evaluating it in your environment.
