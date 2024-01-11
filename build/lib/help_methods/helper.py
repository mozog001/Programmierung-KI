from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta

# Enumeration für die Anzahl der Tage
class NUMB_DAYS:
    WEEK_1 = 7
    MONTH_1 = 31
    MONTH_6 = 183
    YEAR_1 = 365
    YEAR_3 = 1095
    YEAR_5 = 1825
    
def listOftupples_to_list(tupple_list):
    """
    Funktion: Konvertiert eine Liste von Tupeln in eine Liste.
    param:
        - tupple_list: Liste von Tupeln.
    return:
        - Liste von Listen.
    """
    if len(tupple_list) >= 2:
        return map(list, zip(*tupple_list))
    else:
        return(list(tupple_list))

def ListOfList_to_string(input_list):
    """
    Funktion: Konvertiert eine Liste von Listen in einen formatierten String.
    param:
        - input_list: Liste von Listen, wobei jede Liste ein Datum und eine Dezimalzahl enthält.
    return:
        - Formatierter String, der Datum und Dezimalzahl enthält.
    """
    output_string = ""
    for item in input_list:
        # Extrahiere Datum und Dezimalzahl aus der Liste
        date, float_value = item
        timestamp_str = date.strftime('%Y-%m-%d %H:%M:%S')
        date = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        
        float_value = round(float(float_value), 2)

        float_str = str(float_value)
        output_string += date + '\t  ' + float_str + ' €' + '\n' + '\n'
    return output_string

def get_first_twoStrings(text):
    """
    Funktion: Gibt die ersten beiden Strings aus einem Text zurück.
    param:
        - text: Eingabetext.
    return:
        - Die ersten beiden Strings des Texts.
    """
    strings = text.split()
    if len(strings) >= 2:
        return " ".join(strings[:2])
    else:
        return strings
    
def get_page_headers(urls):
    """
    Funktion: Ruft die Titel von Webseiten anhand ihrer URLs ab.
    param:
        - urls: Liste von URLs.
    return:
        - Liste der Titel der Webseiten.
    """
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

def get_time_ticks(date_stamps):
    """
    Funktion: Generiert Zeitmarkierungen für Diagramme basierend auf den übergebenen Datumswerten.
    param:
        - date_stamps: Liste von Datumswerten im Format '%Y-%m-%d'.
    return:
        - Eine Liste von Tupeln, die Index und Datum für die Zeitmarkierungen enthält.
    """
    modified_date = []
    for date_string in date_stamps:
        date_withoutTime = date_string.replace(' 00:00:00', '')
        modified_date.append(date_withoutTime)
    dates = [datetime.strptime(date_str, '%Y-%m-%d') for date_str in modified_date]
    last_date = dates[-1]
    dates_extended = [last_date + timedelta(days=i) for i in range(1, 11)]
    date_strings_extended = [date.strftime('%Y-%m-%d') for date in dates_extended]
    modified_date.extend(date_strings_extended)
    max_ticks = 10
    numb_ticks = min(len(modified_date), max_ticks)
    ticks_diff = max(1, len(modified_date) // (numb_ticks - 1)) if numb_ticks > 1 else 1
    x_Date_ticks = [(i, modified_date[i]) for i in range(0, len(modified_date), ticks_diff)]
         
    return x_Date_ticks