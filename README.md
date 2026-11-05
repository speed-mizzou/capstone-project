# capstone-project

SPEED — interactive quantum networking education platform.

## Layout

```
apps/web/          React 19 + TypeScript + Vite frontend (deployed to Firebase Hosting)
  src/lib/         Firebase client wiring (firebase.ts, auth.tsx, auth-context.ts)
functions/         Cloud Functions 2nd gen, Python 3.13
firebase.json      Hosting / Firestore / Functions / emulator config
firestore.rules    Firestore security rules
firestore.indexes.json
```

## First-time setup

1. **Create the Firebase project** (once, by one person) in the
   [Firebase console](https://console.firebase.google.com), then point this
   repo at it:

   ```sh
   firebase login
   firebase use --add        # replaces the placeholder in .firebaserc
   ```

   In the console, enable **Authentication** (Email/Password provider),
   **Firestore** (production mode, region `us-central1`), and **Hosting**.

2. **Frontend config.** Copy the example env file and fill it in from
   Project settings → General → Your apps → SDK setup and configuration:

   ```sh
   cp apps/web/.env.example apps/web/.env.local
   ```

   The app throws a descriptive error on startup if any of these are missing.

3. **Install dependencies.**

   ```sh
   npm run install:web
   npm run install:functions   # creates functions/venv with Python 3.13
   ```

## Day-to-day

```sh
npm run dev          # Vite dev server
npm run emulators    # Hosting :5050, Auth :9099, Firestore :8080, Functions :5001, UI :4000
npm run build        # type-check + production build to apps/web/dist
npm run lint
```

To run the frontend against the emulator suite instead of live Firebase, set
`VITE_USE_FIREBASE_EMULATORS=true` in `apps/web/.env.local`.

## Deploying

```sh
npm run deploy            # everything (hosting build runs automatically)
npm run deploy:hosting
npm run deploy:functions
npm run deploy:rules
```

## Notes

- Functions are pinned to the shape in the requirements doc: `us-central1`,
  2 vCPU, 1 GiB, 120 s timeout, concurrency 1, 0–3 instances. These are set
  once via `options.set_global_options` in [functions/main.py](functions/main.py).
- Hosting rewrites `/api/**` to the `api` function; everything else falls back
  to `index.html` for client-side routing.
- `firestore.rules` makes `lessons` and `challenges` world-readable, keeps all
  per-user data owner-only, and allows link-sharing a saved network by setting
  `visibility: "public"`.
