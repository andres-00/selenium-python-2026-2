from pathlib import Path

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

from features.driver_factory import create_driver


def before_scenario(context, scenario):
    """Crea el navegador y los Page Objects compartidos por el escenario."""
    context.driver = create_driver()
    context.login_page = LoginPage(context.driver)
    context.inventory_page = InventoryPage(context.driver)


def after_scenario(context, scenario):
    """Guarda evidencia si falla el escenario y cierra siempre el navegador."""
    driver = getattr(context, "driver", None)
    if driver is None:
        return

    try:
        if scenario.status in {"failed", "error", "hook_error", "cleanup_error"}:
            screenshots_dir = Path(__file__).resolve().parents[1] / "screenshots"
            screenshots_dir.mkdir(exist_ok=True)
            filename = "".join(
                character if character.isalnum() or character in "-_" else "_"
                for character in scenario.name
            )
            driver.save_screenshot(str(screenshots_dir / f"{filename}.png"))
    finally:
        driver.quit()
