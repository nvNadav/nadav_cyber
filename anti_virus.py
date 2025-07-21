from pathlib import Path
import requests



apikey="656fcf35264ae798249564de8477e9fd727078c19eb7ce45ee80a01c35ede2eb"
url = "https://www.virustotal.com/api/v3/files"
headers = {
    "accept": "application/json",
    "X-apikey": apikey
}


def traverse_files(file_path):
    path=Path(file_path).iterdir()
    for path in path:
        if path.is_dir(): # folder
            flag = traverse_files(path)
        else: # file
            flag = scan_file(path)

        if not flag: # virus
            return False
        
    return True


def scan_file(path):
    file_url = upload_file(path)
    status = is_malicious(file_url)
    return status
    
    



def upload_file(path): # returns the url of the file 

    file = { "file": (path, open(path, "rb")) }
    response  = requests.post(url, files=file, headers=headers)

    if (response.status_code==200):
        file_url = response.json()["data"]["links"]["self"]
        print ("upload works")
        return file_url
    else:
        print ( "An Error occurred: " + response.json()["error"]["message"])

def is_malicious(file_url): # checks if the file is malicious or suspicious

    response = requests.get(file_url,headers=headers)
    
    if (response.status_code==200):
        stats = response.json()["data"]["attributes"]["stats"]
        print ("analysis works")
        if (stats["malicious"]==0 and stats["suspicious"]==0):
            return True    
        return False
    
    else:
        print ( "An Error occurred: " + response.json()["error"]["message"])

path = r'c:\Users\USER\Downloads\Sharat.zip'
#traverse_files(path)

upload_file(path)