#! python3
# NOT a cash register. just a change maker.
# what da least dat change be
import pyinputplus, cProfile, time
from timeit import default_timer as timer
from datetime import datetime
# price = round(pyinputplus.inputFloat("how much all da ish cost"), 2)
# mulaGiven = round(pyinputplus.inputFloat("how much you given meh"), 2)
# change = mulaGiven - price
changey = round(pyinputplus.inputFloat("what you getting dat change for"), 2)
startD, startT, startTT = datetime.now(), time.time(), timer()
def changeFunc(change):
    if change < 0:
        raise Exception("you aint even give enough doe")
    changeDenoms = {"penny(')": .01, "nickel(s)": .05, "dime(s)": .1, "quarter(s)": .25, "dollar(s)": 1,
                    "5-dollar-bill(s)": 5, "10-dollar-bill(s)": 10, "20-dollar-bill(s)": 20, "50-dollar-bill(s)": 50,
                    "100-dollar-bill(s)": 100}
    giveBackStr, denomsGiven, denomVals = "give back...", 0, list(changeDenoms.values())
    denomVals.sort(reverse=True)
    for denom in denomVals:
        while denom <= change:
            change -= denom
            denomsGiven += 1
        if denomsGiven != 0:
            giveBackStr += f"\n{denomsGiven} {list(changeDenoms.keys())[list(changeDenoms.values()).index(denom)]}"
        denomsGiven = 0
    print(giveBackStr)
cProfile.run("changeFunc(changey)")
endD, endT, endTT = datetime.now() - startD, time.time() - startT, startTT - timer()
print(endD, endT, endTT)



