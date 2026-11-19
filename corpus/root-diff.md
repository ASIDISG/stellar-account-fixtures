# Network Root Documents Diff Analysis

This document provides a structural, field-by-field comparative analysis between
the two network root documents in the corpus:
- `corpus/root-public.json` (Stellar Public Network / Mainnet)
- `corpus/root-testnet.json` (Stellar Testnet)

## 1. Context and Contract Purpose

Per `SCHEMA.md:133` (Section 6, Root documents), every network referenced by a
fixture must provide a corresponding `corpus/root-<network>.json` document.
The primary purpose of root documents is to establish cryptographic ground truth
and network identity for fixtures captured from that network.

Both root documents in this corpus were captured using Horizon endpoints running
identical software builds, allowing an exact distinction between immutable network
identity constants and volatile runtime properties.

## 2. Server and Build Parity

Both files share identical software and protocol version descriptors:

| Field | Public Value | Testnet Value | Classification |
|---|---|---|---|
| `horizon_version` | `30.0.0-b3ff4119cc99ebcc8048334f5ec64e78c16d1666` | `30.0.0-b3ff4119cc99ebcc8048334f5ec64e78c16d1666` | Identical build |
| `core_version` | `stellar-core 30.0.0 (0e49751aa9ddf892302cca02cea7f3f5d97df9f1)` | `stellar-core 30.0.0 (0e49751aa9ddf892302cca02cea7f3f5d97df9f1)` | Identical build |
| `current_protocol_version` | `29` | `29` | Protocol agreement |
| `supported_protocol_version` | `29` | `29` | Protocol agreement |
| `core_supported_protocol_version` | `29` | `29` | Protocol agreement |

Because server and protocol versions are identical across both networks, differences
between the files reflect genuine network distinctions rather than software release skew.

## 3. Essential Network Identity Fields

Network identity fields define the domain boundary of the network and remain constant
across ledgers:

### `network_passphrase`
- **Public**: `Public Global Stellar Network ; September 2015` (`corpus/root-public.json:103`)
- **Testnet**: `Test SDF Network ; September 2015` (`corpus/root-testnet.json:107`)

The network passphrase is the cryptographic seed for all transaction signature
verification on Stellar. A transaction signed for `Test SDF Network ; September 2015`
is mathematically invalid on `Public Global Stellar Network ; September 2015`.
`validate.py:370` checks this field strictly to ensure no fixture silently originates
from the wrong network.

### `_links` URL Templates
- **Public**: All URI templates use the base authority `https://horizon.stellar.org/`
  (for example, `"account": {"href": "https://horizon.stellar.org/accounts/{account_id}"}`).
- **Testnet**: All URI templates use the base authority `https://horizon-testnet.stellar.org/`
  (for example, `"account": {"href": "https://horizon-testnet.stellar.org/accounts/{account_id}"}`).

## 4. Volatile Runtime Ledger State

These fields advance with ledger closure and record the instantaneous network state
at the capture timestamp:

| Field | Public Value (`corpus/root-public.json`) | Testnet Value (`corpus/root-testnet.json`) | Description |
|---|---|---|---|
| `history_latest_ledger` | `65282680` (line 99) | `5535136` (line 103) | Head sequence of history archive |
| `history_latest_ledger_closed_at` | `2026-11-03T09:50:39Z` (line 100) | `2026-11-03T09:48:40Z` (line 104) | Wall-clock timestamp of head ledger |
| `core_latest_ledger` | `65282680` (line 95) | `5535136` (line 99) | Latest sequence processed by core |
| `ingest_latest_ledger` | `65282680` (line 98) | `5535136` (line 102) | Latest sequence processed by Horizon ingestion |
| `history_elder_ledger` | `65218708` (line 94) | `5534241` (line 98) | Oldest retained sequence in history archive window |

## 5. Architectural Conclusions for Consumers

1. **Network Identity Separation**: Consumers validating fixtures must rely on
   `network_passphrase` and base URL authorities, never on ledger sequences or version numbers.
2. **Deterministic Validation**: Fixture sidecars declare `network = "public"` or
   `network = "testnet"`. The validator loads the corresponding root file and verifies
   that the passphrase matches the fixed constant in `validate.NETWORKS`.
3. **Capture Isolation**: When capture tooling refreshes a root document during fixture
   capture, only volatile ledger sequences advance while the network passphrase remains invariant.
