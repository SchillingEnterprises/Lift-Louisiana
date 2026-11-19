# Lift Louisiana — responsive project showcase

This repository contains a static, responsive project page for Lift Louisiana.

## Run locally

Open `index.html` in a browser or serve the repository root with any static file server, for example:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`.

## Quality checks

Run the dependency-free asset and accessibility smoke tests:

```bash
python -m unittest discover -s tests -v
```

GitHub Actions runs these checks for pull requests and deploys the site to GitHub Pages after changes merge to `master`. The deployment workflow publishes only the approved root files (`index.html`, `404.html`, and `robots.txt`) plus `src/`; tests, workflow files, and repository documentation are not copied into the published artifact. In repository settings, select **GitHub Actions** as the Pages build source if it is not already selected.

## Project notes

- Original local imagery and social links are preserved.
- The page is static and does not contain a backend or collect visitor data.
- A branded `404.html` page handles unknown routes on GitHub Pages; `robots.txt` permits indexing of the public showcase.
- External destinations remain external and open in a new tab.
- No paid services or runtime dependencies are required.

## Security

See [SECURITY.md](SECURITY.md) for this repository's security, privacy, and responsible-use guidance.
