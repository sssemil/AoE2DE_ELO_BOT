import os.path
import json
from json import JSONDecodeError

import requests


class Api:
    MAX_ENTRIES_PER_REQUEST = 1000

    allMatches = []
    lastMatchTimestamp = 0

    def __init__(self, dataFilePath) -> None:
        super().__init__()
        self.dataFilePath = dataFilePath
        if os.path.isfile(self.dataFilePath):
            with open(dataFilePath, 'r') as dataFile:
                try:
                    self.allMatches = json.load(dataFile)
                    self.lastMatchTimestamp = Api.getMaxDateFromMatches(self.allMatches)
                    print(f"Loaded {len(self.allMatches)} entries from storage.")
                except JSONDecodeError:
                    print("Corrupted storage file, resetting...")
                    os.remove(self.dataFilePath)

    @staticmethod
    def getMaxDateFromMatches(matches):
        maxTimestamp = 0
        for match in matches:
            timestamp = match['opened']
            if timestamp > maxTimestamp:
                maxTimestamp = timestamp

        return maxTimestamp

    @staticmethod
    def getMinDateFromMatches(matches):
        minTimestamp = matches[0]['opened']
        for match in matches:
            timestamp = match['opened']
            if timestamp < minTimestamp:
                minTimestamp = timestamp

        return minTimestamp

    @staticmethod
    def getMatches(count, since):
        request = requests.get(f"https://aoe2.net/api/matches?game=aoe2de&count={count}&since={since}")
        data = request.json()
        return data

    def getAllMatches(self):
        while True:
            matches = self.getMatches(Api.MAX_ENTRIES_PER_REQUEST, self.lastMatchTimestamp)
            if len(matches) == 0:
                break
            minTimestamp = Api.getMaxDateFromMatches(matches)
            self.lastMatchTimestamp = Api.getMaxDateFromMatches(matches)
            self.allMatches += matches
            with open(self.dataFilePath, 'w') as dataFile:
                json.dump(self.allMatches, dataFile)

            print(f"Loaded {len(self.allMatches)} entries. "
                  f"Min date - {minTimestamp}, max date - {self.lastMatchTimestamp}.")

        return self.allMatches
