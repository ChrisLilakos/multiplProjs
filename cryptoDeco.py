# program that will encode and decode based
# for every letter in the abc is gonna be a number
# the number is how many 3's to move

import math, pyperclip, time  # math import cuz python goes 15 digits after decimal
from timeit import default_timer as timer
from datetime import datetime
startD, startT, startTT = datetime.now(), time.time(), timer()
abc = "abcdefghijklmnopqrstuvwxyz"
def decoding(nums):
    text, abcLen,  = "", len(abc)
    abcLenT2 = abcLen * 2
    if abcLen % 3 == 0:
        raise Exception
    nums = nums.split("-")
    for num in nums:
        num = float(num)
        num = round(num / math.e, 4)
        num *= 3
        if abcLenT2 > num > abcLen:
            num -= abcLen
        elif num > abcLenT2:
            num -= abcLenT2
        # while num > abcLen:
        #     num -= abcLen
        text += abc[round(num)-1]
    print("decoded: ", text)
    return text

def encoding(text):
    text, charRemovals, cryption = list(text.lower()), [], ""
    # removing non-letters
    for char in text:
        if char not in abc:
            charRemovals.append(char)
    for item in charRemovals:
        text.remove(item)
    # (end of) removing non-letters (end)
    for letter in text:
        triterator, triterUnchained, letterMatchIndP1 = 3, 3, abc.find(letter) + 1
        if letterMatchIndP1 in range(3, len(abc), 3):
            triterUnchained = letterMatchIndP1
        elif letterMatchIndP1 in range(1, len(abc), 3):
            triterUnchained = letterMatchIndP1 + len(abc)
        elif letterMatchIndP1 in range(2, len(abc), 3):
            triterUnchained = letterMatchIndP1 + (len(abc) * 2)
        # while abc[triterator-1] != letter:
        #     triterator += 3
        #     triterUnchained += 3
        #     if triterator > len(abc):
        #         triterator -= 26
        triterUnchainedD3 = triterUnchained // 3
        finalTriter = round(triterUnchainedD3 * math.e, 4)
        cryption += f"{finalTriter}-"
    cryption = cryption.strip("-")
    print("encoded: ", cryption)
    return cryption

encoded = encoding(pyperclip.paste())
endD, endT, endTT = datetime.now() - startD, time.time() - startT, startTT - timer()
print(endD, endT, endTT)

print("\n\ndecoding start")
startD, startT, startTT = datetime.now(), time.time(), timer()
decoding(encoded)
endD, endT, endTT = datetime.now() - startD, time.time() - startT, startTT - timer()
print(endD, endT, endTT)
