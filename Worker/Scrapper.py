from ExtendendSelenium import ExtendedSelenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from SeleniumLibrary.errors import ElementNotFound
from RPA.Robocorp.WorkItems import WorkItems
from Worker.Writer import Writer
from Worker.utils import clean_up

def load_work_items():
  items = WorkItems()
  return items.get_input_work_item().payload


class Scrapper:
  
  def __init__(self):
    self.work_item = load_work_items()
    self.selenium = ExtendedSelenium()
    self.selenium.open_site("https://apnews.com")
  
  def run(self):
    self.category_select()
    self.search_on_searchbar()
    clean_up()
    
  def search_on_searchbar(self):
    self.selenium.find_element(locator='class:SearchOverlay-search-button').click()
    input = self.selenium.find_element(locator='class:SearchOverlay-search-input')
    input.send_keys(self.work_item['search'])
    input.send_keys(Keys.RETURN)

  def category_select(self):
    for item in self.work_item["category"]:
      self.div_block_remover()
      navbar = self.selenium.find_element(locator="class:Page-header-navigation")
      item = self.selenium.find_element(f'//a[contains(text(), "{item}")]', parent=navbar)
      WebDriverWait(self.selenium, 1000)
      item.click()
      payload = self.collector()
      Writer(item, payload)
    
  def collector(self):
    parent = self.selenium.find_element("//div[@class=\"PageList-items\"]")
    items = self.selenium.find_elements(locator="class:PageList-items-item", parent=parent)
    payload = []
    
    for item in items:
      try:
        self.div_block_remover()
        title = self.selenium.find_element(locator="class:PagePromo-title", parent=item).text
        description = self.selenium.find_element(locator="class:PagePromoContentIcons-text", parent=item).text
        image = self.selenium.find_element(locator="class:Image", parent=item).get_attribute("src")
      except ElementNotFound:
        return ""
        
      payload.append({"title": title, "description": description, "image": image})
    
    return payload
  
  def div_block_remover(self):
    try:
        removables = ["onetrust-pc-dark-filter ot-fade-in", "ot-dpd-desc", "onetrust-pc-btn-handler"]
        for remove in removables:
            js_string = f"var elements = document.querySelectorAll('.{remove}'); elements.forEach(function(element) {{ element.remove(); }});"
            self.selenium.execute_javascript(js_string)
    except Exception as e:
        print(f"An error occurred: {e}")