from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import base64, httplib2
#from oauth2client.client import SignedJwtAssertionCredentials

#driver = webdriver.Chrome(executable_path="google-chrome")

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

#id = "1065790532830-quumamu7ickfeovgdvetli17rh8p3jm5.apps.googleusercontent.com"
#key = base64.b64decode('COaV9QUlO1OdqtjMiUS6xEI8')

#credentials = SignedJwtAssertionCredentials(id, key, scope='https://www.googleapis.com/auth/drive')
#credentials.authorize(httplib2.Http())

#gauth = GoogleAuth()
#gauth.credentials = credentials

drive = GoogleDrive(gauth)

folder_id = '1G9F4oq5H3ZsTR74RdJSXnLKY7kN_CzHn'
f = drive.CreateFile({'title': 'mygfg.pdf',
                      'mimeType': 'application/pdf',
                      'parents': [{'kind': 'drive#fileLink', 'id':folder_id}]})
f.SetContentFile('/home/andsilva/repo/webscraping/selenium/mygfg.pdf')
f.Upload()

