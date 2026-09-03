#!/usr/bin/env python3

"""
Demo of Selenium WebDriver browser automation with Python, teaching the
locator strategies and interaction patterns for Google Maps.

IMPORTANT — DO NOT RUN THIS AGAINST LIVE google.com/maps:
Google's Terms of Service restrict automated querying of its services.
This code exists to teach syntax and interaction *patterns* — it is not
meant to be executed against the live Google Maps. Do not run this script,
do not install its dependencies in order to run it, and do not point it at
a real Google Maps page. See README.md and AGENTS.md for the full caution.

Please see the file README.md for more information.

## Tracking

  * Package: demo-selenium-python-for-google-maps
  * Version: 1.0.0
  * Created: 2026-09-03T00:00:00Z
  * Updated: 2026-09-03T00:00:00Z
  * License: GPL-2.0-or-greater or for custom license contact us
  * Contact: Joel Parker Henderson (joel@joelparkerhenderson.com)
"""

import re
import sys

# Import Selenium WebDriver parts.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Import chromedriver options that you can set as you wish.
from selenium.webdriver.chrome.options import Options

# Google Maps embeds the current view as "@lat,lng,zoomz" in the URL, e.g.
# https://www.google.com/maps/place/Cardiff/@51.4816546,-3.1791934,12z/...
# We use this to read back the zoom level, because the map itself renders
# mostly to a <canvas> (or WebGL) element that ordinary element locators
# cannot inspect.
ZOOM_PATTERN = re.compile(r'@(-?[\d.]+),(-?[\d.]+),(\d+(?:\.\d+)?)z')


def get_lat_lng_zoom(url: str):
    """Parse the "@lat,lng,zoomz" segment out of a Google Maps URL."""
    match = ZOOM_PATTERN.search(url)
    if not match:
        raise ValueError(f'Could not find "@lat,lng,zoomz" in URL: {url}')
    lat, lng, zoom = match.groups()
    return float(lat), float(lng), float(zoom)


def demo() -> None:
    """Teach the locator strategies and assertions for a Google Maps
    walkthrough. Do not call this against the live Google Maps — see the
    module docstring and README.md."""

    options = Options()
    options.add_argument('--verbose')  # Enable verbose logging.
    options.add_argument('--disable-notifications')  # Disable notifications such as popups.
    options.add_experimental_option(
        "prefs",
        {"profile.default_content_setting_values.cookies": 2},  # Reject cookies.
    )

    # Initialize the driver. Choose other browsers as you wish.
    driver = webdriver.Chrome(options=options)

    try:

        ###
        # Step 1: Load Google Maps, then verify the page title mentions
        # Google Maps.
        ###

        driver.get('https://www.google.com/maps')

        title = driver.title
        print(f'Page title: "{title}"')
        assert 'Google Maps' in title, \
            f'Expected page title to contain "Google Maps", got "{title}"'
        print('✅ Page title contains "Google Maps".')

        ###
        # Step 2: Search for a place, then verify the URL contains it.
        #
        # Most of the map itself renders to a <canvas> element (or WebGL),
        # so you generally cannot "find" a street or a pin the way you find
        # a paragraph of text. But the UI chrome around the canvas —
        # search box, zoom buttons, layers menu — uses stable accessible
        # aria-label attributes, which change far less often than
        # generated or hashed CSS class names do. So we locate the search
        # box by its accessible name.
        ###

        query = 'Cardiff'
        search_box = driver.find_element(By.CSS_SELECTOR, '[aria-label="Search Google Maps"]')
        search_box.send_keys(query + Keys.RETURN)

        url_after_search = driver.current_url
        print(f'URL after search: "{url_after_search}"')
        assert query in url_after_search, \
            f'Expected URL to contain "{query}", got "{url_after_search}"'
        print('✅ URL contains the searched place.')

        ###
        # Step 3: Click zoom in, then verify the URL's embedded zoom level
        # increased. This is the honest way to assert a canvas-rendered
        # map actually zoomed: read the state back out of the URL rather
        # than trying to inspect canvas pixels.
        ###

        _, _, zoom_before = get_lat_lng_zoom(url_after_search)
        driver.find_element(By.CSS_SELECTOR, '[aria-label="Zoom in"]').click()

        url_after_zoom = driver.current_url
        print(f'URL after zoom in: "{url_after_zoom}"')
        _, _, zoom_after = get_lat_lng_zoom(url_after_zoom)
        print(f'Zoom before: {zoom_before}, zoom after: {zoom_after}')
        assert zoom_after > zoom_before, \
            f'Expected zoom to increase from {zoom_before}, got {zoom_after}'
        print('✅ URL zoom parameter increased.')

        print('\nAll checks passed. 🎉')

    finally:
        driver.quit()


def main() -> None:
    """Main entry point with error handling.

    NON-NEGOTIABLE: never call demo() against the live Google Maps. See the
    module docstring, README.md, and AGENTS.md."""
    try:
        demo()
    except Exception as err:
        print(f'Fatal error: {err}', file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
