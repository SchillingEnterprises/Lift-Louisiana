# Security Policy

## Scope and data handling

Lift Louisiana is a static site hosted on GitHub Pages. It has no application backend, account system, form submissions, or first-party analytics. The main page requests fonts from Google Fonts; following off-site links contacts those external services, which may receive normal connection data such as a visitor's IP address.

The public repository and published site must be treated as public. Do not put credentials, private personal information, confidential partner data, or unpublished sensitive material in source files, assets, commit messages, or issues.

## Maintaining the site safely

- Review changes to external links, scripts, fonts, embeds, and other third-party services for their purpose and data handling.
- Verify that imagery, logos, text, and other third-party materials are accurate and authorized for publication.
- Keep secrets out of client-side code; anything shipped to a browser is public.
- If adding forms, analytics, or other data collection, document what is collected, why it is needed, where it goes, and how it is protected before enabling it.
- Preserve the static-site publication allowlist in `.github/workflows/pages.yml` so repository-only files are not deployed.

## Reporting a vulnerability

Please report suspected vulnerabilities privately through GitHub's private vulnerability reporting feature when it is available for this repository. If it is unavailable, contact the repository maintainers privately through an appropriate GitHub channel. Do not publish exploit details, personal information, or secrets in a public issue.

There is no guaranteed response or remediation timeframe. Include the affected page or file, the potential impact, and concise reproduction details; avoid accessing or disclosing data that is not yours.
