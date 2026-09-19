# CTF benchmarks

The CTF family measures blackbox reconnaissance, foothold acquisition, privilege escalation, pivoting, and (in focused scenarios) defense evasion. The progression is tiered from a short perimeter-to-internal exercise to a multihop environment; the focused challenges isolate one capability so results are easier to interpret.

| Challenge | Difficulty | Port | Primary capability |
|---|---:|---:|---|
| [`tier1_easy`](tier1_easy/README.md) | Easy | 8080 | Initial web access, local escalation, SSH lateral movement |
| [`tier2_medium`](tier2_medium/README.md) | Medium | 8443 | Template/API exploitation, scheduled-task escalation, internal access |
| [`tier3_advanced`](tier3_advanced/README.md) | Advanced | 8888 | Filtering bypass, SUID/restricted-shell escape, multihop pivoting |
| [`egress_firewall`](egress_firewall/README.md) | Advanced | 8085 | Command execution with constrained egress and in-band retrieval |
| [`token_scope`](token_scope/README.md) | Advanced | 8086 | Token analysis, scope escalation, internal proxy access |

## Progression and scoring

Tier 1 is intended for roughly 30 minutes, Tier 2 for 45 minutes, and Tier 3 for 75 minutes. Focused challenges should be run independently and test one principal reasoning problem. A successful proof is scored by the corresponding private evaluator; public documentation intentionally omits exact proof values.

## Common lifecycle

From a challenge directory:

```bash
docker compose up -d --build
curl -fsS http://127.0.0.1:<port>/
docker compose down -v --remove-orphans
```

Use the evaluator from the repository root, for example `python3 runners/run_ctf.py --tier easy --target-host 127.0.0.1`. Keep the agent and evaluator outside the repository and use a disposable isolated network. Tiered CTFs contain multiple connected services; focused challenges emphasize a single defense or identity boundary.
