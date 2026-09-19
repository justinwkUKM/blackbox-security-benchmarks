# CBOM generation

## Overview

Track A inventories cryptographic assets in the supplied sample fintech repository.

## Capability under evaluation

Asset discovery and representation of algorithms, certificates, protocols, parameters, weaknesses, and detection context.

## Difficulty and estimated duration

Medium; about 30 minutes (planning estimate).

## Starting conditions

Input is an ordinary source directory containing source files, certificates and configuration. Supply only `sample_fintech_repo`, excluding ground truth and evaluator code. The current runner stages a copy, sends readable file contents to the model, then extracts its response into `cbom.json`; it does not run an autonomous file-writing agent for this track.

## Target topology

```text
Sample source → model context → cbom.json → operator scorer
```

## Exposed ports

None for the target. Model generation requires a separately configured inference endpoint.

## Objective

Return CycloneDX 1.6 JSON with cryptographic components and `cryptoProperties`, saved as `cbom.json`. Requested categories include symmetric and asymmetric algorithms, hashes, PRNGs, MACs, certificates, and TLS/SSL protocols.

## Milestones and scoring categories

This is a continuous inventory score, not binary flag capture; metadata's one milestone denotes the submitted artifact. Precision measures the proportion of reported assets matched by the scorer; recall measures matched reports relative to expected asset count, and F1 combines them. Property accuracy currently checks primitive equality only. Key size, mode, weaknesses, source context, and CycloneDX schema validity are requested but are not scored or validated by this implementation. The reported spec version is read from the submission.

Duplicate reports can inflate recall; interpret results with this limitation and inspect submissions for duplication. Detailed matching rules belong in operator documentation.

## Running locally

For model generation, follow [setup](../../../docs/running-locally.md), then run `python3 runners/run_crypto.py --mode cbom` from the repository root with your endpoint/model overrides.

A model-free scoring smoke test uses the empty sample submission:

```bash
python3 benchmarks/crypto/cbom/evaluate_cbom.py --submission docs/examples/cbom.json --ground-truth benchmarks/crypto/cbom/ground_truth_cbom.json
```

The sample intentionally lists no assets, so precision, recall, F1 and property accuracy are zero. It tests invocation and JSON handling, not inventory quality or schema conformance.

## Health checks

Confirm readable input files, a JSON output containing a `components` array, and a completed scoring report. JSON parsing alone does not validate CycloneDX 1.6.

## Reset and cleanup

Stage a fresh input directory for every trial. Archive logs and output privately before removing that specific temporary directory. No Compose target exists.

## Safety notes

Keep ground truth private. See [setup and log locations](../../../docs/running-locally.md); CBOM request files contain the source supplied to the model.

## Related evaluator

`python3 runners/run_crypto.py --mode cbom` generates and scores; `evaluate_cbom.py` scores an existing submission without OpenCode or an inference service.
