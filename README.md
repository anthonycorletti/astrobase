![](https://github.com/astrobase/brand/blob/master/logos/space-logo.png?raw=true)

[![publish](https://github.com/astrobase/astrobase/actions/workflows/publish.yaml/badge.svg)](https://github.com/astrobase/astrobase/actions/workflows/publish.yaml)
[![test](https://github.com/astrobase/astrobase/actions/workflows/test.yaml/badge.svg)](https://github.com/astrobase/astrobase/actions/workflows/test.yaml)
[![codecov](https://codecov.io/gh/astrobase/astrobase/branch/master/graph/badge.svg?token=LdSYGUjerD)](https://codecov.io/gh/astrobase/astrobase)

[**Why Astrobase**](#why-astrobase) |
[**Docs**](./docs) |
[**Who uses Astrobase?**](./docs/who-uses-astrobase.md) |
[**Roadmap**](./docs/roadmap.md) |
[**Contributing**](./CONTRIBUTING.md) |
[**Credits**](#credits)

## Why Astrobase?

Astrobase provides:

- A streamlined framework for deploying multi-cloud systems
- Bring together the best products of all cloud vendors; S3, BigQuery, GKE, SageMaker, Lambda, Kinesis, etc.
- Low-code overhead
- Cloud bursting capabilities
- ***Pass any parameter directly into your kubernetes yaml from the command line!***
- Multiple deployment environment profiles
- API Server works anywhere docker containers work
- Live, interactive documentation built right in!
- Lightweight and unopinionated configs – we only do what cloud vendors do.
- One fast, easy way to define and create infrastructure and deployment configs as code
- No more chicken-and-egg problems for running infrastructure – you only need Astrobase to deploy infrastructure and resources.
- No DSL or proprietary language to learn! Astrobase is built entirely on top of open source components.
- No more dependency graphs or surprises when making changes to your infrastructure-as-code!

## Getting Started

If you haven't already installed the [Astrobase CLI](https://github.com/astrobase/cli) yet, please do. The CLI the best way to work with Astrobase, and has an awesome [walkthrough of the features and usage of the cli](https://github.com/astrobase/cli#features-and-usage).

After that, read Astrobase's [docs](./docs) for more.

## Credits

- The Astrobase API server is built on top of [fastapi](https://github.com/tiangolo/fastapi).
- The Astrobase CLI is built on top of [typer](https://github.com/tiangolo/typer).

