import pytest


@pytest.mark.ui
@pytest.mark.smoke
def test_home_and_about_page(base_url: str) -> None:
    playwright = pytest.importorskip("playwright.sync_api")
    with playwright.sync_playwright() as browser_tool:
        browser = browser_tool.chromium.launch()
        page = browser.new_page()
        page.goto(base_url)
        assert page.title() == "QA Python Lab"
        assert page.get_by_role("heading", name="QA Python Lab").is_visible()
        page.get_by_role("link", name="About the lab").click()
        assert page.get_by_role("heading", name="About this lab").is_visible()
        browser.close()
