from ExtendendSelenium import ExtendedSelenium
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
      self.selenium.click_element(f'//a[contains(text(), "{item}")]')
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
        if not self.selenium.find_element(f"//*[@class=\"{remove}\"]"):
          continue
        
        self.selenium.find_element(f"//*[@class=\"{remove}\"]")
        js_string = f"var element = document.getElementsByClassName(\"{remove}\")[0];element.remove();"
        self.selenium.execute_javascript(js_string)
      
      
      for remove in removables:
        if not self.selenium.find_element(f"//*[@class=\"{remove}\"]"):
          continue
        self.div_block_remover()
        
    except ElementNotFound:
      pass