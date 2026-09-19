# Blackbox Security Benchmarks

Containerized blackbox challenges for evaluating autonomous security agents across three benchmark families:

- **CTF**: reconnaissance, exploitation, privilege escalation, and lateral movement.
- **Chain**: multi-stage vulnerability discovery and dependency-gated exploitation.
- **Crypto**: cryptographic vulnerability exploitation and CBOM generation.

## Repository layout

```text
benchmarks/ctf/       CTF tiers and focused evasion challenges
benchmarks/chain/     Multi-stage vulnerability-chain scenarios
benchmarks/crypto/    CBOM auditing and cryptographic exploit targets
runners/              Evaluation entry points
docs/                 Execution and isolation guidance
```

Select an experiment in the [benchmark catalog](docs/benchmark-catalog.md). Follow [running locally](docs/running-locally.md) for dependencies, isolation, logs, and cleanup. Restricted operator material is described in [operator documentation](docs/operator-documentation.md).

## Running a challenge

Each containerized challenge is self-contained. Start one from its directory:

```bash
cd benchmarks/ctf/tier1_easy
docker compose up -d
```

Run the corresponding evaluator from the repository root:

```bash
python3 runners/run_ctf.py --tier easy --target-host 127.0.0.1
python3 runners/run_chain.py --scenario scenario1 --target-host 127.0.0.1
python3 runners/run_crypto.py --mode exploit --target aes_gcm --target-host 127.0.0.1
```

Set `OPENAI_API_KEY` or pass `--api-key` when connecting an evaluator to an inference endpoint. Never commit production credentials, agent logs, or benchmark result artifacts.

## Fair evaluation

Run agents in disposable, isolated containers or VMs. The agent should receive only the task prompt, target address, inference endpoint, and an empty workspace. It must not receive this repository, challenge source, ground-truth flags, evaluator code, host mounts, or the Docker socket. See [Fair Blackbox Evaluation Guidelines](docs/evaluation-guidelines.md).

## Safety

These services are intentionally vulnerable. Run them only in an isolated Docker or VM network that you control. They are for authorized testing and research only.

## License

Released under the MIT License. See [LICENSE](LICENSE).
