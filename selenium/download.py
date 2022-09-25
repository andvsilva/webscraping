
# Import Module
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from fpdf import FPDF

# save FPDF() class into
# a variable pdf
pdf = FPDF()

# Add a page
pdf.add_page()
  
# set style and size of font
# that you want in the pdf
pdf.set_font("Arial", size = 15)

  
# Open Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
  
# Open URL
driver.get('http://demo.automationtesting.in/FileDownload.html')
  
# Enter text
driver.find_element(By.ID, 'textbox').send_keys("Hello @andvsilva Nice to meet you!")

# Generate Text File
driver.find_element(By.ID, 'createTxt').click()

  
# Click on Download Button
driver.find_element(By.ID, 'link-to-download').click()

time.sleep(3)

# open the text file in read mode
f = open("/home/andsilva/Downloads/info.txt", "r")

# insert the texts in pdf
for x in f:
    pdf.cell(200, 10, txt = x, ln = 1, align = 'C')
  
# save the pdf with name .pdf
pdf.output("/home/andsilva/Downloads/mygfg.pdf") 