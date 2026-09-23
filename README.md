# iGoBeat song library

Public overseas mirror for iGoBeat. Contains song catalog, covers, announcements and versioned Release assets. No app source code or credentials.

Catalog base: `https://raw.githubusercontent.com/GloobyFF/iGoBeat/main/`

485 songs: Pro / HD / 2+3. VIP access is verified by the app; public URLs are not DRM.

## Updates

The maintainer publishes a complete validated source catalog. New/changed music files receive immutable Release URLs. Unchanged files are reused. Covers use content hashes. A single git commit switches the catalog after all uploads have passed SHA-256 checks. Previous pages and Release assets remain available for in-flight downloads and rollback.

To roll back metadata, revert the publication commit on `main` (do not force-push). Existing media need not be reuploaded. Use an explicit package revision increase for replacing audio/charts; preserve song UUIDs and VIP assignments.
