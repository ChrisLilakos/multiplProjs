#! python3
# College/highschool (wo)Men's 100 Meters top 5000 Rankings for outdoor official races
# supposed to get male hs (boys), female hs (girls), female college (women), male college (men) per year (5 dif years)
# 20 folders should be created 4 groups per year
import lxml, pprint, csv, re, pyinputplus
from pathlib import Path as path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import exceptions as selErr

browser = webdriver.Edge(executable_path=r"C:\Users\chris\OneDrive\Desktop\edgedriver_win64\msedgedriver.exe")
browser.get("https://www.athletic.net/TrackAndField/Division/Event.aspx?DivID=115862&Event=1&page=0")
browser.maximize_window()

def loginAth():  # signing in
    browser.find_element_by_partial_link_text("Create Free Account to View").click()
    browser.implicitly_wait(4)
    browser.find_element_by_css_selector('[type="email"]').send_keys("cjwillis92@yahoo.com")
    browser.minimize_window()  # so the password can be typed in
    browser.find_element_by_css_selector('[type="password"]').send_keys(input("passcode:\n"))
        # pyinputplus.inputPassword("gimme dat pass\n", mask='*', strip='\n', correctPassword=None))
    browser.maximize_window()
    browser.find_element_by_css_selector('[type="password"]').submit()

# get the tr elems, then get the td elems into a list and put that list into another list
def athltScrp(url):
    browser.implicitly_wait(4)
    browser.get(url)
    browser.implicitly_wait(4)
    athltDataLis, outrAthltlis, innerAthltLis = BeautifulSoup(browser.page_source, 'lxml').select("tbody > tr > td"), \
                            [["Rank", "Grade Year", "Athlete", "Media Link", "Time", "State", "Team", "Date",
                              "Meet/Event/Race", "Raw Time (Sec)"]], []
    markReg = re.compile(r"\s?(\d{1,2}:)?(\d{1,2}.\d{2})?(.*)")  # second group for absolute num. for the Mark & MrkInt
    athltDataLis = athltDataLis[:-1]
    while len(outrAthltlis) <= maxAthlts:  # while the number of students doesn't go over the max athlts we want...
        #       may go a little bit over 5000. can just cut the list if we want with a list = list[:5001]
        timeFloat, clipCnt, markCnt, ordrCnt = 0, 1, 13, 9  # markcnt is 13 instead of 4 to skip the first row
        for cnt in range(len(athltDataLis)):
            athDlisCnt = athltDataLis[cnt]
            if cnt == len(athltDataLis) - 1:  # append the remaining elements to the outer list when its finish
                innerAthltLis.append(athltDataLis[cnt].getText())
                innerAthltLis.append(timeFloat)
                outrAthltlis.append(innerAthltLis)
                innerAthltLis = []
            elif (cnt % 9 == 0 and cnt not in [0, 9]) or cnt == len(athltDataLis):
                #       0 % 9 == 0 and we want to ignore the first row which is a header aka the first 9 td's
                innerAthltLis.append(timeFloat)
                outrAthltlis.append(innerAthltLis)
                innerAthltLis = []  # make the list empty for the new row
            # elif cnt % 4 == 0 and cnt not in [0, 4] and cnt % 8 != 0:  # if it can divide by 8 then it's the last row
            elif cnt == markCnt:  # or something like if (cnt - 1) / 3 == float(clipcnt)
                markCnt += 9
                mrkRegG1, mrkRegG2 = markReg.findall(athltDataLis[cnt].getText())[0][0], \
                                     markReg.findall(athltDataLis[cnt].getText())[0][1]  # g1 minutes, g2 seconds
                # assert len(markReg.findall(athltDataLis[cnt].getText())[0][0])==0, "err cuz sum slowass mofo's in hur"
                if len(mrkRegG1) == 0:
                    # if len(markReg.findall(athltDataLis[cnt].getText())[0][1]) != 0:
                    timeFloat = float(mrkRegG2)  # da 2nd group is there sec's
                else:
                    timeFloat = float(mrkRegG2) + (float(mrkRegG1.strip(":")) * 60)

            if cnt / 3 == float(clipCnt) and cnt not in range(0, 9):
                # for the clip column. cnt%6!=0 isn't an option so i gotta do a workaround. the workaround makes all %'s
                #   obsolete such as cnt%3==0, cnt%9!=0. and if it has an a tag child elem
                clipCnt += 3
                if len(athltDataLis[cnt].select("a")) != 0:
                    innerAthltLis.append(athltDataLis[cnt].select("a")[0].attrs["href"])  # rmemba its bSoup not selnium
                else:
                    innerAthltLis.append(athltDataLis[cnt].getText())
            elif cnt == ordrCnt and cnt not in range(0, 9):
                ordrCnt += 9
                if len(athltDataLis[cnt].getText()) == 0:
                    innerAthltLis.append(str(len(outrAthltlis)) + ".")
                else:
                    innerAthltLis.append(athltDataLis[cnt].getText())
            elif cnt not in range(0, 9):
                innerAthltLis.append(athltDataLis[cnt].getText())
        try:
            browser.find_element_by_link_text("View Next Page").click()
        except selErr.NoSuchElementException:
            break
        athltDataLis = BeautifulSoup(browser.page_source, "lxml").select("tbody > tr > td")
        athltDataLis, innerAthltLis = athltDataLis[:-1], []
    # pprint.pprint(outrAthltlis)
    disYear = browser.find_elements_by_css_selector('[ng-model="appC.params.season"]')[1].find_element_by_css_selector(
    '[selected="selected"]').text
    disPg = browser.find_element_by_tag_name("h2").text.replace(" ","")
    with open(path("csvRunFiles") / f'{disPg}{disYear}.csv', 'w', newline='') as fileObj:
        csv.writer(fileObj).writerows(outrAthltlis)
    # todo: zip these files/folders (use zipfile module?)

