"""Creación portable de ChromeDriver para Chrome y navegadores Chromium."""

import os
import shutil
import sys
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def _existing_path(candidate):
    path = Path(candidate).expanduser()
    if path.is_file():
        return path.resolve()
    return None


def _usable_driver(path):
    return path if os.access(path, os.X_OK) or path.suffix.lower() == ".exe" else None


def _windows_candidates():
    candidates = []
    for variable in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA"):
        root = os.environ.get(variable)
        if root:
            candidates.extend(
                (
                    Path(root) / "Google" / "Chrome" / "Application" / "chrome.exe",
                    Path(root)
                    / "BraveSoftware"
                    / "Brave-Browser"
                    / "Application"
                    / "brave.exe",
                )
            )
    return candidates


def _browser_candidates():
    if sys.platform.startswith("linux"):
        return (
            ("chrome", ("google-chrome", "google-chrome-stable", "chromium")),
            ("brave", ("brave", "brave-browser", "/opt/brave-bin/brave", "/usr/bin/brave")),
        )
    if sys.platform == "darwin":
        return (
            (
                "chrome",
                ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",),
            ),
            (
                "brave",
                ("/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",),
            ),
        )
    if sys.platform.startswith("win"):
        return (
            ("chrome", tuple(_windows_candidates()[::2])),
            ("brave", tuple(_windows_candidates()[1::2])),
        )
    return ()


def _find_browser():
    explicit_path = os.environ.get("BROWSER_PATH")
    if explicit_path:
        path = _existing_path(explicit_path)
        if path:
            return path, "chrome" if "chrome" in path.name.lower() else "brave"
        print(f"WARNING: BROWSER_PATH no existe o no es un archivo: {explicit_path}")

    forced_browser = os.environ.get("BROWSER", "").strip().lower()
    if forced_browser and forced_browser not in {"chrome", "brave"}:
        print("WARNING: BROWSER debe ser 'chrome' o 'brave'; se usará autodetección.")
        forced_browser = ""

    for browser_name, candidates in _browser_candidates():
        if forced_browser and browser_name != forced_browser:
            continue
        for candidate in candidates:
            path = _existing_path(shutil.which(candidate) or candidate)
            if path:
                return path, browser_name
    return None, forced_browser or "chrome"


def _driver_path():
    configured = os.environ.get("CHROMEDRIVER_PATH")
    if configured:
        path = _existing_path(configured)
        path = _usable_driver(path) if path else None
        if path:
            return path
        print(f"WARNING: CHROMEDRIVER_PATH no existe o no es un archivo: {configured}")

    root = Path(__file__).resolve().parents[1]
    for filename in ("chromedriver", "chromedriver.exe"):
        path = root / filename
        if path.is_file() and (os.access(path, os.X_OK) or path.suffix.lower() == ".exe"):
            return path.resolve()
    return None


def _options(binary):
    options = Options()
    if binary:
        options.binary_location = str(binary)
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=en-US")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    if os.environ.get("HEADLESS") == "1":
        options.add_argument("--headless=new")
    if os.environ.get("NO_SANDBOX") == "1":
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    return options


def create_driver():
    """Crea un driver local y usa Selenium Manager si el local no funciona."""
    binary, browser_name = _find_browser()
    options = _options(binary)
    local_driver = _driver_path()

    if local_driver:
        try:
            driver = webdriver.Chrome(service=Service(str(local_driver)), options=options)
            print(f"[WebDriver] navegador={browser_name} driver={local_driver}")
            return driver
        except (SessionNotCreatedException, WebDriverException) as error:
            print(
                "WARNING: el ChromeDriver local no pudo iniciar el navegador "
                f"({error.__class__.__name__}); se intentará Selenium Manager."
            )

    try:
        driver = webdriver.Chrome(options=options)
    except WebDriverException as error:
        raise RuntimeError(
            "No fue posible iniciar Chrome/Brave con ChromeDriver local ni Selenium Manager."
        ) from error
    print(f"[WebDriver] navegador={browser_name} driver=Selenium Manager")
    return driver
