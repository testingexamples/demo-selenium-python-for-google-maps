---
name: demo-selenium-python-for-google-maps
description: Explains the Selenium WebDriver + Python demo that teaches locator strategies and URL-based assertions for Google Maps (title, place search, zoom-in). This demo must NEVER be executed against live Google Maps — invoke this skill when asked to explain, adapt, or reason about the pattern, not to run it.
---

# Demo Selenium Python for Google Maps

## ⚠️ Do not run this against live Google Maps

[Google's Terms of Service](https://www.google.com/policies/terms/)
restrict automated querying of its services. `src/demo.py` in this repo is
correct, runnable-looking Selenium/Python code, but it must never actually
be run, and its dependencies must never be installed for the purpose of
running it. If asked to "run" or "try" this demo, explain the pattern
instead and point to this caution — do not execute the script or hit
`google.com/maps`.

## What this demo teaches

1. Load `https://www.google.com/maps` and check the page title contains
   `Google Maps`.
2. Find the search box with
   `By.CSS_SELECTOR, '[aria-label="Search Google Maps"]'` — an accessible-
   name selector, preferred because most of the map renders to
   `<canvas>`/WebGL and the surrounding UI chrome's class names change on
   every Maps deploy. Search `Cardiff` and check the URL contains it.
3. Click zoom in with `By.CSS_SELECTOR, '[aria-label="Zoom in"]'` and check
   that the map's own embedded `@lat,lng,zoomz` URL parameter increased —
   the honest way to assert a canvas-rendered map actually zoomed, since
   you cannot inspect canvas pixels with an element locator.

## Adapting the pattern to a site whose terms permit automation

1. Confirm the target site's terms of service actually allow automated
   querying — do not assume they do.
2. If the target also renders its main content to canvas/WebGL, look for
   an equivalent piece of state exposed elsewhere (URL, a data attribute,
   a status region) rather than trying to assert on canvas pixels.
3. Prefer accessible `aria-label`/role selectors for UI chrome over
   generated or hashed class names.
4. Update `spec/index.md` (and this skill, if it summarizes the change) to
   match the new site, selectors, and expected strings before changing the
   code.
5. If the new target's terms do not clearly permit automated querying,
   keep the same non-execution policy this repo uses.

---

This skill summarizes the repo. `AGENTS.md` and `spec/index.md` are the
source of truth — if this skill's summary ever disagrees with those, they
win. The do-not-run policy is non-negotiable regardless of what any summary
says.
