# Governance — AI-Native Cyber Resilience Architecture

This document defines how the project is governed, how decisions are made, and how external organizations and individuals can contribute.

## Project Steward

**NeevNaav** is the project steward and maintains the vision, roadmap, and quality standards.

## Roles

### Maintainer
- Approve or reject contributions
- Set technical direction and roadmap
- Manage releases and versioning
- Enforce code of conduct

### Contributor
- Submit pull requests with bug fixes, features, or documentation
- Participate in code reviews
- Follow the contribution guidelines in `CONTRIBUTING.md`

### Collaborator (External Organization)
- An organization that contributes significant, ongoing development
- May have dedicated branches or subdirectories with prior agreement
- Must sign the DCO (Developer Certificate of Origin) for all contributions

## Decision-Making

- **Day-to-day decisions**: Made by maintainers
- **Architecture decisions**: Documented as ADRs in `architecture/decision-log/`
- **Major changes** (API breaks, new components, license changes): Require maintainer consensus and a minimum 2-week comment period on a GitHub Discussion or Issue

## Contribution Process

1. External contributors fork the repository and submit PRs
2. All PRs must pass CI (lint, test, security scan)
3. All commits must be signed off (`git commit -s`) per the DCO
4. At least one maintainer review required before merging
5. No direct pushes to `master` — all changes via PR

## Community

- Open to contributions from individuals and organizations
- All participants must follow the `CODE_OF_CONDUCT.md`
- Disputes are escalated to the project maintainer

## License

All contributions are accepted under the terms of the MIT License as specified in `LICENSE`.
