from robocorp import browser

class Worker():
  
  def __init__(self, url: str):
    self.url = url
    
  def open_browser(self):
    browser.configure(
      slowmo=1000
    )
    browser.goto(self.url)
    
  def click_search_icon(self):
    page = browser.page()
    page.locator("[class=\"site-nav__anchor site-nav__item--search-link\"]").click()
    
  def type_search_string(self):
    page = browser.page()
    page.get_by_placeholder("Search CBS News").fill("Olympics")
    