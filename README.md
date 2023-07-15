# emotouchplotter
This small python project to evaluate and plot csv data of emotouch.

# Content
- [How to use?](#how-to-use)
  - [Preperations](#preperations)
  - [Install and run](#install-and-run)
- [Obsolete scripts](#obsolete-scripts)
- [Detailed beginners guide (ger)](#detailed-beginners-guide)
  - [Installation von Python](#installation-von-python)
  - [Python auf dem eigenen System testen](#python-auf-dem-system-testen)
    - [Was ist pip?](#was-ist-pip)
  - [Installation und Einrichtung der Entwicklungsumgebung VScode](#installation-vscode)
  - [Runterladen und Einrichten vom Projekt](#einrichten-projekt)

# How to use?<a name="how-to-use"></a>
This is a short introduction in this project

## Preperations<a name="preperations"></a>
1. You need python 3
2. You need to install pip
3. Create a folder data/origin and paste there your .csv files
4. Update filenames in main.py

## Install and run<a name="install-and-run"></a>
1. Create a virtual environment within your project folder with
```
python -m venv virtualEnv
```
2. Activate virtual environment
```
.\venv\Scripts\activate
```
3. Install all necessary packages with 
```
pip install -r requirements.txt
```
4. Start programm with
```
python main.py
```

This is only for the first start. Later you just need to activate the virtual environment and can directly start the script.

# Obsolete scripts<a name="obsolete-scripts"></a>
You can find some old scripts within the directory obsolete scripts. This is just for history because there are not functional. But if you want to see how it starts then check them out.

# Detailed beginners guide (ger)<a name="detailed-beginners-guide"></a>
Die folgende Anleitung wird der einfachsheitshalber auf deutsch formuliert.

## Installation von Python<a name="installation-von-python"></a>
Um das Skript ausführen zu können wird auf dem PC Python benötigt. Eine Installationsdatei für Windows lässt sich hier (https://www.python.org/downloads/) runterladen.
Achtet hier darauf, dass hier mindestens die Python Version 3.10 verwendet wird. 
Führt anschließend die Installation aus und achtet hier darauf, dass der Hacken bei der Pfadeinstellung gesetzt ist.
> Beispiel:
> ![grafik](https://github.com/LexQzim/emotouchplotter/assets/12845370/d5e645f2-fd25-4146-9f87-797b015708b0)

Dieser Hacken bedeutet, dass Python in die Umgebungsvariablen integriert wird und somit von der Konsole aus überall auf dem PC genutzt werden kann. 

Alternativ kannst du dir auch Python direkt aus dem Windows Store laden. Wenn du einfach `python` in die Eingabeaufforderung eingibst, dann öffnet sich automatisch der Store und schlägt dir eine Python Version vor.

## Python auf dem eigenen System testen<a name="python-auf-dem-system-testen"></a>
Nach Abschluss der Installation kann mittels der Konsole (Eingabeaufforderung) geprüft werden, ob Python richtig installier wurde. 
Öffne dazu zunächst die Konsole. Im einfachsten Fall drückst du die Windowstaste und gibst dann die Suche "cmd" ein und wählst dann die "Eingabeaufforderung" aus.

> Beispiel:
> ![grafik](https://github.com/LexQzim/emotouchplotter/assets/12845370/4ef317fc-0bd6-402a-864b-e9cbd1e9e108)

Nun gibst du folgende Befehle in die Konsole ein:
```
python --version
```
und
```
pip --version
```
Als Ausgabe wird die angezeigt, welche Version du aktuell auf dem System installiert hast.

> Beispiel:
> ![grafik](https://github.com/LexQzim/emotouchplotter/assets/12845370/f59a695b-f1df-4347-a888-1e386409e2af)

### Was ist pip?<a name="was-ist-pip"></a>
pip ist ein kleiner Helfer, worüber leicht neue Pakete in Python installiert werden können. Mit diesen Paketen lassen sich die Basisfunktionen von Python erweitern und ermöglichen so eine vielseitige Softwareentwicklung.

## Installation und Einrichtung der Entwicklungsumgebung VScode<a name="installation-vscode"></a>
Es handelt sich ja hierbei um blanken Quellcode. Um diesen vernünftig lesen und bearbeiten zu können empfiehlt es sich eine Entwicklungsumgebung einzurichten. Ich empfehle hier [VsCode](https://code.visualstudio.com/). Es handelt sich dabei um einen Texteditor, welche durch Erweiterungen für jede Programmiersprache, aber auch für die Bearbeitung von verschiedenen Datein, wie .csv und .json, individuell eingerichtet und angepasst werden kann. Gleichzeitig ist der kostenlos und für alle nutzbar. 

Starte den Editor nach der erfolgreichen Installation. Klicke in der unteren linken Ecke das Zahnradsymbol an und wähle Erweiterungen (Extensions) aus (Tastenkombination: Strg + Shift + X). Gib dann in die Suche Python ein und installiere die erste vorgeschlagene Erweiterung von Microsoft.

> Beispiel:
> ![grafik](https://github.com/LexQzim/emotouchplotter/assets/12845370/f9ea91cc-b64d-4a51-b730-5dce8012bf6d)

Du kannst nun im Editor testen, ob du von hier aus Python ausführen kannst. Führe Die Tastenkombination Strg + Shift + Ö aus und es sollte sich innerhalb des Editors eine Konsole öffnen. Gib auch hier wieder `python --version` ein. Du solltest auch hier wieder die Versionsnummer von Python angezeigt bekommen.

> Beispiel:
> ![grafik](https://github.com/LexQzim/emotouchplotter/assets/12845370/34f9ab68-e999-410a-bb62-48227206fa82)

## Runterladen und Einrichten vom Projekt<a name="einrichten-projekt"></a>
Lade dir nun das gesamte Projekt aus github runter. Im einfachsten Fall kannst du dir das Paket als .zip-Datei runterladen und auf deinem PC abspeichern:
> Beispiel:
> ![grafik](https://github.com/LexQzim/emotouchplotter/assets/12845370/edbd2659-f389-4c2e-b5c0-3e3e6f642d72)

Entpacke das Archiv in einem Ordner deiner Wahl.

Öffne nun VSCode, falls das noch nicht geschehen ist, und öffne hier den Projektorder. Dazu klickst du oben links auf "Datei" (File) und dann auf "Order öffnen..." (Open Folder...). Alternativ kannst du auch die Tastenkombination Strg + K und dann Strg + O verwenden. Wähle hier nun deinen Projektordner aus. 

> Beispiel:
> ![grafik](https://github.com/LexQzim/emotouchplotter/assets/12845370/c36d04cb-2736-420a-8ea7-8aa4a0c4aed2)

Installiere nun das Paket `virtualenv` mit dem Befehl
```
pip install virtualenv
```

> Beispiel:
> ![grafik](https://github.com/LexQzim/emotouchplotter/assets/12845370/69e61431-9bfc-40f8-a202-dc7314dc9c84)

Nun kannst du die Schritte unter dem Abschnitt [Install and run](#install-and-run) ausführen. 
Beim ersten Start wird dir auch direkt der Order "data" mit dem Unterordner "origin" erzeugt. Darin legst du deine .csv Dateien ab. Nun musst du in der `main.py` die Dateinamen in der Zeile 7-10 entsprechend anpassen:

> Beispiel:
> ![grafik](https://github.com/LexQzim/emotouchplotter/assets/12845370/2378e02e-a4b5-4e77-850c-c88d730a86e4)

Übrigens. Du kannst das Script auch direkt über die Playtaste im Editor starte. Wenn du eine .py datei geöffnet hast, dann findest du das Symbol oben rechts. 
> Beispiel:
> ![grafik](https://github.com/LexQzim/emotouchplotter/assets/12845370/9ef307b3-3aad-4fa4-b4b7-2d502c5abf84)



