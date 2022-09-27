
## Import Module
#import time
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.common.by import By
#
#from fpdf import FPDF
#
## save FPDF() class into
## a variable pdf
#pdf = FPDF()
#
## Add a page
#pdf.add_page()
#  
## set style and size of font
## that you want in the pdf
#pdf.set_font("Arial", size = 15)
#
#  
## Open Chrome
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#  
## Open URL
#driver.get('http://demo.automationtesting.in/FileDownload.html')
#  
## Enter text
#driver.find_element(By.ID, 'textbox').send_keys("Hello @andvsilva >>> Nice to meet you!")
#
## Generate Text File
#driver.find_element(By.ID, 'createTxt').click()
#
#  
## Click on Download Button
#driver.find_element(By.ID, 'link-to-download').click()
#
#time.sleep(3)
#
## open the text file in read mode
#f = open("/home/andsilva/Downloads/info.txt", "r")
#
## insert the texts in pdf
#for x in f:
#    pdf.cell(200, 10, txt = x, ln = 1, align = 'C')
#  
## save the pdf with name .pdf
#pdf.output("/home/andsilva/Downloads/mygfg.pdf")

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.

#drive = GoogleDrive(gauth)
#
#file1 = drive.CreateFile({'title': 'Hello.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
#file1.SetContentString('Hello World!') # Set content of the file from given string.
#file1.Upload()
#print(file1)
#
#drive.CreateFile({'id':file1['id']}).GetContentFile('Hello World!')

drive = GoogleDrive(gauth)

folder_id = '1G9F4oq5H3ZsTR74RdJSXnLKY7kN_CzHn'
f = drive.CreateFile({'title': 'mygfg.pdf',
                      'mimeType': 'application/pdf',
                      'parents': [{'kind': 'drive#fileLink', 'id':folder_id}]})
f.SetContentFile('/home/andsilva/Desktop/works/mygfg.pdf')
f.Upload()