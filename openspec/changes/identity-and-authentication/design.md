# Design

## Context

See `proposal.md` for motivation and `specs/identity-and-authentication/spec.md` for the behavior contract. The Reflex app is currently the initial scaffold. The versioned Xano files contain one authenticated `user` table with a unique email index, password field, and `role` values `admin/member`, plus generic signup, login, current-user, and password-reset endpoints. Signup/login and password reset pass user records into event-log metadata. The available Xano knowledge query returned no workspace items; no live workspace schema or data was confirmed.

## Goals / Non-Goals

**Goals:**

- Reuse Xano's existing authentication primitives where compatible while preserving adopter and ONG as exactly two customer account types.
- Keep account-type and ownership enforcement in Xano; Reflex route guards provide navigation behavior only.
- Establish a session lifecycle that supports invalidation on logout and safe handling of authentication data.

**Non-Goals:**

- Implement pets, matching, adoption requests, or multi-user NGO membership.
- Decide or execute a physical database migration in this proposal.
- Replace Reflex, Xano, or the existing authentication subsystem without a reviewed compatibility reason.

## Decisions

### Reuse the Xano authentication identity and separate account type from legacy role

Use the existing authenticated `user` identity as the shared email/password authentication record, subject to checking the actual Xano branch before implementation. Represent customer account type with exactly `ADOTANTE` or `ONG`; do not treat the scaffold's `admin/member` values as customer account types. Preserve existing records and role behavior until their use and any required mapping are known; do not silently rewrite or delete them.

Alternatives considered: create separate authentication tables per account type, which duplicates credential handling and complicates global email uniqueness; reinterpret `admin/member` as the two customer types, which would conflate existing authorization roles with account identity and cannot represent the required values.

### Keep type-specific data distinct from shared credentials

Retain the conceptual distinction between a person/adopter and an NGO from `docs/domain-model.md`. The proposed physical direction is one adopter profile per adopter identity and one NGO record per ONG identity, with CPF unique among adopter profiles, CNPJ unique among NGO records, and a one-to-one NGO/account association. Keep globally unique email on the shared authentication identity. Confirm Xano's supported uniqueness and relationship constraints on the actual branch before applying schema changes; if a required guarantee cannot be enforced there, document a safe alternative for review before implementation.

Alternatives considered: put every adopter and NGO field in the generic auth table, which mixes mutually exclusive profile data and weakens the conceptual separation; independent auth tables, which make global email uniqueness harder to guarantee.

### Enforce authorization at the Xano boundary

Protected Xano operations derive the account identity from authenticated context, validate account type, and scope data access to that identity. Do not accept a caller-supplied owner ID as authority. Reflex redirects and hidden controls improve navigation but are not authorization controls. This establishes a reusable ownership rule for later capabilities without implementing pet or adoption-request access now.

Alternative considered: frontend-only route checks, rejected because direct API calls would bypass them.

### Use backend-controlled session validity for logout

The existing snapshot creates expiring Xano auth tokens but has no logout endpoint. The available Xano security reference documents server-side session records and token revocation patterns, but does not identify a ready-made logout primitive in this scaffold. The implementation should use a Xano-supported server-validated session/revocation mechanism so logout invalidates protected access; verify the exact token/session integration before designing its physical representation. Do not claim that deleting a token from Reflex alone invalidates it at the backend.

Alternative considered: only discard the client-held token, rejected because a copied token could remain usable until expiration and would not meet the backend invalidation requirement.

### Exclude secrets from authentication event metadata

Replace whole-user event metadata with an explicit allowlist of non-sensitive event fields. Audit signup, login, password reset, and other authentication paths, and ensure auth responses include only the fields needed by the caller. The snapshot's login query explicitly selects `password` and sends the user record to the event logger; do not rely on undocumented masking behavior.

Alternative considered: assume Xano automatically masks password fields in event metadata, rejected because the checked snapshot and available workspace knowledge do not establish that guarantee.

## Risks / Trade-offs

- [Legacy `role` data may be in use in the live Xano branch] → Inspect deployed records and endpoints before migration; preserve current behavior and require an explicit mapping plan before any destructive change.
- [Xano's exact unique-index, relationship, or session-revocation behavior may differ from the local snapshot] → Validate against the connected workspace and document alternatives before applying schema or API changes.
- [Phone and identifier normalization policy is not fully specified] → Define and document accepted input/normalization during implementation without weakening required validation or backend uniqueness.
- [Existing authentication logs may contain credential fields] → Audit current event data/retention and prevent further sensitive metadata from being written; assess handling of prior records before any cleanup.

## Migration Plan

1. Before implementation, inspect the target Xano workspace/branch, existing records, auth endpoints, role usage, and token behavior; confirm that it matches the versioned snapshot.
2. Document a non-destructive account-type and profile mapping for existing records. Do not infer adopter/ONG type or delete legacy data without an approved mapping.
3. Implement and validate schema and API changes in the appropriate Xano development branch, including backend uniqueness, ownership checks, safe event metadata, and logout invalidation.
4. Integrate and test Reflex registration, login, route handling, and logout against those backend contracts.
5. Roll back by restoring the prior Xano API/table definitions and Reflex version only after assessing any accounts or sessions created under the new model; preserve user data and do not use destructive rollback as a default.

## Open Questions

- The MCP workspace knowledge list is empty and no live Xano branch/data was available in the inspected project context. The implementation must identify the target workspace/branch and verify that the local `.xs` snapshot reflects it before planning a migration.
- Confirm the exact accepted phone-number validation/normalization policy and CPF/CNPJ input normalization before implementation; the required validation and uniqueness behavior remain fixed by the spec.