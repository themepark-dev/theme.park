# Working on theme.park

This project injects CSS into other applications. Reproduce CSS bugs in the
affected app and inspect the result in a browser.

## Maintainer instructions

- Do not push, publish, deploy, or trigger deployment workflows without an
  explicit instruction from the maintainer. Describing their usual release
  workflow does not authorize a push. Keep trial-run work local and reviewable.
- Preserve existing work. Inspect the working tree before editing or changing
  branches; do not reset unrelated changes.
- Always create task branches from freshly fetched `origin/develop`, including
  CSS fixes and development tooling. Verify the starting commit before editing.
  The normal flow is a task branch from `develop`, then a merge back into
  `develop`. Target pull requests at `develop` as well.
- Reserve `testing` for potentially breaking changes that need isolation from
  users of `develop`. It is not a required step for ordinary fixes. Users of
  `testing` accept disruption; protecting them is not a release constraint.
- App UI rewrites do not need backward compatibility unless the rewrite targets
  the themed app's development branch. In that case, preserve support for its
  stable release.
- Add development tools when an app needs them. Record setup steps in
  `dev/<app>/README.md` so the next session can reuse them.
- Document discoveries that would help another session before finishing a task.
  Put shared workflow lessons in `dev/README.md` and app-specific lessons in
  `dev/<app>/README.md`. Apply the `unslop` skill to these notes. Explain what
  happened, why it matters, and how to reproduce or avoid it. Update existing
  guidance instead of duplicating it, and distinguish verified findings from
  untested ideas. Keep run-specific evidence under ignored `dev/artifacts/`.
- Always apply the `unslop` skill to writing. Keep PR titles and descriptions
  short, stating the user-visible fixes and relevant validation. Before/after
  screenshot attachments are optional for bug-fix PRs, per the maintainer.
  The skill source is
  [cursor/plugins unslop](https://raw.githubusercontent.com/cursor/plugins/refs/heads/main/pstack/skills/unslop/SKILL.md).

## Read before starting

1. Read [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md).
2. Read [dev/README.md](dev/README.md) and any `dev/<app>/README.md`.
3. Consult the [setup docs](https://docs.theme-park.dev/setup/), the target app's
   documentation page, and its entry in
   [mkdocs.yml](https://github.com/themepark-dev/tp-docs/blob/main/mkdocs.yml).
   The documentation source is the separate
   [tp-docs repository](https://github.com/themepark-dev/tp-docs).
   Check app-specific exceptions before using a generic installation recipe.
4. Read the issue, relevant base CSS, its imports, and recent fixes. Record the
   reported app version and installation method. Check whether an existing
   commit already addresses the issue.

## Implementation and verification

- Follow `dev/README.md`. Reuse the app's setup or add one with sample data and
  startup commands.
- Edit `css/base/<app>/<app>-base.css` for app-specific styling. Inspect shared
  files in `css/defaults` before changing them. Servarr apps share styles.
- Use existing variables in `css/theme-options` and
  `css/community-theme-options`. Preserve their value formats and the meaning
  of status colors. Scope overrides to the affected component where possible.
- Generated `<app>/<theme>.css` wrappers come from `themes.py`. Do not hand-edit
  generated output or populate the working tree with build artifacts.
- Confirm the browser loads the edited local stylesheet and its imports.
  Verify the final files through the documented injection method, even if you
  used temporary browser styles while investigating.
- Save before/after screenshots and inspect the rendered result. Computed-style
  assertions alone do not establish visibility, contrast, or correct layout.
- Test the affected interaction states, theme options, browsers, and viewport
  sizes. Include solid-color, radial-gradient, and linear-gradient backgrounds.
  Check the actual variables used by the component, not just the page background.
  Follow the screenshot requirements in
  CONTRIBUTING.md when adding a new application theme.
- Report app and browser versions, installation method, evidence, and untested
  areas. Do not claim an issue fixed from a screenshot or source inspection alone.
- Add any setup requirements you discover to the app's development notes.
  Record other UI defects found during inspection separately from the reported
  bug. Explain which ones the patch fixes and which remain.
  Target `develop` for contributions. Push only when the maintainer instructs you.
