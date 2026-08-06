# Ingest

Ingest is the first step for every project. Its goal is not to summarize; its goal is to make the project readable.

Recommended flow:

1. Put source files under `workspace/projects/[Project Name]/materials/`.
2. Inventory every file: path, type, size, source, and whether it is readable.
3. Group materials into BP, Datapack, references, management interviews, expert interviews, and other materials.
4. Convert unreadable files when needed and keep converted text under `runs/` or a local cache.
5. Update `master.md` with material inventory, current stage, open questions, and next recommended action.

The Agent should never silently skip files. If a file cannot be read, record the reason.
