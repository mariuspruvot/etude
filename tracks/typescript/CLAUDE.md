# TypeScript track — tutor notes

Target TypeScript 5.x with `strict` on. Treat plain JS as a subset — always teach typed.
Pull current TS/lib/runtime usage via Context7. React/Vue/Svelte and Node/Bun specifics are
on-demand extensions, not part of this core.

- Emphasize: `strict` mode, no `any`, discriminated unions + narrowing, structural typing,
  generics with constraints, ESM, typed async.
- Tooling the learner touches: `tsc`, `ts-node`/`tsx`, `vitest`, `package.json`/`tsconfig.json`.
- Solution files are learner-written; never write the solution file (the hook blocks it).
