from pathlib import Path
import requests

apikey="656fcf35264ae798249564de8477e9fd727078c19eb7ce45ee80a01c35ede2eb" 
url = "https://www.virustotal.com/api/v3/files" 
headers = { 
    "accept": "application/json",
    "X-apikey": apikey
}

def traverse_files(folder_path): 
    """
    Recursively checks all files in a folder and its subfolders.
    Returns True if all files are safe, otherwise False.
    """
    path=Path(folder_path).iterdir()
    
    for path in path:
        if path.is_dir(): 
            # Recursively scan subfolder
            flag = traverse_files(path)
        else: 
            # Scan the file
            flag = scan_file(path)  

        if not flag: 
            # Malicious file found
            return False
    
    # All files scanned are safe
    return True 


def scan_file(path):
    """
    Uploads a file and checks if it's malicious.
    Returns True if safe, otherwise False.
    """
    file_url = upload_file(path)
    if not file_url:
        return False
    status = is_malicious(file_url)
    return status

def upload_file(path): 
    """
    Uploads the file to VirusTotal and returns its unique scan URL.
    """

    file = { "file": (path.name, open(path, "rb")) } 
    response  = requests.post(url, files=file, headers=headers)

    if (response.status_code==200): 
        # Extract file scan result URL
        file_url = response.json()["data"]["links"]["self"] 
        return file_url
    else:
        # API error handling
        print("An error occurred: " + response.json().get("error", {}).get("message", "Unknown error"))
        return None

def is_malicious(file_url): 
    """
    Queries VirusTotal for the file's scan result.
    Returns False if file is malicious or suspicious, otherwise True.
    """
    response = requests.get(file_url,headers=headers)
    
    if (response.status_code==200):
        stats = response.json()["data"]["attributes"]["stats"]

        # Consider safe if neither malicious nor suspicious
        if (stats["malicious"]==0 and stats["suspicious"]==0):
            return True    
        
        # Flag as malicious/suspicious
        return False
    else:
        # API error handling
        print("An error occurred: " + response.json().get("error", {}).get("message", "Unknown error"))

path = r'c:\Users\USER\Documents\tempo'

if traverse_files(path):
    print ("No malicious/suspicious files found in path!")
else:
    print ("Found a malicious/suspicious file in Path :(")