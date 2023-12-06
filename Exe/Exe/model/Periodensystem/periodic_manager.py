from model.Periodensystem.element import Element
from model.Periodensystem.listeNamenElementeDeutsch import elementeNamenDeutsch
import random
import json

class Manager():

    def __init__(self, window) -> None:

        self.listOfAllElements          = []
        self.listHiddenElementsByNumber = []
        self.window                     = window
        self.gameStarted                = False
        self.askedOrdinalNumber         = None
        self.window.lineEdit.setReadOnly(True)

        #Auslesen der JSON in einem Loop und speichern der für uns benötigten Daten in ein Elementobject, dieses Object 
        # wird in eine Liste gespeichert
        with open('model/Periodensystem/elements.json', 'r') as jsonDatei:
            data = json.load(jsonDatei)
            for element in data["elements"]:
                elementObject = Element(elementeNamenDeutsch[element["number"]-1], element["atomic_mass"], element["density"], element["number"],element["symbol"], element["electronegativity_pauling"])
                self.listOfAllElements.append(elementObject)

        self.window.assignElements(self.listOfAllElements)
    
    #Funktion die durch random Zahlen wählt und die entsprechenden Elemente ausblendet. Ausgeblendete Elemente
    # werden in einer Liste gespeichert um sie später leichter wieder aufzudecken.
    #Fehlerhandling: Durch while loop wird sichergestellt, dass keine Zahl doppelt vorkommt
    def hideRandomElements(self, count):

        for i in range(count):
            randomOrdinalNumber = random.randint(1, len(self.listOfAllElements)-1)
            while randomOrdinalNumber in self.listHiddenElementsByNumber:
                randomOrdinalNumber = random.randint(1, len(self.listOfAllElements)-1)
            self.window.hideElement(randomOrdinalNumber)
            self.listHiddenElementsByNumber.append(randomOrdinalNumber)


    def initConectors(self):

        self.window.startButton.clicked.connect(self.onStart)


    #Funktionen um Aufgabe anzuzeigen: Entweder wird das Element nach Ordnungszahl oder Symbol gesucht
    def showOrdinalNumberTask(self, ordinalNumber):

        self.window.displayTask("Das Element mit der Ordungszahl " + str(ordinalNumber))


    def showSymbolTask(self, ordinalNumber):

        symbol = self.listOfAllElements[ordinalNumber-1].symbol
        self.window.displayTask("Das Element mit dem Symbol " + symbol)

    #Funktion um zu entscheiden welche Aufgabe gewählt wird, durch random mit zwei Zahlen(0,1), solange noch 
    # Elemnete in der von uns zuvor erstelleten Liste vorhanden sind. Wenn die Liste leer ist(=alle Elemente aufgedeckt)
    #  wird ein gut gemacht Text eingeblendet, der Startbutton wird resettet und das Schreibfeld wird auf RO gesetzt.
    def showRandomTask(self):

        coinToss = random.randint(0, 1)
        if len(self.listHiddenElementsByNumber) > 0:
            randomIndex = random.randint(0, len(self.listHiddenElementsByNumber)-1)
            ordinalNumber = self.listHiddenElementsByNumber[randomIndex]

            if coinToss == 0:
                self.showOrdinalNumberTask(ordinalNumber)
            else:
                self.showSymbolTask(ordinalNumber)

            self.askedOrdinalNumber = ordinalNumber

            self.listHiddenElementsByNumber.remove(ordinalNumber)
        else:
            self.window.displayTask("Gut gemacht! :)") 
            self.window.timer.stop()
            self.window.startButton.setText("Start")
            self.window.lineEdit.setReadOnly(True)

    #Funktion die bei klicken des Startbuttons aufgerufen wird: Ruft die benötigeten Funktionen zum Spielstart auf.
    #Fehlerhandling:Sollte das Spiel bereits eim Gange seit wird statdessen das Spiel resettet.
    def onStart(self):

        if self.gameStarted == False:
            self.winStreakCounter = 0
            self.window.lineEdit.setReadOnly(False)
            self.window.resetTimer()
            self.window.timer.start(1000)
            self.window.startButton.setText("Stop")
            self.hideRandomElements(12)
            self.showRandomTask()
            self.gameStarted = True
        else:
            self.window.timer.stop()
            self.window.assignElements(self.listOfAllElements)
            for i in range(118):
                self.window.elementWidgets[i].setStyleSheet("background-color:#b5deff; border-style:outset; border-width:1px; border-color:#ffffff;")
            self.window.startButton.setText("Start")
            self.listHiddenElementsByNumber.clear()
            self.winStreakCounter = 0
            self.window.rightWrong.setText("Richtig/Falsch")
            self.window.rightWrong.setStyleSheet("text-align:center; background-color:#b5deff; border-style:outset; border-width:1px; border-color:#ffffff;")
            self.gameStarted = False

    #Funktionen um den Input vorher zu prüfen um Fehler abzufangen und um mit Enterdrücken weiter zu können
    def onInputTextChange(self):

        self.evaluateUserInput(self.window.lineEdit.text())
        self.window.lineEdit.clear()

    def readUserInput(self):

        userInput          = input()
        userInputLowercase = userInput.lower()
        return userInputLowercase
    
    #Funktion die die zuvor auf Fehler überprüfte Eingabe des Users mit der richtigen Antwort vergleicht und
    # dementsprechend reagiert(Richtig/Falsch Display, ...)
    def evaluateUserInput(self, userInput):

        correctAnswer = str(self.listOfAllElements[(self.askedOrdinalNumber)-1].name)
        if userInput == correctAnswer or userInput == correctAnswer.lower():
            self.revealElement(self.askedOrdinalNumber)
            self.winStreakUp()
            self.displayRight()  
            self.showRandomTask()
        else:
            self.resetWinStreak()
            self.displayWrong()
  
    #Funktion um durch drücken der Enter Taste den Input zu evaluieren
    def mainGameLoop(self):

        self.window.lineEdit.returnPressed.connect(self.onInputTextChange)
        userInput = self.readUserInput()
        self.evaluateUserInput(userInput)

    #Funktionen die die UI bei richtiger/falscher Eingabe ändern.
    def winStreakUp(self):
        self.winStreakCounter += 1
        self.window.winCounter.setText(str(self.winStreakCounter))
    

    def resetWinStreak(self):
        self.winStreakCounter = 0
        self.window.winCounter.setText(str(self.winStreakCounter))
    

    def displayRight(self):
        self.window.rightWrong.setText("Richtig")
        self.window.rightWrong.setStyleSheet("text-align:center; background-color:#90EE90; border-style:outset; border-width:1px; border-color:#006400;")
    

    def displayWrong(self):

        self.window.rightWrong.setText("Falsch")
        self.window.rightWrong.setStyleSheet("background-color:#DE1738; border-style:outset; border-width:1px; border-color:#8B0000;")

    #Funktion, die nach richtigem Userinput das Element wieder anzeigt.
    def revealElement(self, ordinalNumber):
        self.window.elementWidgets[ordinalNumber-1].setStyleSheet("background-color:#b5deff; border-style:outset; border-width:1px; border-color:#ffffff;")
        self.window.elementWidgets[ordinalNumber-1].symbol.setText(str(self.listOfAllElements[ordinalNumber-1].symbol))
        self.window.elementWidgets[ordinalNumber-1].ordinalNumber.setText(str(ordinalNumber))
        self.window.elementWidgets[ordinalNumber-1].atomicMass.setText(str(self.listOfAllElements[ordinalNumber-1].atomic_mass)[:5])
        self.window.elementWidgets[ordinalNumber-1].fullName.setText(str(self.listOfAllElements[ordinalNumber-1].name))
