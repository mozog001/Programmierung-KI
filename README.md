[**Aktien-App**](#aktien-app)
- [Warum haben wir die Technologien verwendet, die wir verwendet haben?](#warum-haben-wir-die-technologien-verwendet-die-wir-verwendet-haben)
- [Wir haben diese Technologien verwendet, weil sie uns die folgenden Vorteile bieten:](#wir-haben-diese-technologien-verwendet-weil-sie-uns-die-folgenden-vorteile-bieten)
- [Welche Herausforderungen haben wir bei der Entwicklung unserer Anwendung gemeistert?](#welche-herausforderungen-haben-wir-bei-der-entwicklung-unserer-anwendung-gemeistert)
- [Welche Funktionen möchten wir in Zukunft implementieren?](#welche-funktionen-möchten-wir-in-zukunft-implementieren)
- [Ursprüngliche Zielsetzung der Aktien-App zu Beginn:](#ursprüngliche-zielsetzung-der-aktien-app-zu-beginn)
- [Installationshinweis:](#installationshinweis)
- [Bedienhinweis:](#bedienhinweis)
- [Known Issues](#known-issues)

Unsere Aktien-App ist ein Aktienkurs-Index-Tool, das es Benutzern ermöglicht, die Kursentwicklung von Aktien verschiedener Unternehmen zu verfolgen. Die Anwendung bezieht Daten über eine kostenlose Börsen-API und speichert diese in einer Datenbank. Die Daten werden dann in einer grafischen Benutzeroberfläche (GUI) dargestellt, die es Benutzern ermöglicht, den Aktienkurs und zugehörige Informationen über die Zeit zu sehen.

Die Anwendung bietet folgende Funktionen:

-   Auswahl verschiedener Unternehmen und deren Aktienkurse
-   Anzeige und Ausblendung von Informationen im zeitlichen Verlauf
-   Anwendung verschiedener Analysemethoden
-   Export und Speicherung der Daten in einer Datenbank

## Warum haben wir die Technologien verwendet, die wir verwendet haben?

Wir haben die folgenden Python-Bibliotheken, Tools und APIs verwendet, um unsere Anwendung zu erstellen:

<b>PyQt5</b>: PyQt5 ist ein Qt-Framework für Python, das die Entwicklung von grafischen Benutzeroberflächen (GUIs) ermöglicht.  
<b>PyQt5-tools</b>: PyQt5-tools ist eine Sammlung von Tools, die die Entwicklung von PyQt5-Anwendungen erleichtern.  
<b>Matplotlib</b>: Matplotlib ist eine Bibliothek für die Erstellung von Diagrammen und Visualisierungen.  
<b>yfinance</b>: yfinance ist eine Bibliothek für den Zugriff auf Finanzdaten.  
<b>pandas</b>: pandas ist eine Bibliothek für die Manipulation und Analyse von Daten.  
<b>pyqtgraph</b>: pyqtgraph ist eine Bibliothek für die Erstellung von interaktiven Diagrammen und Visualisierungen.  
<b>prophet</b>: Prophet ist ein Zeitreihen-Forecasting-Modell.  

## Wir haben diese Technologien verwendet, weil sie uns die folgenden Vorteile bieten:

<b>Python</b>: Python ist eine leistungsstarke und vielseitige Sprache, die sich gut für die Entwicklung von Datenanalyse- und Visualisierungstools eignet.  
<b>PyQt5</b>: PyQt5 bietet eine einfache und intuitive API für die Entwicklung von GUIs.  
<b>Matplotlib</b>: Matplotlib bietet eine Vielzahl von Funktionen für die Erstellung von ansprechenden und informativen Diagrammen und Visualisierungen.  
<b>yfinance</b>: yfinance bietet einen einfachen Zugriff auf Finanzdaten aus einer Vielzahl von Quellen.  
<b>pandas</b>: pandas bietet eine Vielzahl von Funktionen für die Manipulation und Analyse von Daten.  
<b>pyqtgraph</b>: pyqtgraph bietet eine leistungsstarke und flexible API für die Erstellung von interaktiven Diagrammen und Visualisierungen.  
<b>prophet</b>: Prophet bietet eine einfache Möglichkeit, Zeitreihen zu modellieren und zu prognostizieren.  

## Welche Herausforderungen haben wir bei der Entwicklung unserer Anwendung gemeistert?

Wir haben erfolgreich mehrere Herausforderungen während der Anwendungsentwicklung bewältigt. Die Integration der Börsen-API stellte eine bedeutende Hürde dar, da die Vielfalt der Funktionen eine genaue Auseinandersetzung erforderte. Die GUI-Entwicklung erforderte Experimente, um die richtige Balance zwischen Funktionalität und Benutzerfreundlichkeit zu finden.    

Ein weiterer Schwerpunkt lag auf dem Abgleich der tagesaktuellen Börsen-API-Daten mit der Datenbank. Aufgrund unterschiedlicher Datenformate war die Entwicklung eines Algorithmus notwendig, der eine nahtlose Zusammenführung ermöglichte. Durch gründliche Auseinandersetzung mit den Datenformaten und einem eigens entwickelten Algorithmus konnten wir diese Herausforderung erfolgreich meistern. Dies ermöglicht uns nun die Nutzung aktueller Daten für umfassende Analysen in unserer Anwendung.

## Welche Funktionen möchten wir in Zukunft implementieren?

In Zukunft planen wir die Integration folgender Funktionen in unsere Anwendung:  

-   Unterstützung für weitere Börsen-APIs
-   Implementierung von Threads, um das Einfrieren des Fensters zu vermeiden
-   Automatisches Drücken der Buttons "Absolut" und "1-Woche", wenn eine neue Aktie ausgewählt wird
-   Grafische Anzeige der ausgewählten Zeiträume durch Buttons, ähnlich wie bei den Analysemethoden
-   Signalisierung an den Benutzer, wenn die Anwendung im Hintergrund arbeitet
-   Automatisches Plotten des Graphen beim Auswahlwechsel einer weiteren Analyse-Methode


## Ursprüngliche Zielsetzung der Aktien-App zu Beginn:

- [x] Bezug von Daten über eine kostenlose Börsen-API
- [x] Sammeln und Speichern der Daten in einer Datenbank
- [x] Darstellung des Aktienkurses und zugehöriger Informationen über die Zeit
- [x] Auswahl verschiedener Unternehmen und deren Aktienkurse über eine grafische Benutzeroberfläche (GUI)
- [x] Möglichkeit zur Anzeige und Ausblendung von Informationen im zeitlichen Verlauf über die GUI
- [x] Anwendung verschiedener Analysemethoden über die GUI
- [ ] Export und Speicherung der Daten in Excel-Format über die GUI

## Installationshinweis:
Um die für das Projekt notwendigen Requirements automatisch zu installieren, muss in das Verzeichnis navigiert werden und in folgender Code in der Kommandozeile ausgeführt werden: pip install -r requirements.txt

## Bedienhinweis:
1. Starten der main.py
2. Name des Unternehmens in das Suchfeld eingeben (nur NASDAQ-Unternehmen werden unterstützt)
3. Das Unternehmen im Dropdown auswählen und Enter drücken. Anschließend auf die API-Abfrage bzw. den Datenbankaufruf warten (dauert bis zu einer Minute)
4. Nachdem die Daten verarbeitet wurden, sind die Weekly-Trends ersichtlich.
5. Damit der Aktienkurs visuell Dargestellt werden kann, muss die Schaltfläche ABS (Absoluter Aktienkurs) selektiert werden und ein Betrachtungszeitraum gewählt werden (z.B. 6 Monate).
6. Um sich weitere Analysen anzeigen zu lassen, können die Buttons SMA (Simple Moving Average) und TSM () ausgewählt werden. Hinweis: Der Graph wird erst angezeigt, nachdem man einen Zeitraum auswählt.

## Known Issues
Issue: "Importing plotly failed. Interactive plots will not work."  
Solution: run pip install --upgrade plotly  
  
Issue: Wenn bereits ein Unternehmen dargestellt wurde, wird der Graph nach Auswahl eines neuen Unternehmens nicht gelöscht.  
Solution: Gewünschte Analyseverfahren auswählen und Zeitraum auswählen, sodass der Graph aktualisiert wird.  
  