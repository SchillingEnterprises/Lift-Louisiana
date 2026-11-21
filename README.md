# Lift Louisiana

A responsive, static showcase for Lift Louisiana, focused on community, advocacy, and reproductive health care access in Louisiana. The site is built with HTML, CSS, and a small amount of vanilla JavaScript; it has no application backend, build step, or package installation.

## Run locally

Use Python's built-in static file server from the repository root:

```bash
python -m http.server 8000
```

Open [http://localhost:8000](http://localhost:8000). You can also open `index.html` directly, though a local server more closely matches how the site is hosted.

## Project structure

| Path | Purpose |
| --- | --- |
| `index.html` | Main showcase page and its content |
| `404.html` | Branded not-found page for GitHub Pages |
| `robots.txt` | Crawler policy for the public site |
| `src/styles/css/overview.css` | Responsive layout, visual design, and motion preferences |
| `src/js/site.js` | Progressive enhancement for the mobile navigation |
| `src/img/` | Site imagery and favicon |
| `tests/` | Dependency-free Python and Node.js regression tests |
| `.github/workflows/pages.yml` | Validation and GitHub Pages deployment |

## Validate changes

The checks require Python 3 and Node.js. No packages need to be installed.

```bash
python -m unittest discover -s tests -v
node --test tests/navigation.test.cjs
node --check src/js/site.js
```

The Python tests check required pages, local HTML and stylesheet references, and accessibility and link-safety basics. The Node.js tests exercise the mobile navigation's open, close, Escape, focus-restoration, and link-activation behavior.

## Publish

GitHub Actions runs the validation checks for pull requests targeting `master`. A push to `master` runs the checks and, if they pass, deploys the site to GitHub Pages. The workflow stages only `index.html`, `404.html`, `robots.txt`, and `src/`; documentation, tests, and repository configuration are not published.

For the first deployment, set the repository's **Pages build and deployment** source to **GitHub Actions**. The workflow's deployment job is restricted to pushes to `master`; manually running the workflow performs validation but does not deploy.

## Editing guidance

- Keep the page static and dependency-free unless a project requirement calls for otherwise.
- Keep local links and asset paths relative so the site works on GitHub Pages.
- Provide useful alternative text for informative images; mark decorative imagery as decorative.
- Preserve keyboard navigation, visible focus, reduced-motion support, and the mobile menu's no-JavaScript fallback.
- For links opening a new tab, retain `rel="noopener noreferrer"`.
- Check permissions and accuracy before publishing third-party content, imagery, or external destinations.

## Privacy and security

The site has no first-party analytics, forms, accounts, or backend. The main page loads its typefaces from Google Fonts, and following external links contacts the linked service; those third parties may receive normal connection data from a visitor's browser. See [SECURITY.md](SECURITY.md) for security and reporting guidance.

## License

See [LICENSE](LICENSE) for the repository's license terms.
