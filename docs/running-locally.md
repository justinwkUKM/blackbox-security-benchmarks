# Running locally

Run commands from the repository root unless a challenge guide says otherwise. Use Python 3.10+, Docker Engine with Compose v2, and curl. The CTF, Chain, and crypto runners require an installed `opencode` executable on PATH, an accessible inference endpoint, and a compatible model. The CBOM runner also checks for OpenCode and imports the Python `openai` package even though it calls the endpoint through curl.

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install openai
docker compose version
opencode --version
python3 runners/run_ctf.py --help
```

The runners use different OpenCode flags (`--auto` for CTF/Chain and `--format json` for crypto). Check compatibility with your installed OpenCode before an experiment and record its version. Container dependencies are installed by Dockerfiles; network access is needed during builds.

## Start and check a target

```bash
cd benchmarks/ctf/tier1_easy
docker compose up -d --build
docker compose ps
curl --fail --show-error --max-time 10 http://127.0.0.1:8080/
docker compose logs --tail 100
```

Use each guide's endpoint and port. All current web targets use HTTP, including port 8443. An HTTP error alone is not readiness: inspect the expected status and response body. Crypto readiness requires successful JSON from the sample/token endpoint. The negative control and CBOM use their own procedures.

## Run an evaluator

From the repository root in a separately provisioned disposable evaluation VM, configure the inference credentials and run, for example:

```bash
python3 runners/run_ctf.py --tier easy --target-host 127.0.0.1 --vllm-ip 127.0.0.1 --vllm-port 8000 --model openai/Antanom
```

Replace addresses and model with the experiment's values; `127.0.0.1` refers to the machine running the command. Supply `OPENAI_API_KEY` through your secret configuration. The runners provide CLI overrides for endpoint, model and timeout.

A temporary working directory is not a security sandbox. Current runners launch an agent subprocess with inherited host permissions and environment. Operators must enforce filesystem and network boundaries externally; do not run a fair blackbox trial with the agent able to read this checkout. Public guides are researcher material, not automatically the agent prompt.

Compose publishes ports on host interfaces by default. Use a disposable VM with inbound access limited to the evaluator/agent and controlled outbound access. Scenario 1 and CTF backends have internal networks, but public bridges and single-container scenarios do not automatically block egress. Fixed container names and subnets can conflict; run trials on separate hosts or sequentially.

## Logs and results

| Runner | Output directory | Main artifacts |
|---|---|---|
| CTF | `/tmp/antanom_ctf_eval_<tier>_<timestamp>/` | `agent_execution.log`, `benchmark_result.json` |
| Chain | `/tmp/antanom_chainbench_<scenario>_<timestamp>/` | `chain_agent.log`, `chainbench_result.json` |
| Crypto exploitation | `/tmp/antanom_crypto_exploit_<target>_<timestamp>/` | `agent_execution.log`, `benchmark_result.json` |
| CBOM | `/tmp/antanom_cbom_eval_<timestamp>/` | `cbom_agent.log`, `cbom.json`, request JSON; score printed to stdout |

These directories currently share the subprocess workspace; they are not protected logging channels. Collect and protect results externally for fair evaluation. Reports may contain ground truth; request files may contain the supplied source. Target logs are available through `docker compose logs` until teardown.

## Reset and cleanup

In the selected Compose directory:

```bash
docker compose down -v --remove-orphans
docker compose ps -a
docker compose up -d --build
```

After teardown, verify the challenge containers/networks are absent and the former endpoint is unreachable. After recreation, repeat readiness checks and use a fresh agent workspace. Rebuilding restores image contents; it does not rotate embedded credentials or flags. Teardown does not erase host result directories: archive needed results privately, then remove only the specific per-run workspace. Stop the negative-control foreground process with Ctrl-C; CBOM has no service to stop.
