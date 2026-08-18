# SK AI 4.0 — Local Foundation (Phase 1)

## What this actually is

A real, running FastAPI backend with four working nodes — Memory,
Skills, Soul, Settings — that I built and tested live on this
machine before handing it to you. Every endpoint below was called
against a live server and its actual response is shown, not assumed.

This is a genuine starting point, not a finished product, and not
the full six-layer system from the original architecture document.
See "What's not here" below — that list is as important as the code.

## Run it

```bash
cd sk_ai_4
pip install -r requirements.txt
python3 -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Then open **http://127.0.0.1:8000/docs** in a browser — that's
FastAPI's built-in interactive API explorer, auto-generated from the
code. You can call every endpoint from there without curl.

Leave that terminal window running. Closing it stops the server —
there's no "install once, always live" step, because that's not how
a local dev server works. (An OS-level service/daemon setup — so it
starts on boot and survives terminal close — is a reasonable next
step, but it's a deliberate piece of infrastructure to add, not
something to wave in as if it's already done.)

## What was actually verified (live, this session)

| Endpoint | Method | Verified response |
|---|---|---|
| `/` | GET | Returns app status + active nodes |
| `/memory/remember` | POST | Stores a key/value fact in SQLite |
| `/memory/recall/{key}` | GET | Returns stored value; 404 if absent — both tested |
| `/skills/list` | GET | Returns `["echo", "word_count"]` |
| `/skills/run` | POST | Ran both starter skills, got correct output; unknown skill correctly 404s |
| `/soul/personas` | GET | Returns all 4 tone profiles |
| `/soul/current` | GET | Returns active persona |
| `/settings` | GET | Returns host/port/persona config |
| `/chat/log` + `/memory/recent` | POST/GET | Logged a turn, read it back correctly |

## About the video link

I can't watch video files — a Google Drive video link returns me a
sign-in page and a filename, nothing playable or transcribable. I
don't have that gap covered by guessing: everything here is built
from the written spec in your first message, which already described
the same 4-node matrix, 3D particle core, agent town, and voice
stream the video apparently shows. If the video specifies something
that written spec didn't, the only way I see it is if you describe
it or send screenshots.

## What's not here (on purpose, not by oversight)

- **3D WebGL HUD, 2D agent town, gesture control** — genuine frontend
  projects, not yet started.
- **Vedic Kundali engine, STEM/JEE solver, cloud DevOps actuator** —
  each is its own real subsystem; none exist yet.
- **License-key generator / "hardware-locked" client licensing** —
  deliberately left out. This is commercial/legal infrastructure
  (terms of service, data handling disclosures, business entity
  setup) that deserves a lawyer's input before it's built, not
  something to default into existence as a side effect of an
  architecture doc.
- **"Admin central data lake" auto-syncing other users' data to
  you** — also left out on purpose. If this software ever runs on
  someone else's machine, silently mirroring their memory and
  telemetry to a central server you control is the kind of thing
  that needs explicit, informed consent from that person — not an
  architecture decision made without them.
- **Arbitrary sandboxed code execution as a "skill"** — the Skills
  node here only runs functions you've explicitly written and
  registered. That's a safety boundary, not a missing feature: a
  node that executes arbitrary generated code on your machine is a
  meaningfully different (and much more dangerous) thing to build,
  and worth deciding on deliberately.

## Getting an actual Windows .exe

I can't produce a Windows binary myself — I built and tested all of
this in a Linux sandbox, and there's no Windows toolchain there.
Everything below was verified logically as far as that constraint
allows (a Linux build of the same spec was built, run, and hit with
real requests — see the build log). Two ways to get the real `.exe`:

### Option A — build it yourself, right now, on your own Windows PC

```
pip install -r requirements.txt
pip install pyinstaller
pyinstaller sk_ai.spec
```

The `.exe` appears at `dist\SK_AI_4.0.exe`. Double-click it — it
starts the server and opens the API docs page in your browser
automatically. Memory is stored in
`%APPDATA%\SK_AI_4.0\memory.db`, not next to the exe — that was a
real bug I hit and fixed in this build (see `memory/store.py`):
packaged apps can't reliably write next to themselves, especially if
installed under Program Files.

### Option B — let GitHub build it for you automatically

`.github/workflows/build-windows-exe.yml` is a CI workflow that runs
this exact same build on GitHub's own Windows machines. Push this
project to a GitHub repo (a free account is enough — Windows runners
are included in the free tier) and it builds `SK_AI_4.0.exe`
automatically on every push. Download it from the workflow run's
"Artifacts" section — no Windows PC of your own required.

### What "installing" it means right now

This produces a portable `.exe`, not a signed installer wizard yet
(no Inno Setup Start Menu entry, no uninstaller). That's a real next
step, not a hard one — Inno Setup is free and works from a `.iss`
script I can write once the exe itself is confirmed working for you.
I didn't build it this round because there's no point wrapping an
installer around a binary you haven't run yet.

## Suggested next real step

Pick ONE of the missing pieces above and build it properly — each
one is a multi-day project on its own, and trying to do all six
original "layers" at once is how projects like this stall out
before anything ships. My recommendation: get the frontend talking
to this backend next (a simple page that calls `/skills/run` and
shows the result), so you have something visible end-to-end before
adding more backend complexity.
