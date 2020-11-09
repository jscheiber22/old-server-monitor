'''
    This is a library for the Ethereum network API that will simplify the process of pulling information
    from their funky API that dumb dumbs like me refuse to try to learn. It will also make decisions for
    you like is a worker active and maybe even decide the slope of your recent mining.

    Intended for use with Ethpool, Ethermine & Flypool pools.
'''

import sys
import requests
from datetime import datetime

'''
    List of callable commands for Worket because I'll forget because I'm dumb :)
    # for the docs 8)

    update() - updates the information and repulls from the API; no return
    lastSeen() - returns time since last seen in minutes; returns minutes as integer
    getCurrentHashrate() - returns current hashrate in MH/s; returns float
    // getAverageHashrate() - same as current but like the average over 24 hours; returns float *not currently supported by API as of release of this idk why :/
    getActiveWorkers() - returns the count of active workers; returns int
    getValidShares() - returns number of valid shares for that worker; returns int
    getInvalidShares() -returns number of invalid shares for that worker; returns int
    getStaleShares() -returns number of stale shares for that worker; returns int
    // getAccountBalance() - returns the current unpaid balance of the miner; returns float *returns crackhead value that I have no idea what I'm supposed to do with
'''

class General:
    def __init__(self, address):
        self.address = str(address)
        self.update()

    # I assume this will be for any of the workers and the value returned is for the most recent
    def lastSeen(self):
        lastSeen = datetime.utcfromtimestamp(self.data["lastSeen"]) # In UTC time
        currentTime = datetime.utcnow()
        # Returns differnce in time in seconds divided by 60 to make into minutes and then made an integer with // :) Algorithm god 8)
        return (currentTime - lastSeen).seconds // 60

    def getCurrentHashrate(self):
        return round(self.data["currentHashrate"] / 1000000, 3)

    # def getAverageHashrate(self):
    #     return self.data["averageHashrate"]

    def getActiveWorkers(self):
        return self.data["activeWorkers"]

    def getValidShares(self):
        return self.data["validShares"]

    def getInvalidShares(self):
        return self.data["invalidShares"]

    def getStaleShares(self):
        return self.data["staleShares"]

    # def getAccountBalance(self):
    #     # Some formatting to make it easier to use and read
    #     return self.data["unpaid"]

    def update(self):
        response = requests.get("https://api.ethermine.org/miner/" + self.address + "/dashboard") # All data for general information, not miner specific

        # Response for could not find API address so not good :/
        if response.status_code == 404:
            print("Could not find miner. Make sure you entered the address correctly and try again. Also confirm you are sending the miner address as type String.")
            exit()

        # Response for good :) Now it will run all the data determining and whatnot
        elif response.status_code == 200:
            data = response.json()

            # API is a behind and lets you pull from it with a code 200 but still fail with an incorrect address, ew
            if data["status"] == "ERROR":
                print("Could not find miner. Make sure you entered the address correctly and try again. Also confirm you are sending the miner address as type String.")
                exit()

            self.data = data["data"]["currentStatistics"]

        # Uho, one of the other many return codes I neglected to prepare this code for :/ good luck bubs
        else:
            print("API request returned with code: " + respone.status_code + ". Sorry :/")
            exit()

'''
    List of callable commands for Worket because I'll forget because I'm dumb :)
    # for the docs 8)

    update() - updates the information and repulls from the API; no return
    getWorkerName() - returns name of worker declared on object creation; returns String
    isActive() - returns true if active, false if not; returns boolean
    getCurrentHashrate() - returns current hashrate in MH/s; returns float
    lastSeen() - returns time since last seen in minutes; returns minutes as integer
    getValidShares() - returns number of valid shares for that worker; returns int
    getInvalidShares() -returns number of invalid shares for that worker; returns int
    getStaleShares() -returns number of stale shares for that worker; returns int
    getAverageHashrate() - same as current but like the average over 24 hours; returns float
'''

# Technically the data for the miners is available to the general class, but this breaks it up more and makes it easier to work with I think? hope?
class Worker:
    def __init__(self, address, workerName):
        self.address = str(address)
        self.workerName = workerName
        self.update()

    def getWorkerName(self):
        return self.worker["worker"]

    def isActive(self):
        if self.worker["currentHashrate"] < 1:
            return False
        else:
            return True

    def lastSeen(self):
        lastSeen = datetime.utcfromtimestamp(self.worker["lastSeen"]) # In UTC time
        currentTime = datetime.utcnow()
        # Returns differnce in time in seconds divided by 60 to make into minutes and then made an integer with // :) Algorithm god 8)
        return (currentTime - lastSeen).seconds // 60

    def getCurrentHashrate(self):
        return round(self.worker["currentHashrate"] / 1000000, 3)

    def getValidShares(self):
        return self.worker["validShares"]

    def getInvalidShares(self):
        return self.worker["invalidShares"]

    def getStaleShares(self):
        return self.worker["staleShares"]

    def getAverageHashrate(self):
        history = requests.get("https://api.ethermine.org/miner/" + self.address + "/history").json() # Might have to use a different endpoint for this,oops :)
        avgHash = history["data"][self.workerNumber]["averageHashrate"] # Only in worker specific because needs worker number :/
        return round(avgHash / 1000000, 3)

    def update(self):
        response = requests.get("https://api.ethermine.org/miner/" + self.address + "/dashboard") # All data for general information, not miner specific

        # Response for could not find API address so not good :/
        if response.status_code == 404:
            print("Could not find miner. Make sure you entered the address correctly and try again. Also confirm you are sending the miner address as type String.")
            exit()

        # Response for good :) Now it will run all the data determining and whatnot
        elif response.status_code == 200:
            data = response.json()

            # API is a behind and lets you pull from it with a code 200 but still fail with an incorrect address, ew
            if data["status"] == "ERROR":
                print("Could not find miner. Make sure you entered the address correctly and try again. Also confirm you are sending the miner address as type String.")
                exit()

            workers = data["data"]["workers"] # way shortens this for readibiltyh

            # The most difficult way possible to pull the placement of the worker in the list
            if len(workers) > 0:
                self.workerNumber = 0
                for worker in workers:
                    if worker["worker"] == self.workerName:
                        break
                    else:
                        self.workerNumber += 1
                        if self.workerNumber == len(workers) - 1:
                            print("Worker name was not found. Please check your spelling and try again.")
                            exit()
                self.worker = data["data"]["workers"][self.workerNumber]

        # Uho, one of the other many return codes I neglected to prepare this code for :/ good luck bubs
        else:
            print("API request returned with code: " + respone.status_code + ". Sorry :/")
            exit()
