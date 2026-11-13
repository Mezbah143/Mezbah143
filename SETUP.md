# Mezbah Uddin · Midnight Aurora

A GitHub profile built with Markdown, supported HTML, original SVG artwork, local technology icons, and scheduled GitHub Actions. No JavaScript runs inside the README.

## Account and publishing

The intended profile repository is **[Mezbah143/Mezbah143](https://github.com/Mezbah143/Mezbah143)**. It must be public, and `README.md` must be at the root of its default branch (`main`). This is the special repository GitHub displays on your profile.

Commit `README.md`, `SETUP.md`, `assets/`, `scripts/`, and `.github/workflows/snake.yml` to `main`. Do not publish `.preview/` or temporary output. The source branch is `main`; generated images are published to `output`.

## First workflow run

1. Open the repository’s **Actions** tab. If GitHub asks whether to enable workflows, enable them for this repository.
2. Choose **Refresh profile visuals → Run workflow → main**.
3. Wait for a successful run. The `output` branch should contain `stats.svg`, `languages.svg`, `activity.svg`, `github-snake.svg`, and `github-snake-dark.svg`.
4. Open [your profile](https://github.com/Mezbah143). GitHub’s image cache can delay visible updates.

The workflow runs daily at **12:23 p.m. Korea time (03:23 UTC)** and whenever its source or scripts change on `main`. Schedules are approximate and may be delayed by GitHub. Scheduled workflows in inactive public repositories may be disabled by GitHub; re-enable from Actions when necessary.

The workflow explicitly requests `contents: write` to publish generated assets. The standard, automatically supplied `GITHUB_TOKEN` is sufficient; no personal access token or new secret is required. Repository/organization policies can still restrict Actions or branch writes. If a push is denied, inspect the run log and the repository’s Actions policy and rules for `output`; do not remove protections from unrelated branches.

## What the automation does

- Retrieves public GitHub repositories and the contribution calendar through GitHub’s GraphQL API.
- Draws matching statistics, language, and 31-day contribution cards with Python’s standard library.
- Generates animated contribution snakes with [Platane/snk](https://github.com/Platane/snk).
- Validates the SVGs and commits only generated SVG files to `output`.
- Preserves previously published images if a generator fails, and reports the partial refresh as a failed run. The first run must produce all five files.

Statistics are daily snapshots, not real-time counters. Repository/star/language metrics cover **public, owned, non-fork repositories**. The contribution total follows GitHub’s calendar; it includes contribution types beyond commits. The longest streak is explicitly limited to the fetched year. Current streak permits a zero-contribution current UTC day, so yesterday’s streak remains active until today ends. Language percentages are based on GitHub’s code-byte classification and do not measure skill.

Public endpoints tested on November 11, 2026 returned 503 for github-readme-stats, 402 for the activity graph provider, and 403 for the streak and skillicons services. The cards therefore use GitHub itself as their live data provider and are served from this repository. Custom graphics and Devicon icons are local. The optional Komarev counter worked when checked; it counts image loads rather than unique people and may be affected by caching. Remove its final `<p>` from `README.md` if it stops working.

## Personalization still needed

These are intentional plain-text placeholders, never fake clickable links:

| Placeholder | What to supply |
|---|---|
| `[ADD VERIFIED LINKEDIN PROFILE]` | Your own LinkedIn profile URL |
| `[ADD VERIFIED JAVAFX ATM REPOSITORY]` | The public ATM project repository |
| `[ADD VERIFIED ARDUINO REPOSITORY]` | The public door-lock project repository |

Email and portfolio were verified against the existing public portfolio source. Education and expected graduation follow the supplied brief. JavaFX ATM and Arduino descriptions follow the brief; their source and completion status have not been independently verified. Review these descriptions if their scope changes.

StudentBridge is linked to the supplied team repository. Its current README describes seeded frontend jobs, partially working authentication requiring database setup, and application submission as unfinished. SoccerSense’s verified source is **[Mezbah143/SDLC-PROJECT](https://github.com/Mezbah143/SDLC-PROJECT)**: its HTML identifies SoccerSense, and its JavaScript contains placeholder API credentials. It is presented as a prototype, with no deployed live-score claim.

## Editing the artwork

Edit `scripts/build_assets.py`, then run:

```sh
python3 scripts/build_assets.py
```

This rebuilds the desktop/mobile headers, project technology badges, and contact buttons. The palette is midnight navy `#0b1020`, cyan `#67e8f9`, violet `#a78bfa`, and restrained pink `#f0abcf`. Headers use SVG-contained CSS animation, with reduced-motion support. Essential information is also present in README text and image alt text. The desktop header uses a 1200×420 viewBox; the mobile alternative uses 600×490. Text remains selectable throughout the main Markdown sections.

GitHub controls the page background, HTML sanitization, typography outside images, and layout. The dark artwork is self-contained and remains readable in light mode. Project text and headings inherit GitHub’s theme. The snake switches palettes with `<picture>`.

## Validation and maintenance

Run `python3 scripts/validate_profile.py` to check SVG XML, required files, image alt text, local references, image safety, and Python syntax. Run `python3 scripts/validate_profile.py --network` to check remote URLs after the first workflow has published `output`. Actual GitHub rendering and a successful Actions run remain the final checks.

Verify desktop and mobile widths, light and dark themes, contact targets, and generated image dates after changing the README. Review the intentionally pinned Actions commit hashes when upgrading dependencies. If renaming the GitHub account, replace all `Mezbah143` references and the portfolio URL; the workflow reads the repository owner automatically.

## Credits

- Original header, cards, SQL icon, badges, and layout: custom artwork for this profile.
- Technology icons: [Devicon](https://github.com/devicons/devicon), downloaded from the upstream `master` branch on November 11, 2026. MIT license retained at `assets/icons/LICENSE.devicon`. GitHub icon fill adjusted for visibility on both themes. Brand names and marks belong to their respective owners.
- Snake generator: [Platane/snk](https://github.com/Platane/snk), pinned to the verified `v3` commit.
- Checkout: [actions/checkout](https://github.com/actions/checkout), pinned to the verified `v4` commit.
- Optional view counter: [Komarev/github-profile-views-counter](https://github.com/antonkomarev/github-profile-views-counter).
