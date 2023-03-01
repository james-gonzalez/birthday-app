# Contributing

First of all, thank you for considering contributing! We are always grateful for contributions, and will give feedback on pull requests as soon as we're able.

1. [Where Do I Start?](#where-do-i-start)
2. [Prerequisites](#prerequisites)
3. [Code Conventions](#code-conventions)
4. [Pull Request Lifecycle](#pull-request-lifecycle)

## Where Do I Start?

If you've noticed a bug or have a feature request, please make one. It's usually best if you get confirmation of your issue or approval for your feature request this way before starting to code.

If you have a general question about TEAM_NAME or are just unsure about anything, you can post on the [#<TEAM_SLACK> Slack Channel](https://sainsburys-tech.slack.com/archives/C0156KF4Q93). The issue tracker is for bugs and feature requests.

## Prerequisites

A set of prerequisites for running tests and code [can be found here](../docs/prerequisites.md).

## Code Conventions

Documentation: Each template has its own documentation in `docs` folder with usage examples.

Well-formed Code: Do your best to follow existing conventions you see in the codebase, and ensure your code is formatted with `terraform fmt` ([pre-commit](../docs/prerequisites.md) can help with this). The PR reviewers can help out on this front, and may provide comments with suggestions on how to improve the code. [Danger](../docs/danger-review.md) runs during the CI process, and tests the common code review chores and commit message formats to ensure that your pull request follows this repository's best practices.

Versioning is done by CI and using [semantic-release](https://semantic-release.gitbook.io/semantic-release/). It uses commit messages to determine the next release version. The commit message should be structured as follows:

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

[commitizen](http://commitizen.github.io/cz-cli/) can be used to enforce these types of commits.

## Pull Request Lifecycle

1. You are welcome to submit a [draft pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests#draft-pull-requests) for commentary or review before it is fully completed. It's also a good idea to include specific questions or items you'd like feedback on.

2. Once you believe your pull request is ready to be merged you can create your pull request.

3. When time permits the Digital Cloud Engineering core team members will look over your contribution and either merge, or provide comments letting you know if there is anything left to do.  We may also have questions that we need answered about the code, either because something doesn't make sense to us or because we want to understand your thought process.

4. If we have requested changes, you can either make those changes or, if you disagree with the suggested changes, we can discuss our reasoning and agree on a path forward. Our view is that pull requests are a chance to collaborate, and we welcome conversations about how to do things better. It is the contributor's responsibility to address any changes requested.

5. Once all outstanding comments and checklist items have been addressed, your contribution will be merged! Merged PRs may or may not be included in the next release based on changes the Digital Cloud Engineering team deems breaking or not. Releases and CHANGELOG updates are managed by the team.

6. In some cases, we might decide that a PR should be closed without merging. We'll make sure to provide clear reasoning when this happens. Following the recommended process above is one of the ways to ensure you don't spend time on a PR we can't or won't merge.

### Release Rules

- Commits with a **BREAKING CHANGE** will be associated with a **major** release.
- Commits with type **feat** will be associated with a **minor** release.
- Commits with type **fix** will be associated with a **patch** release.
- Commits with type **perf** will be associated with a **patch** release.
- Commits with scope **no-release** will not be associated with a release type even if they have a **BREAKING CHANGE** or the type **feat**, **fix** or **perf**.
- All other types of commit won't publish a release.
