# Design

## Context

See `proposal.md` for motivation and `specs/petfinder-home/spec.md` for observable behavior. The current Reflex application has only `/`, `/login`, and `/register`. Login is a local placeholder and does not establish a session. The only Xano tables are `user` and `event_log`; available endpoint snapshots cover authentication, password reset, and event logs. The documented snapshot is not deployed to the only known live branch. No pet/ONG images or catalog API contracts are available.

## Goals / Non-Goals

**Goals:**
- Add a navigable, responsive Home shell using the existing Reflex app and documented design tokens.
- Show accurate empty/unavailable states until real data contracts exist.
- Keep all current routes and local user changes intact.

**Non-Goals:**
- Create or modify Xano tables/endpoints, query live production, or add sample records.
- Implement authentication/session storage, logout, profile persistence, quiz scoring, favorites, adoption requests, or image hosting.
- Add frontend dependencies or replace the existing login and registration pages.

## Decisions

### Keep the Home sections in one Reflex page state

Use `/home` with a Reflex state variable for the selected section and a mobile navigation toggle. This keeps navigation responsive without introducing routes that have no detail pages or backend behavior. Alternatives considered: adding separate routes for each menu item, which would create destinations without independent content or existing route conventions.

### Make the unavailable backend explicit in the UI

Do not create a generic service that guesses `/pets`, `/ngos`, or other endpoint paths. Render shared empty-state panels explaining that each capability awaits a confirmed Xano contract. Search/filter inputs and account actions that cannot act on real data are omitted or disabled with a clear explanation. Alternatives considered: mock/demo records or speculative endpoint calls, both of which could be mistaken for real platform data.

### Do not infer an authenticated identity

Show a guest label and a link to `/login`. Do not show user-specific greetings, profile details, or a logout action, because the existing login does not establish a session and the client has no verified token lifecycle. Keep `/` and `/login` unchanged. The `/home` page contains no private data and remains a public preview until authentication is implemented.

### Reuse the current visual system and avoid surrogate pet photos

Use the documented purple palette, system font, spacing, borders, radii, and shadows from `docs/design-system.md`. A gradient banner may use a library icon as decoration, but it will not depict that as a real registered animal. No local pet images exist, and the existing login's external photo is not a catalog record. Alternatives considered: reuse the login background photo, which could imply an available pet record without provenance.

## Risks / Trade-offs

- [The page cannot show real pets, ONGs, quiz results, or account data until API/session contracts exist] → Show specific empty states and document each backend dependency.
- [The Home is public because there is no verifiable login session to enforce] → Display no private data or mutation controls; add access control only with a real session implementation.
- [No image fields or local pet assets are available] → Avoid pet cards and use a neutral branded banner.

## Migration Plan

No backend migration is included. Add `/home` to the existing Reflex app. Rollback consists of removing the new route/module while preserving `/`, `/login`, and `/register`.

## Open Questions

- The Xano owner must provide a compatible development branch and verified base URL before catalog, NGO, quiz, profile, adoption, favorite, or logout integrations can be designed and tested.
- Confirm whether public catalog browsing should remain available without login when real endpoints are introduced.
