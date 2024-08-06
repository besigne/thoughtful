import os
import requests
from RPA.Excel.Files import Files


class Writer:
  
  def __init__(self, category: str, payload: list):
    self.path_verifier(category)
    
    headers = ['title', 'description', 'image']
    path = f"./output/{category}/data.xlsx"
    excel = Files()
    
    excel.create_workbook(f'./output/{category}/data.xlsx', fmt="xlsx")
    excel.save_workbook()
    excel.open_workbook(f'./output/{category}/data.xlsx')
    
    rows = [[item['title'], item['description'], item['image']] for item in payload]
    
    excel.append_rows_to_worksheet([headers] + rows)
    
    excel.save_workbook(path)
    excel.close_workbook()
    
    self.image_downloader(payload, category)
    
  def path_verifier(self, category):
    if not os.path.exists(f"./output/{category}"):
      os.mkdir(f"./output/{category}")
    if not os.path.exists(f"./output/{category}/images"):
      os.mkdir(f"./output/{category}/images")
      
  def image_downloader(self, payload, category):
    images = [item['image'] for item in payload]
    for index, image in enumerate(images):
      if not image:
        continue
      with open(f'./output/{category}/images/{index}.jpg', 'wb') as file:
        file.write(requests.get(image).content)