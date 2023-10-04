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
  - [Wie funktioniert das Script?](#einrichten-script)

# How to use?<a name="how-to-use"></a>

This is a short introduction in this project

## Preperations<a name="preperations"></a>

1. You need python 3
2. You need to install pip
3. Create a folder data/origin and paste there your .csv files
4. Update filenames in main.py

## Install and run<a name="install-and-run"></a>

### 1.

Create a virtual environment within your project folder with

```
python -m venv virtualEnv
```

If you get an error then try

```
py -m venv virtualEnv
```

### 2.

Activate virtual environment

```
.\virtualEnv\Scripts\activate
```

If you get an error which says that it isn't allowed to run a script. In that case you need to update your execution policy in windows.
Type the following command into your powershell. To start powershell just press windows key and type **powershell** into the searchbar. Then you will get a suggestion to **open powershell as admin**. Do it. You need administration right to execute the following command:

```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

For more details about this change look here:

- [englisch](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy?view=powershell-7.3)
- [german](https://learn.microsoft.com/de-de/powershell/module/microsoft.powershell.security/set-executionpolicy?view=powershell-7.3)

### 3.

Install all necessary packages with

```
pip install -r requirements.txt
```

### 4.

Start programm with

```
python main.py
```

If you get an error then try

```
py main.py
```

This is only for the first start. Later you just need to activate the virtual environment and can directly start the script.

# Obsolete scripts<a name="obsolete-scripts"></a>

You can find some old scripts within the directory obsolete scripts. This is just for history because there are not functional. But if you want to see how it starts then check them out.

# Detailed beginners guide (ger)<a name="detailed-beginners-guide"></a>

Die folgende Anleitung wird der einfachsheitshalber auf deutsch formuliert.

## Installation von Python<a name="installation-von-python"></a>

Um das Skript ausführen zu können wird auf dem PC Python benötigt. Es gibt mehrere Möglichkeiten Python auf dem Windows System zu installieren. Die einfachste die die Installation aus dem Windows Store.

### Installationsmöglichkeit 1

Öffne die **Eingabeaufforderung** in Windows. Dazu drückst du die Windowstaste und gibt in die Suche `cmd` ein. Dann wird die die Eingabeaufforderung als Option angezeigt.

> Beispiel:\
> ![grafik](https://github.com/LexQzim/emotouchplotter/assets/12845370/4ef317fc-0bd6-402a-864b-e9cbd1e9e108)

Nun gibst du hier einfach `python` ein. Darauf sollte sich der Windows Store öffnen und dir direkt ein passende Pythonversion vorschlagen. Führe nun die Installation aus.

### Installationsmöglichkeit 2

Eine Installationsdatei für Windows lässt sich direkt online (https://www.python.org/downloads/) runterladen.
Achtet hier darauf, dass hier mindestens die Python Version 3.10 verwendet wird.
Führt anschließend die Installation aus und achtet hier darauf, dass der Hacken bei der Pfadeinstellung gesetzt ist.

> Beispiel:\
> ![grafik](https://github.com/LexQzim/emotouchplotter/assets/12845370/d5e645f2-fd25-4146-9f87-797b015708b0)

Dieser Hacken bedeutet, dass Python in die Umgebungsvariablen integriert wird und somit von der Konsole aus überall auf dem PC genutzt werden kann.
Damit du aber Python ohne Probleme nutzen kannst, musst in den Windowseinstellung noch eine Option deaktiveren. Ich empfehle dazu den ersten Lösungsvorschlag aus diesem [Beitrag](https://stackoverflow.com/questions/58754860/cmd-opens-windows-store-when-i-type-python) zu übernehmen.

## Python auf dem eigenen System testen<a name="python-auf-dem-system-testen"></a>

Nach Abschluss der Installation kann mittels der Konsole (Eingabeaufforderung) geprüft werden, ob Python richtig installiert wurde.
Öffne dazu zunächst die Konsole. Im einfachsten Fall drückst du die Windowstaste und gibst dann die Suche **cmd** ein und wählst dann die **Eingabeaufforderung** aus.

Nun gibst du folgende Befehle in die Konsole ein:

```
python --version
```

und

```
pip --version
```

Als Ausgabe wird die angezeigt, welche Version du aktuell auf dem System installiert hast.

> Beispiel:\
> ![grafik](https://github.com/LexQzim/emotouchplotter/assets/12845370/f59a695b-f1df-4347-a888-1e386409e2af)

### Was ist pip?<a name="was-ist-pip"></a>

pip ist ein kleiner Helfer, worüber leicht neue Pakete in Python installiert werden können. Mit diesen Paketen lassen sich die Basisfunktionen von Python erweitern und ermöglichen so eine vielseitige Softwareentwicklung.

## Installation und Einrichtung der Entwicklungsumgebung VScode<a name="installation-vscode"></a>

Es handelt sich ja hierbei um blanken Quellcode. Um diesen vernünftig lesen und bearbeiten zu können empfiehlt es sich eine Entwicklungsumgebung einzurichten. Ich empfehle hier [VSCode](https://code.visualstudio.com/). Es handelt sich dabei um einen Texteditor, welche durch Erweiterungen für jede Programmiersprache, aber auch für die Bearbeitung von verschiedenen Datein, wie .csv und .json, individuell eingerichtet und angepasst werden kann. Gleichzeitig ist der kostenlos und für alle nutzbar.

Starte den Editor nach der erfolgreichen Installation. Klicke in der unteren linken Ecke das Zahnradsymbol an und wähle **Erweiterungen** (Extensions) aus (Tastenkombination: _Strg + Shift + X_). Gib dann in die Suche **Python** ein und installiere die erste vorgeschlagene Erweiterung von Microsoft.

> Beispiel:\
> ![grafik](https://github.com/LexQzim/emotouchplotter/assets/12845370/f9ea91cc-b64d-4a51-b730-5dce8012bf6d)

Du kannst nun im Editor testen, ob du von hier aus Python ausführen kannst. Führe Die Tastenkombination _Strg + Shift + Ö_ aus und es sollte sich innerhalb des Editors eine Konsole öffnen. Gib auch hier wieder `python --version` ein. Du solltest auch hier wieder die Versionsnummer von Python angezeigt bekommen.
Solltest du hier einen Fehler erhalten, dass python nicht gefunden werden kann, dann versuche es mal mit dem Befehl `py --version`.

> Beispiel:\
> ![grafik](https://github.com/LexQzim/emotouchplotter/assets/12845370/34f9ab68-e999-410a-bb62-48227206fa82)

## Runterladen und Einrichten vom Projekt<a name="einrichten-projekt"></a>

Lade dir nun das gesamte Projekt aus github runter. Im einfachsten Fall kannst du dir das Paket als .zip-Datei runterladen und auf deinem PC abspeichern:

> Beispiel:\
> ![grafik](https://github.com/LexQzim/emotouchplotter/assets/12845370/edbd2659-f389-4c2e-b5c0-3e3e6f642d72)

Entpacke das Archiv in einem Ordner deiner Wahl.

Öffne nun VSCode, falls das noch nicht geschehen ist, und öffne hier den Projektorder. Dazu klickst du oben links auf **Datei (File)** und dann auf **Order öffnen... (Open Folder...)**. Alternativ kannst du auch die Tastenkombination _Strg + K_ und dann _Strg + O_ verwenden. Wähle hier nun deinen Projektordner aus.

> Beispiel:\
> ![grafik](https://github.com/LexQzim/emotouchplotter/assets/12845370/c36d04cb-2736-420a-8ea7-8aa4a0c4aed2)

Installiere nun das Paket `virtualenv` mit dem Befehl

```
pip install virtualenv
```

> Beispiel:\
> ![grafik](https://github.com/LexQzim/emotouchplotter/assets/12845370/69e61431-9bfc-40f8-a202-dc7314dc9c84)

Nun kannst du die Schritte unter dem Abschnitt [Install and run](#install-and-run) ausführen.

## Wie funktioniert das Script?<a name="einrichten-script"></a>

Beim ersten Start wird dir auch direkt der Order **data** mit dem Unterordner **origin** erzeugt. Darin legst du deine .csv Dateien ab. Du findest diese Ordner nun in deinem Projektordner. Alternativ kannst du auch in VSCode einen Rechtsklick auf den Ordner machen und dann auf **Reveal in File Explorer** auswählen. Dann öffnet sich der Ordner und du kannst darin deine .csv Dateien ablegen.

> Beispiel: \
> <img width="305" alt="Screenshot 2023-07-15 231420" src="https://github.com/LexQzim/emotouchplotter/assets/12845370/3f72e888-4645-4d90-9784-42b2f767b854">

Für die Bearbeitung werden die Zeitreihen (timeline) und die Sitzungsdaten (session) Daten benötigt. Lade dir diese beiden Daten aus Emotouch herunter und füge diese in den Ordner **origin** ein. Achte bei den Dateinamen darauf, dass keine Leerzeichen enthalten sind. Ersetze alle Leerzeichen durch einen Unterstrich \_

> Beispiel: \
> aus: emoTouch*aus- einschleichend MIT aufforderung_version1.7 (100 ms)\_object_metadata_v1.6.1 \
> wird: emoTouch_aus_einschleichend_MIT_aufforderung_version1.7*(100_ms)\_object_metadata_v1.6.1

Achte darauf, dass du vor dem Herrunterladen der .csv-Dateien das Trennzeichen richtig einstellst. Ich würde hier das Semikolon empfehlen. Ansonsten müsstest du das sonst im Skript entsprechend anpassen.

> Beispiel:\
> <img width="412" alt="Screenshot 2023-07-15 232159" src="https://github.com/LexQzim/emotouchplotter/assets/12845370/bf717feb-f89c-47a2-b3e2-0720d3f14dc8">

Es gibt mehrere .py-Dateien. Die `main.py` ist dabei die Hauptdatei. Von hier aus wird alles ausgeführt.
In der `plotSettings.py` finden sich alle Grundeinstellungen für die Plots. Wie z.b. die Titel und auch die Dateinamen. Hier musst du einmal deine Einstellungen setzen und kontrollieren.
In der `pandaReader.py` werden die .csv Dateien eingelesen und entsprechend konvertiert. Je nach dem, welche Informationen du weiter verarbeiten willst, solltest du hier ggf. nachschauen und anpassen. Für die Bearbeitung der .csv Datein wurde die Bibliothek panda verwendet. Dieses macht es recht einfach, da die gewünschte Spalte über den Namen erfasst werden kann.
In `searbornDrawer.py` werden die Plots erstellt. Dazu wird die Bibliothek seaborn verwendet. Diese harmoniert perfekt mit der Pandas Bibliothek, da das Dateiformat direkt und in die seaborn-Methoden eingebunden werden kann. Alle Einstellungen und Feinjustierungen lassen sich auch hier einfach direkt über den entsprechenden Spaltennamen vornehmen.

> Beispiel:\
> <img width="448" alt="Screenshot 2023-07-15 234314" src="https://github.com/LexQzim/emotouchplotter/assets/12845370/ac8f918b-dabe-450f-98ac-06831e96af6b">

Der Start des Skript erkennst du an der Zeile

```python
if __name__ == "__main__":
```

Alles unterhalb dieser Anweisung wird beim Aufruf der main.py ausgeführt. Hier kannst du durch Auskommentieren und Einfügen definieren, welche Plots du erzeugen möchtest.

Mit einem **#** vor der Zeile kannst du alle unnötigen Zeilen auskommentieren bzw. wenn du es entfernst, dann wird die Zeile wieder aktiv.

#### Wichtige Notiz

Achte darauf, dass die Endungen der Dateinamen auch passend zu den spezifischen Endungen von emotouch passen. Die Dateinamen setzen sich nämlich immer aus 2 - 3 Elementen zusammen.

> (Sitzungname) _ (Version_1.7) _ (Typ_der_Datei).csv

Es reicht, wenn du den ersten Teil (Sitzungsname) in die Liste **fileNames** hinzufügst.
Der mittlere Teil kommt nur in den resampelten Dateien vor.
Der Rest wird im Skript an den entsprechenden Stellen generisch zusammen gesetzt. Die Variablen sind dabei so benannten, wie der geforderte String (Textabschnitt).

#### Ergebnisse

Die Ergebnisse des Programm finden sich dann alle im Ordner **data**

#### Übrigens

Du kannst das Script auch direkt über die Playtaste im Editor starte. Wenn du eine .py-Datei geöffnet hast, dann findest du das Symbol oben rechts.

> Beispiel:
> ![grafik](https://github.com/LexQzim/emotouchplotter/assets/12845370/9ef307b3-3aad-4fa4-b4b7-2d502c5abf84)
