import os
import re


class Reader:
    def __init__(self, filename):
        self.fieldData = []
        self.roversPositions = []
        self.roversCommands = []
        self.read(filename)

    def read(self, filename):
        try:
            with open(filename) as inputFile:
                if os.stat(filename).st_size == 0:
                    raise StopIteration
                self.readField(inputFile)
                self.readPositionAndCommands(inputFile)
        except IOError:
            print("File reading error")
        except ValueError:
            print("Wrong data format")
        except AttributeError:
            print("Wrong field size format")
        except StopIteration:
            print("File empty")

    def readField(self, inputFile):
        firstLine = re.sub(' +', ' ', inputFile.readline().strip())  # removes multiplied spaces
        firstLine = re.search('[0-9]+ [0-9]+', firstLine).group(0)   # string composed of 2 numbers & space
        self.fieldData = [int(x) for x in firstLine.split(" ")]      # cast to list of ints

    def readPositionAndCommands(self, inputFile):
        while True:
            linePosition = inputFile.readline()
            lineCommands = inputFile.readline()
            if len(linePosition) == 0 and len(lineCommands) == 0:
                break
            linePosition = re.sub(' +', ' ', linePosition.strip().upper())
            lineCommands = re.sub(' +', ' ', lineCommands.strip().upper())
            try:
                position = re.search('[0-9]+ [0-9]+ [NESW]', linePosition).group(0)
                commands = re.search('[LRM]*', lineCommands).group(0)
            except AttributeError:
                print("Incorrect input")
                continue
            position = [int(item) if item.isdigit() else item for item in position.split()]

            self.roversPositions.append(position)
            self.roversCommands.append(commands)


class Rover:
    def __init__(self, coords):
        self.x, self.y, self.direction = coords

    def __repr__(self):
        return f"{self.x} {self.y} {self.direction}"

    def __eq__(self, other):
        # Protect against comparisons of other classes.
        if not isinstance(other, Rover):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def roverOnField(self, field):
        if self.x <= field.x and self.y <= field.y:
            return True
        return False


class Field:
    def __init__(self, size):
        if size:
            self.x, self.y = size

    def __str__(self):
        return f"Field top right corner is ({self.x}; {self.y})"


class TrafficControl:
    def __init__(self, fieldData, roversPositions, roversCommands):
        self.directions = "NESW"
        self.field = Field(fieldData)
        self.commands = roversCommands
        self.rovers = self.initializeRovers(roversPositions)
        self.moveRovers()

    def initializeRovers(self, roversPositions):
        rovers = []
        deletedCounter = 0
        for i, rover in enumerate(roversPositions):
            newRover = Rover(rover)
            if not newRover.roverOnField(self.field) or newRover in rovers:
                self.commands.pop(i - deletedCounter)
                deletedCounter += 1
            else:
                rovers.append(newRover)
        return rovers

    def moveRovers(self):
        for i, command in enumerate(self.commands):
            for step in command:
                currentOrientation = self.rovers[i].direction
                if step == 'M':
                    self.move(i)
                else:
                    self.rovers[i].direction = self.rotate(currentOrientation, step)

    def move(self, roverNb):
        match self.rovers[roverNb].direction:
            case "N":
                delta = [0, 1]
            case "E":
                delta = [1, 0]
            case "S":
                delta = [0, -1]
            case "W":
                delta = [-1, 0]
            case _:
                delta = [0, 0]
        newX = self.rovers[roverNb].x + delta[0]
        newY = self.rovers[roverNb].y + delta[1]
        if self.checkSpot(newX, newY):
            self.rovers[roverNb].x = newX
            self.rovers[roverNb].y = newY

    # makes a move only if new position is available
    def checkSpot(self, x, y):
        if x < 0 or y < 0 or x > self.field.x or y > self.field.y:
            return False
        for rover in self.rovers:
            if rover.x == x and rover.y == y:
                return False
        return True

    def rotate(self, currentOrientation, step):
        index = self.directions.find(currentOrientation)
        if step == "R":
            index = (index + 1) % 4
        else:
            index = (index - 1) % 4
        return self.directions[index]


class Writer:
    def __init__(self, data):
        with open("result.txt", "w") as outputFile:
            for item in data:
                outputFile.writelines(repr(item) + "\n")
