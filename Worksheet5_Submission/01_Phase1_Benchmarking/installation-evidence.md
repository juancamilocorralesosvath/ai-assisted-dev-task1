# BMad 6.10 → 6.12 Installation Evidence

**Date:** 2026-09-14  
**Workspace:** `C:\Users\joshe\Desktop\SDD\ai-assisted-dev-task1`  
**IDE target:** Codex

## Required sequence

The professor's requested sequence was performed in the same workspace so that WDS would be installed while it was still selectable, then preserved by the upgrade.

```powershell
npx --yes bmad-method@6.10.0 install --yes --directory . --modules bmm,wds,tea --tools codex
npx --yes bmad-method@6.12.0 install --yes --directory . --action quick-update
npx --yes bmad-method@6.12.0 status
```

## Checkpoint after 6.10 installation

The installer reported:

- BMad Core: `6.10.0`
- BMM: `6.10.0`
- WDS: `v0.4.3`
- TEA: `v1.26.0`
- Codex integration: 71 generated skills

This checkpoint confirms that WDS was present before the upgrade.

## Upgrade result

The 6.12 quick update reported:

- Core: `6.10.0 → 6.12.0`
- BMM: `6.10.0 → 6.12.0`
- WDS: `v0.4.3` preserved
- TEA: `v1.26.0` preserved
- Codex integration: 75 generated skills
- 21 deprecated compatibility shims retained

## Final status

```text
Version:       6.12.0
Location:      C:\Users\joshe\Desktop\SDD\ai-assisted-dev-task1\_bmad
Built-in Modules
  core         6.12.0 ✓
  bmm          6.12.0 ✓
External Modules (Official)
  wds          v0.4.3 ✓
  tea          v1.26.0 ✓
All modules are up to date
```

The generated manifest at `_bmad/_config/manifest.yaml` independently records BMad `6.12.0`, BMM `6.12.0`, WDS `v0.4.3`, TEA `v1.26.0`, and the Codex IDE integration.

## Phase 1 commands now available

The generated Codex skills include the required review workflows:

- `bmad-prd` for PRD validation
- `bmad-review` for multi-lens review
- WDS workflows and the Freya UX agent
- BMad Method and TEA workflows

## Conclusion

The requested installation path is complete. The workspace is on BMad `6.12.0` and WDS remains available at `v0.4.3`.
