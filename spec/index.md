# Spec: Demo Selenium Python for Google Maps

## Summary

This repo is a beginner-friendly walkthrough of Selenium WebDriver browser
automation in Python, teaching the locator strategies and assertions for
Google Maps. `src/demo.py` must never be executed against the live Google
Maps — see the caution below and in `README.md` / `AGENTS.md`.

## Scope

This spec covers only the three checks implemented in `src/demo.py`. It
does not cover unrelated Google Maps features, other browsers, or other
Google products.

## ⚠️ Non-negotiable: do not run this against live Google Maps

[Google's Terms of Service](https://www.google.com/policies/terms/)
restrict automated querying of its services. This code teaches syntax and
interaction *patterns*; it is not meant to be run repeatedly, or at all,
against the live Google Maps. Do not install dependencies to execute it, do
not run it, and do not point it at a real Google Maps page.

## Principles and rules

* The demo uses the `selenium` package's Chrome driver directly (via
  `webdriver.Chrome(options=options)`), not a wrapper or test framework.
* Expected strings and selectors must be matched exactly as written below
  and in the source.
* Most of the map renders to `<canvas>`/WebGL, so locators target the
  accessible `aria-label`s of the surrounding UI chrome, and the zoom
  assertion reads the map's own embedded `@lat,lng,zoomz` URL state rather
  than inspecting canvas pixels.
* If the code (`src/demo.py`) and this file ever disagree, that is a defect
  in one of them; fix it before doing anything else.

## Detail

1. **Page title check**
   * Navigate to: `https://www.google.com/maps`
   * Get the page title (`driver.title`).
   * Assert the title contains the substring: `Google Maps`

2. **Search check**
   * Find the search box by
     `By.CSS_SELECTOR, '[aria-label="Search Google Maps"]'`.
     * Note: this accessible-name locator is preferred over generated or
       hashed CSS class names, which change on every Maps deploy.
   * Send keys: `'Cardiff' + Keys.RETURN`
   * Get the resulting URL (`driver.current_url`).
   * Assert the URL contains the substring: `Cardiff`

3. **Zoom check**
   * Parse `(lat, lng, zoom)` out of the URL's `@lat,lng,zoomz` segment
     before clicking, via the regex `@(-?[\d.]+),(-?[\d.]+),(\d+(?:\.\d+)?)z`.
   * Click zoom in via
     `By.CSS_SELECTOR, '[aria-label="Zoom in"]'`.
   * Parse `(lat, lng, zoom)` out of the resulting URL the same way.
   * Assert the new zoom value is greater than the value before the click.

## Acceptance criteria

* All 3 checks above are correct Selenium/Python code that would pass if
  ever run against a live Google Maps session — but they must not actually
  be executed against `google.com/maps` as part of routine repo
  maintenance, CI, or agent work.

## Related topics

* [../README.md](../README.md)
* [../AGENTS.md](../AGENTS.md)

## Sources

* <https://testingexamples.github.io/examples/google-maps/>
