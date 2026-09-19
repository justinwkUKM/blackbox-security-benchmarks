# Fair Blackbox Evaluation Guidelines

These guidelines define the minimum isolation and reproducibility requirements for evaluating an autonomous security agent against this benchmark suite.

## Evaluation roles

Keep these roles separate:

```text
Evaluator / grader
├── Starts and stops the target challenge
├── Provides the task prompt and target address
├── Collects agent output
└── Scores flags and milestones privately

Target environment
└── Intentionally vulnerable Docker services

Agent environment
└── Agent, tools, and an empty disposable workspace
```

The agent must never be given the benchmark repository, challenge source, evaluator scripts, ground-truth files, or a host filesystem mount.

## What the agent may access

The agent may receive:

- The benchmark task prompt.
- The target service address and exposed port.
- Its own empty temporary workspace.
- The inference endpoint required to run the model.
- Any tools explicitly required by the experiment, such as HTTP clients or a terminal.

The agent should not receive challenge names that reveal the intended exploit chain unless that is part of the experiment design.

## Required isolation

Run the agent in a disposable container or VM. At minimum, the container should use:

```bash
docker run --rm \
  --network <benchmark-network> \
  --read-only \
  --tmpfs /tmp \
  --tmpfs /workspace \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --pids-limit=256 \
  --memory=4g \
  --cpus=2 \
  --name benchmark-agent \
  benchmark-agent:latest
```

Do not use any of the following for a fair run:

```text
--privileged
--network host
The Docker socket (/var/run/docker.sock)
The benchmark repository as a volume mount
Host filesystem mounts
Unrestricted internet egress
```

If the model endpoint is hosted outside the benchmark network, expose only that endpoint through a controlled proxy or a second explicitly allowed network. Do not give the agent general outbound access.

## Network topology

The target services and agent may share a dedicated per-run Docker network. The evaluator and grader should remain outside that network except for the control and result channels they require.

Use a fresh network and fresh target containers for every run. Do not reuse containers, mutable volumes, or agent workspaces between runs. Current challenge flags and credentials are static assets and are reused by the supplied images; recreation does not rotate them.

The agent must be able to reach the target, but the target must not provide a route back to the evaluator host or the host network.

## Ground truth and scoring

Ground-truth flags, milestone definitions, and scoring code must remain in the evaluator environment. The agent must not be able to read them from:

- The mounted workspace.
- Environment variables.
- Command-line arguments.
- Process arguments or inherited file descriptors.
- Logs written into the agent container.

The grader should parse the agent's externally collected output after the run. For chain benchmarks, the current runner matches each proof independently and does not record capture order. Preserve timestamps in an external transcript if order is part of your experiment.

## Run lifecycle

For every evaluation:

1. Create a unique temporary run identifier.
2. Create a dedicated network and disposable workspace.
3. Start only the selected target challenge.
4. Health-check the target from the agent network.
5. Start the agent with a fixed timeout and resource limits.
6. Collect stdout, stderr, tool traces, exit status, and timestamps outside the agent workspace.
7. Score the result without exposing ground truth to the agent.
8. Stop and remove the agent, target containers, network, and temporary volumes.
9. Store only the final report and reproducibility metadata.

Do not use a successful run's containers or workspace as the starting point for another run.

## Reproducibility

Record at least:

- Git commit of this benchmark repository.
- Challenge family and challenge ID.
- Target image digests or Compose configuration.
- Agent image/model identifier.
- Prompt version.
- Timeout and resource limits.
- Target and inference endpoint configuration.
- Random seeds, if applicable.
- Final score and captured flags.

Never record API keys or other infrastructure credentials in reports.

## Safety

These challenges intentionally contain command injection, privilege-escalation, cryptographic, credential, and lateral-movement vulnerabilities. Run them only on isolated infrastructure that you control. Destroy environments after testing and do not expose challenge ports to the public internet.

## Pre-run checklist

- [ ] Agent has an empty workspace.
- [ ] No benchmark or evaluator files are mounted into the agent.
- [ ] No Docker socket or host network is available.
- [ ] Target is running on a fresh per-run network.
- [ ] Ground truth is outside the agent environment.
- [ ] Timeout and CPU/memory limits are configured.
- [ ] Logs are collected outside the agent workspace.
- [ ] Cleanup is automated and verified after the run.
