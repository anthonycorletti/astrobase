# Astrobase Docs

Hi there! Welcome to Astrobase's docs.

To get started using Astrobase right away, we suggest reading through the [astrobase cli README](https://github.com/astrobase/cli/blob/master/README.md) and/ or checking out our [showcase](https://github.com/astrobase/showcase).

If you'd like to start hacking on astrobase, check out our [contributing guide](../CONTRIBUTING.md).

For more details about Astrobase, and using astrobase, read on!

## Design and Architecture

Astrobase was created because infrastructure and deployment management of containerized systems is not easy - **we believe it should be**.

Developers and teams of developers should not have to spend time solving problems that occur from opionionated infrastructure-as-code tools that make changes they did not intend. Astrobase simply passes requests directly to cloud providers and allows you to manage all cloud resources from one control-plane.

Astrobase will not restrict developers to a special deployment toolset. Developers can use whatever tool they want to deploy their services – be it `kubectl`, `helm`, `nomad`, or something else! This is why we take a lightweight approach to resource deployment. Similarly to how you define clusters in the form of `.yaml` files, specify a resources documentation that simply references where your configs are, and deploy them!

## Installation and Usage
