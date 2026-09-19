# Operator documentation

Public guides support experiment selection and setup. Detailed attack paths, credentials, proof values, grader rules and solution transcripts belong in a restricted operator package, withheld from evaluated agents.

The local `operator-docs/` directory is gitignored, not access-controlled or delivered in a clean checkout. Obtain the matching operator package from the benchmark maintainer through a restricted channel. No private repository or distribution endpoint has been configured here. Before distribution, the maintainer must put the package in access-controlled storage, record its matching benchmark revision, and grant access only to operators.

Do not rely on the directory name or Git ignore rules for secrecy. Source and runners in this repository already contain evaluator assets; the whole checkout must stay outside the agent's readable filesystem. Keep researcher documentation separate from the neutral prompt supplied for evaluation.

## Documentation maintenance

Treat `challenge.yaml` as the authoritative source for IDs, difficulty, planning durations and milestone counts, and Compose as the source of host port mappings. Durations are planning estimates, not measured completion times. Documentation tables are manually maintained; generation is not implemented.

Run `python3 scripts/validate_docs.py`. It checks existing metadata files, standard README headings, catalog presence, local links and a flag-pattern scan. It does not establish that every target has metadata, that README/catalog values match metadata, or that runtime commands work. Review target directories independently, compare every catalog row and README to metadata, inspect rendered guides, and run setup/readiness checks on a disposable host before a release. Public summaries must not include exact solutions or ground truth.

This documentation update does not change the validator, challenge implementations, or evaluators.
