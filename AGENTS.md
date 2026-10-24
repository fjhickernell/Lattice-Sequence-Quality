# Lattice Sequence Quality

## Checkpoint publication to GitHub and Overleaf

Fred requested on October 24, 2026 that Checkpoints publish this repository
to both GitHub and Overleaf. This applies to `Checkpoint`,
`Checkpoint <message>`, and both Express Checkpoint variants.

Follow the global Checkpoint review, handoff, validation, and commit rules.
After committing the intended changes, run the shared bridge from this
repository's root:

```sh
python3 "$HOME/Documents/SharedConfigs/bin/sync-overleaf.py" \
  "$PWD" Lattice-Sequence-Quality
```

The bridge uses `SharedConfigs/settings/overleaf-sync.json`, reconciles
compatible committed changes, and pushes GitHub `origin/main` followed by
the configured Overleaf `main`. This is authorized as part of each
Checkpoint; no separate approval is needed to publish to Overleaf.

Report a Checkpoint fully published only after the bridge verifies that
both remote tips match the local commit. If a conflict, authentication
failure, or rejected push occurs, preserve successful earlier work and
report which publication remains incomplete. Do not force-push or bypass
the bridge's clean-tree and branch checks. It requires local `main` with
upstream `origin/main`; do not change branches automatically to satisfy it.

This rule applies only to Lattice-Sequence-Quality. It does not authorize
running `sync-active.sh`, `git-repo-sync.sh`, or synchronizing the other
repositories in the Lattice and Kronecker project during a Checkpoint.
