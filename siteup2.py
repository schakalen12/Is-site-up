import sys
import time
import datetime
from lankar import urls

missingimports = False

try:
    from fake_useragent import UserAgent
except:
    print("Modulen 'fake_useragent' finns inte installerad. Installera med 'pip3 install fake_useragent'.")
    missingimports = True
try:
    import requests
except:
    print("Modulen 'requests' finns inte installerad. Installera med 'pip3 install requests'.")
    missingimports = True  
try:
    import colorama
except:
    print("Modulen 'colorama' finns inte installerad. Installera med 'pip3 install colorama'.")
    missingimports = True
    
if missingimports == True:
    sys.exit(1)

colorama.init()
ua = UserAgent()
headers = {'User-Agent': ua.random}
#Ignorera SSL-problem.
requests.packages.urllib3.disable_warnings()

def banner():
    print("*" * 76)
    print("*" + " " * 74 + "*")
    print("*" + " " * 18 + "Monitorering av Myndigheters Webbsidor" + " " * 18 + "*")
    print("*" + " " * 74 + "*")
    print("*" * 76)

def get_status_code(url):
    try:
        response = requests.get(url, headers=headers, verify=False)
        return response.status_code
    except requests.exceptions.SSLError:
        return ("An SSL error occurred. Certifikatsproblem")
    except requests.exceptions.ConnectionError:
        return("A Connection error occurred. Sidan kan inte nås.")
    except requests.exceptions.RequestException:
        return("An error occurred. Annat konstigt fel.")
    except:
        return ("N/A")

def get_status_message(status_code):
    if status_code == 200:
        return "OK!" 
    elif status_code == 404:
        return "Not Found." 
    elif status_code == 403:
        return "Forbidden. WAF?"
    elif status_code == 429:
        return "Too Many Requests - DDOS?"
    elif status_code == 502:
        return "Bad Gateway"
    elif status_code == 503:
        return "Service Unavaliable"
    elif status_code == 500:
        return "Internal Server Error"
    elif status_code == 504:
        return "Gateway Timeout"
    elif status_code == 524:
        return "A timeoout occurred"
    return None
    
def convert_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    seconds = round(seconds)
    minutes = round(minutes)
    hours = round(hours)
    if hours > 0:
        return f"{hours} timme, {minutes} minuter och {seconds} sekunder."
    elif minutes > 0:
        return f"{minutes} minuter och {seconds} sekunder."
    else:
        return f"{seconds} sekunder."

prev_status_codes = {}
start_times = {}
printed_200_flag = {}

banner()

while True:
    try:    
        for url in urls:
            status_code = get_status_code(url)
            hostname = urls[url]
            status_message = get_status_message(status_code)

            if hostname not in prev_status_codes:
                prev_status_codes[hostname] = status_code
                printed_200_flag[hostname] = False

            if status_code != prev_status_codes[hostname]:
                prev_status_codes[hostname] = status_code
                printed_200_flag[hostname] = True

            if status_code != 200:
                if hostname not in start_times:
                    start_times[hostname] = time.time()
                    elapsed_time = time.time() - start_times[hostname]
                    elapsed_time_minutes = elapsed_time / 60
                    if not status_message:
                        print(colorama.Fore.RED + f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {hostname.capitalize()} svarar inte. {status_code}") 
                        time.sleep(1)
                    elif status_message:
                        print (colorama.Fore.RED + f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {hostname.capitalize()} svarar inte.Statuskod: {status_code} - {status_message}")  
                        time.sleep(1)
            else:
                if printed_200_flag[hostname] == False:
                    print(colorama.Fore.GREEN + f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {hostname.capitalize()} {status_code} ({status_message})")
                    printed_200_flag[hostname] = True
                    time.sleep(1)
                if hostname in start_times:
                    start_time = start_times[hostname]
                    elapsed_time = time.time() - start_time
                    elapsed_time_minutes = elapsed_time / 60
                    print(colorama.Fore.YELLOW + f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {hostname.capitalize()} svarade inte under ca {convert_time(elapsed_time)}")
                    print(colorama.Fore.GREEN + f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {hostname.capitalize()} {status_code} ({status_message})")
                    del start_times[hostname]
                    time.sleep(1)
    except:
        print(colorama.Fore.RED + f"Skriptfel! Avslutar.")     
        sys.exit()       