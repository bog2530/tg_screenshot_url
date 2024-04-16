"""
Утилита для создания скриншота сайта
"""

from playwright.async_api import async_playwright


async def screenshot(url: str) -> tuple[str, str, bytes]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=100)
        page = await browser.new_page()
        await page.goto(url)
        screenshot_bytes = await page.screenshot(scale="css")
        title = await page.title()
        await browser.close()
    return title, page.url, screenshot_bytes
