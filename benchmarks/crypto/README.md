# Crypto benchmarks

CryptoBench has two complementary tracks:

| Track | Target | What it measures |
|---|---|---|
| A: CBOM generation | [`cbom`](cbom/README.md) | Discovery and accurate CycloneDX 1.6 representation of cryptographic assets |
| B: Cryptographic exploitation | [`exploitation`](exploitation/README.md) | Mathematical reasoning against nonce-reuse and padding-oracle behavior |

Track A uses a supplied repository copy and produces `cbom.json`; it has no network port. Track B runs isolated HTTP services on ports 8091 and 8092. Start a target from its directory with `docker compose up -d --build`, check the documented endpoint, and tear it down with `docker compose down -v --remove-orphans`. From the repository root, use `python3 runners/run_crypto.py --mode cbom` or `python3 runners/run_crypto.py --mode exploit --target aes_gcm --target-host 127.0.0.1`.

Do not expose the intentionally vulnerable services to an untrusted network. Exact vulnerable parameters, expected plaintexts, and proof values are operator-only.
