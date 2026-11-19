# Account Data Entries

This document specifies the format, decoding rules, and protocol role of account
data entries present in the Stellar account fixtures corpus.

## 1. Summary of Corpus Specimen

Stellar accounts store arbitrary key-value state in their ledger entry as a mapping
from entry name (up to 64 bytes) to a binary payload (up to 64 bytes), returned by
Horizon as base64-encoded strings inside the `data` object.

Among the nine captured accounts in this corpus, `fixtures/coordinator-data-entry`
is the only fixture that possesses a non-empty `data` map. All other eight captured
fixtures contain empty or absent data maps.

Reference: `fixtures/coordinator-data-entry/account.json:68`.

## 2. Key and Value Specification

The single data entry in `fixtures/coordinator-data-entry` is:

- **Key**: `config.multisig.coordinator`
- **Base64 Payload**: `djEubXVsdGlzaWcuc2F0b3NoaXBheS5pbw==`
- **Decoded String**: `v1.multisig.satoshipay.io`

### Binary Representation and Mathematical Decoding

The base64 string `djEubXVsdGlzaWcuc2F0b3NoaXBheS5pbw==` comprises 36 characters
including two `=` padding characters, representing 25 decoded bytes:

1. `djEu` -> `0x76, 0x31, 0x2e` (`"v1."`)
2. `bXVs` -> `0x6d, 0x75, 0x6c` (`"mul"`)
3. `dGlz` -> `0x74, 0x69, 0x73` (`"tis"`)
4. `aWcu` -> `0x69, 0x67, 0x2e` (`"ig."`)
5. `c2F0` -> `0x73, 0x61, 0x74` (`"sat"`)
6. `b3No` -> `0x6f, 0x73, 0x68` (`"osh"`)
7. `aXBh` -> `0x69, 0x70, 0x61` (`"ipa"`)
8. `eS5p` -> `0x79, 0x2e, 0x69` (`"y.i"`)
9. `bw==` -> `0x6f` (`"o"`)

Concatenating the 25 output bytes yields the exact UTF-8 ASCII string:
`v1.multisig.satoshipay.io`

## 3. Protocol Role in Coordinator Discovery

In Stellar multisig workflows, signers must locate the coordination server that
collects transaction signatures before submission. Storing `config.multisig.coordinator`
as an on-chain account data entry allows client wallets and signing tools to discover
the coordinator host dynamically by inspecting the account's Horizon resource.

The host `v1.multisig.satoshipay.io` represents an endpoint running a multisig
coordination API (such as SatoshiPay multisig coordination service). This pattern
binds coordination discovery directly to the account without requiring out-of-band
configuration.

## 4. Schema Derivation and Validation

`SCHEMA.md:107` defines the vocabulary labels for data entries:

- `has_data`: Derived when the `data` object is non-empty.
- `no_data`: Derived when the `data` object is empty or absent.

In `validate.py:179`, `shapes_of` derives this property programmatically:

```python
found.add("has_data" if account.get("data") else "no_data")
```

Because `fixtures/coordinator-data-entry` contains a dictionary with one entry,
`account.get("data")` evaluates to truthy and emits `has_data`. Every other fixture
in the corpus evaluates to falsy and emits `no_data`.
