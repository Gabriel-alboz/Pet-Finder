# Tasks

## 1. Xano Discovery and Compatibility

- [ ] 1.1 Inspect the target Xano workspace/branch, current records, auth endpoints, `role` usage, event logs, and token/session behavior; update `design.md` with verified findings and a non-destructive migration decision, and verify the local snapshot comparison is documented before any schema/API change.
- [ ] 1.2 Confirm Xano support for backend-enforced email, CPF, and CNPJ uniqueness, one-to-one NGO/account association, field validation, and session invalidation; document any limitation and reviewed alternative in `design.md`, and verify each spec guarantee has a backend enforcement path before implementation.

## 2. Account Model and Registration

- [ ] 2.1 Implement the agreed account type and type-specific adopter/NGO data model in the Xano development branch, preserving existing data and role behavior; verify XanoScript/schema validation and one-to-one/unique constraints, and update the Xano schema documentation or snapshot.
- [ ] 2.2 Implement adopter and NGO registration with all required fields and backend validation, including email/CPF/CNPJ uniqueness, valid UF, date and phone policy, and no generated identifiers; verify successful and rejected registration cases against the backend and document accepted normalization rules.
- [ ] 2.3 Implement own-profile read/update operations with immutable account type, CPF, and CNPJ under ordinary profile editing; verify cross-account access and protected-field updates are rejected by backend tests.

## 3. Authentication and Backend Security

- [ ] 3.1 Adapt the shared Xano login/current-user flow to authenticate either account type and return only required safe account data; verify valid adopter/ONG logins, invalid credentials, and type identification using backend tests.

## 4. Reflex Account Experience

- [ ] 4.1 Implement Reflex registration flows for adopter and ONG with the required fields and backend error handling; verify both forms submit to the matching Xano flow and display validation failures without relying on frontend validation for enforcement.
- [ ] 4.2 Implement the shared Reflex login, account-type destination, and logout flow; verify both account types reach the correct private area and logout clears client state while the backend rejects the ended session.
- [ ] 4.3 Protect adopter and NGO private routes in Reflex as a navigation layer while retaining Xano authorization; verify direct unauthenticated navigation redirects or returns an appropriate response and run the Reflex compile check.

## 5. Integrated Verification

- [ ] 5.1 Verify the end-to-end account lifecycle for both types, global email uniqueness, CPF/CNPJ uniqueness, profile ownership, protected routes, and logout invalidation against the development Xano branch; record the test evidence and confirm no pet, match, adoption-request, or multi-user NGO features were introduced.