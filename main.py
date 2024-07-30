from seleniumbase import Driver
from PgTikTok import TikTokClass

driver = Driver(uc=True)
driver.maximize_window()


tk_instance = TikTokClass()
tk_instance.login_to_tiktok(driver)
tk_instance.automate_content_planner(driver)
