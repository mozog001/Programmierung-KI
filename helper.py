#Funktion zum Entfernen eines bestimmten Begriffs wie z. B. 'Inc. Common Stock'
def clear_list_element(list_to_replace, String_to_replace):
    replaced_List = list()
    
    for element in list_to_replace:
        for string in String_to_replace:
            if string in element:
                element = element.replace(string, '')
        replaced_List.append(element)
    return replaced_List