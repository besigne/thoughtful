import os

def clean_up():
  files = [filename for filename in os.listdir("./") if "geckodriver-" in filename]
  for file in files:
    os.remove(file)