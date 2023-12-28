from bs4 import BeautifulSoup
import requests
from datetime import datetime

class NUMB_DAYS:
    WEEK_1 = 7
    MONTH_1 = 31
    MONTH_6 = 183
    YEAR_1 = 365
    YEAR_3 = 1095
    YEAR_5 = 1825
    
def listOftupples_to_list(tupple_list):
    return map(list, zip(*tupple_list))

def ListOfList_to_string(input_list):
    output_string = ""
    for item in input_list:
        # Extrahiere Datum und Dezimalzahl aus der Liste
        date, float_value = item
        timestamp_str = date.strftime('%Y-%m-%d %H:%M:%S')
        # Entferne die Uhrzeit aus dem Datum
        date = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        
        # Runde die Dezimalzahl auf zwei Nachkommastellen auf
        float_value = round(float(float_value), 2)
        
        float_value = round(float(float_value), 2)

        float_str = str(float_value)
        output_string += date + '\t  ' + float_str + ' €' + '\n' + '\n'
    return output_string

def get_first_twoStrings(text):
    strings = text.split()
    if len(strings) >= 2:
        return " ".join(strings[:2])
    else:
        return strings
    
def get_page_headers(urls):
    headers = []
    
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            if soup.title:
                header = soup.title.text
            else:
                print("Kein Header gefunden")
            headers.append(header)
        except Exception as e:
            print("Keine Verbindung zur Website")
            
    return headers