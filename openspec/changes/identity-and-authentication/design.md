# Design

## Context

See `proposal.md` for motivation and `specs/identity-and-authentication/spec.md` for the behavior contract. The Reflex login is still a local demo and does not call Xano. A read-only pull of workspace `151970`, its only branch `v1` (live), confirmed the deployed `user` table has `id`, `created_at`, `name`, `email`, `password`, `role` (`admin/member`) and `password_reset`; it has a unique email index but no `account_type`, contact, adopter, or ONG profile fields. The remote event table is `event_log` (singular) and references `user`. The remote authentication and reset endpoints are generic quick-start implementations and send full user records to the logger; the remote `logs/user/my_events` endpoint returns complete event rows, including metadata. The workspace reports `Allow Push: false`; no remote writes or record exports were performed.

The checked-in Xano snapshot is a proposed divergent state: it adds `account_type`, contact/profile fields, and CPF/CNPJ indexes. The local schema now preserves `role` separately from `account_type`; local signup assigns new customer accounts the least-privilege role `member`. Local authentication/reset endpoints are not deployed to remote `v1`. The local logger now applies an allowlist (`account_type` only), and the local event-history endpoint masks metadata; neither change affects already stored remote events until manually deployed. See `docs/xano-authentication-setup.md` for the verified comparison and manual migration plan.

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

Use the existing authenticated `user` identity as the shared email/password authentication record. Represent customer account type with exactly `ADOTANTE` or `ONG`; keep it distinct from legacy `role` values `admin/member`, which remain for authorization. New customer accounts receive `member`; an ONG is never assigned `admin` automatically. Preserve existing records and do not infer account type from role or silently rewrite/delete users.

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
- [Logger allowlist currently retains only `account_type`] → Require an explicit security review before adding other metadata keys; do not pass whole records or request/response objects.
- [Remote `my_events` returns stored metadata that may contain historical credentials] → Apply the local allowlisted event response in an approved development branch; assess old records separately without exposing or deleting them automatically.
- [Only live branch `v1` is available and CLI push is disabled] → Keep remote unchanged; ask the workspace owner to provide an approved development branch before applying snapshots.
- [Local auth endpoints require fields absent from remote `user`] → Do not connect the Reflex client to the current live contract; migrate and verify a development branch first.

## Migration Plan

1. Before implementation, inspect the target Xano workspace/branch, existing records, auth endpoints, role usage, and token behavior; confirm that it matches the versioned snapshot.
2. Document a non-destructive account-type and profile mapping for existing records. Do not infer adopter/ONG type or delete legacy data without an approved mapping.
3. Implement and validate schema and API changes in the appropriate Xano development branch, including backend uniqueness, ownership checks, safe event metadata, and logout invalidation.
4. Integrate and test Reflex registration, login, route handling, and logout against those backend contracts.
5. Roll back by restoring the prior Xano API/table definitions and Reflex version only after assessing any accounts or sessions created under the new model; preserve user data and do not use destructive rollback as a default.

## Open Questions

- The read-only workspace pull confirmed deployed schema/source files, but not production records, runtime behavior, or historical logs. Verify those separately in the approved development workspace before deployment.
- Confirm the exact accepted phone-number validation/normalization policy and CPF/CNPJ input normalization before implementation; the required validation and uniqueness behavior remain fixed by the spec.
- The API group base URL is absent from the repository. Obtain it from the workspace owner before configuring a Reflex client; do not infer the URL from the workspace ID.