def genderize(url):
    urlReg = re.compile(r"(.*)(&page=\d{,4})$")
    if url.endswith("&page="):
        url += "0"
    elif len(urlReg.findall(url)) == 0:
        url += "&page=0"

    if urlReg.findall(url)[0][0][-1] == "1":  # when it ends in &Event=1 it is male, &Event=19 when it is female
        return urlReg.findall(url)[0][0] + "9"  # gets puts in
    elif urlReg.findall(url)[0][0][-1] == "9":  # takes whatever came before the page number
        return urlReg.findall(url)[0][0].strip("9")  # takes it out
    # else:
    #     raise Exception("url doesn't end with the page number")
def schoolChng():
    # browser.get(url)
    lvls = browser.find_element_by_css_selector('[ng-model="appC.params.level"]')
    lvls.click()
    if lvls.find_element_by_css_selector('[selected="selected"]').text == "College":
        lvls.find_element_by_css_selector('[value="4"]').click()
    elif lvls.find_element_by_css_selector('[selected="selected"]').text == "High School":
        lvls.find_element_by_css_selector('[value="8"]').click()
    return browser.current_url
def yearChng(year):
    lvls = browser.find_elements_by_css_selector('[ng-model="appC.params.season"]')[1]
    lvls.click()
    lvls.find_element_by_css_selector(f'[value="{year}"]').click()
    return browser.current_url

def athCalling(url):
    athltScrp(url)  # men's.. the comment's in here are for the first time around
    athltScrp(genderize(browser.current_url))  # women's
    athltScrp(schoolChng())  # girls
    athltScrp(genderize(browser.current_url))  # boys

while True:  # it keeps reloading the login page. will prefer to make it an if statement: if brows.find_elem does exist
    # then login, otherwise/else carry on
    try:
        # loginAth()
        break
    except selErr.NoSuchElementException:
        break

yearsToGet, maxAthlts = [str(year) for year in range(2015, 2020)] + ["2021"], 5000  # skipping 2020, how many from each?
browser.implicitly_wait(4)
# browser.quit()

# athltScrp(browser.current_url)  # just 1 pg
# athCalling(browser.current_url)  # just one year
# for year in yearsToGet:
#     yearChng(year)
#     athCalling(browser.current_url)

browser.minimize_window()
if pyinputplus.inputYesNo("quit?\n") == "yes":
    browser.quit()
