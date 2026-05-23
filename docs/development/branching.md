# Branching Strategy

This repository uses a lightweight GitHub Flow. Keep the model simple:
`main` is protected, short-lived branches carry changes, and every change lands
through a pull request.

## Branches

- `main` is the only long-lived branch.
- `main` should always be releasable.
- Do not push commits directly to `main`.
- Do not create a permanent `develop` branch. This project is small enough that
  a second integration branch would add delay without improving safety.
- Create short-lived branches from the latest `main`.

Use these branch name prefixes:

- `feature/<short-name>` for user-facing behavior or new capabilities.
- `fix/<short-name>` for bug fixes.
- `docs/<short-name>` for documentation-only changes.
- `chore/<short-name>` for maintenance, tooling, or dependency updates.
- `release/<version>` only when release preparation needs multiple commits.
- `hotfix/<short-name>` for urgent fixes based on `main`.

## Normal Change Flow

1. Update local `main` from `origin/main`.
2. Create a short-lived branch.
3. Keep commits focused and related to one change.
4. Open a draft pull request early if feedback or CI visibility is useful.
5. Run `scripts/check` locally before marking the pull request ready.
6. Merge only after required checks pass and the review expectation is met.
7. Delete the branch after merge.

Prefer squash merges for small, focused pull requests so `main` stays readable.
Use a regular merge only when preserving multiple commits adds clear value.

## Pull Request Rules

Each pull request should include:

- A short summary of the behavior or documentation change.
- Tests or a note explaining why tests were not needed.
- Any migration, release, or compatibility notes.
- Confirmation that `scripts/check` passed locally, unless CI is the only
  practical validation path.

Pull requests should stay small. If a branch grows into unrelated changes, split
it before review.

## Releases

Releases are cut from `main`.

1. Merge release preparation changes through a pull request.
2. Tag the release commit on `main`.
3. Build and publish artifacts from the tagged commit.

Do not release from feature branches.

## Repository Protection

Configure GitHub branch protection for `main`:

- Require pull requests before merging.
- Require status checks to pass before merging.
- Require branches to be up to date before merging when GitHub can enforce it
  without creating excessive noise.
- Restrict direct pushes to `main`.

One approval can be optional if required checks are strong, but changes should
still go through a pull request rather than direct pushes.
