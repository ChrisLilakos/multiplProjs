#! python3
# cheapMetTicks - seats 1-19, 109-126, 209-237, 313-325 of the next 5 games for under $30 bucks
from selenium import webdriver
from selenium.common import exceptions as selErr
from selenium.webdriver.common.keys import Keys as keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import logging, time, random, re  # , sys
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s -  %(message)s')
logging.disable()

# firefox *************************************************
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary  # if opening firefox only
# firefox_binary = FirefoxBinary(r"C:\Program Files\Firefox Developer Edition\firefox.exe")
#     # the target after right-click properties on the desktop icon
# browser=webdriver.Firefox(executable_path=r"C:\Users\chris\OneDrive\Desktop\geckodriver-v0.29.1-win64\geckodriver.exe"
#                             , firefox_binary=firefox_binary)
# edge ****************************************************
browser = webdriver.Edge(executable_path=r"C:\Users\chris\OneDrive\Desktop\edgedriver_win64\msedgedriver.exe")
    # "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
    # r"C:\Users\chris\OneDrive\Desktop\edgedriver_win64\msedgedriver.exe"
wait = WebDriverWait(browser, 20)  # timeout in seconds. for an explicit wait
browser.maximize_window()
goodSecs, pgStopNum = [list(range(1, 20)), list(range(109, 127)), list(range(209, 238)), list(range(313, 326))], 5
goodSecs, maxPrice = [secs for area in goodSecs for secs in area], 30  # good sections: 1-19, 109-126, 209-237, 313-325

# get the website, make sure the games you get links to are in NY and make sure there're upcoming games to begin w/, get
# the links to each game, send those links to another function. At the other function make sure it went to the correct
# page, make sure all the tickets are accessible thru the html, then get the raw data about the date, time, price, and
# section number. once you have that info you can see if it meets our standards if it does print dat bih owt. and when
# that's done go back to the og function for the next link
# --------------------
def ticketmasterTickPg(tickLink):
    browser.get(tickLink)
    time.sleep(random.randint(4, 8))
    # pre-getting section data
    sortBtn = browser.find_element_by_class_name("quick-picks__sort-button--unselected")
    if sortBtn.text != "Section":
        sortBtn = browser.find_element_by_class_name("quick-picks__sort-button--selected")
    sortBtn.click()
    time.sleep(random.randint(4, 8))
    scrollDiv = browser.find_element_by_class_name("quick-picks__listings-scroll")
    for i in range(15):  # so that it can load all the seats first. 15 might be overkill but i don't know
        scrollDiv.send_keys(keys.END)
        time.sleep(random.randint(8, 18))  # needs time to load
    # getting the sec(tions) info/data and seeing if it's gucch
    secLis = browser.find_elements_by_class_name("quick-picks__list-item")  # the list item with the seat and price info
    secRgx = re.compile(r"(sec[a-z ]*)(\d{1,3})", re.I)  # (,\srow .+) row rgx add-on. not including it atm doe
    for secInfo in secLis:
        secNum = int(re.findall(secRgx, secInfo.find_element_by_class_name("quick-picks__item-desc").text)[0][1])
        price = secInfo.find_element_by_class_name(
            "quick-picks__fees-block").find_element_by_class_name("quick-picks__button").text.strip("$ ea")
        if "," in price:
            price = price.replace(",", "")  # to avoid an error when converting to a float
        price = float(price)
        if secNum in goodSecs and price <= maxPrice:
            print(f"""Section {secNum} only goes for like ${price} each at the {browser.find_element_by_class_name(
                  'event-header__event-date').text} game biHtch!""")
def ticketmaster():
    browser.get("https://www.ticketmaster.com/new-york-mets-tickets/artist/805990?home_away=home")
    time.sleep(random.randint(4, 8))
    # double check the location's in ny. may not be necessary here cause its obvious by the ending of the link dat it is
    locBtn = browser.find_element_by_class_name("location-title")
    locSpan = locBtn.find_element_by_tag_name("span")
    assert ("NY" in locSpan.text.upper()) or ("new york" in str(locSpan.text).lower()), "ny != location"
    #
    # get the links to each game day's tickets
    linkStop, linkList = 0, []  # the a tags w/ ths txt list
    # if len(gmeLnks) > 0:  # if there even are any upcoming games
    try:
        gmeLnks = browser.find_elements_by_link_text("See Tickets")
    except selErr.NoSuchElementException:
        print("no upcoming games on ticket master")
        return  # sys.exit()
    for lnkTag in gmeLnks:
        if linkStop >= pgStopNum:  # i just want the next 5 games
            break
        linkList.append(lnkTag.get_attribute("href"))  # the links of the "see tickets" buttons
        linkStop += 1
    time.sleep(random.randint(4, 8))
    for link in linkList:  # take that link and go to it's page, milk the info then come back for the next one
        time.sleep(random.randint(4, 8))
        ticketmasterTickPg(link)
# ---------------------
def seatgeekTickPg(tickLink):
    browser.get(tickLink)
    time.sleep(random.randint(4, 8))
    gmeLis = browser.find_elements_by_css_selector('[data-test="event-listing"]')
    sectnRgx = re.compile(r"(Section\s)(\d{1,3})", re.I)  # (\s.\srow .+) row rgx optional add-on
    for seatSec in gmeLis:
        sectnNum = int(re.findall(sectnRgx, seatSec.find_element_by_css_selector('[data-test="section"]').text)[0][1])
        price = seatSec.find_element_by_tag_name("a").text.strip("$ /ea")
        if "," in price:
            price = price.replace(",", "")
        price = float(price)
        if sectnNum in goodSecs and price <= maxPrice:
            print(f"""Section {sectnNum} only goes for like ${price} each at the {browser.find_element_by_tag_name(
                'h2').text} game biHtch!""")  # there's 2 h2's but i'm hoping this one stays first in the html
def seatgeek():
    browser.get("https://seatgeek.com/new-york-mets-tickets")
    time.sleep(random.randint(4, 8))
    # double check the location's in ny
    locBtn = browser.find_element_by_css_selector('[data-test="geolocation-filter-button"]').text
        # or ('button[data-test="geolocation-filter-button"]'). if above dont work theres ish we gon hav to chng up
    assert ("NY" in locBtn.upper()) or ("new york" in locBtn.lower()), "ny != location"
    # may not need the above because
    try:
        for h6 in browser.find_elements_by_tag_name("h6"):  # just in case there's other h6's
            if "No nearby games" in h6.text:
                return print("no games here on seatgeek, dweak")
    except selErr.NoSuchElementException:
        pass
    # ge-in da links (no so-sage) byyyyy (doing):
    gmeLnks, linkStop, linkList = browser.find_elements_by_partial_link_text("at New York Mets"), 0, []
    for lnkTag in gmeLnks:
        if linkStop >= 5:  # may run into problems if more than 5
            break
        linkList.append(lnkTag.get_attribute("href"))
        linkStop += 1
    time.sleep(random.randint(4, 8))
    for link in linkList:  # i could alt-ly sent the list to the other function and have it cycle through there
        time.sleep(random.randint(4, 8))
        seatgeekTickPg(link)  # "https://seatgeek.com" +
# -----------------------
def mlbTicketsSiteTickPg(tickLink):
    browser.get(tickLink)
    time.sleep(random.randint(4, 8))
    # try:
    getUrl, schedUrl = browser.current_url(), "https://mpv.tickets.com/schedule"
    wrngPgMsg = (f"""linked to this page in error: {getUrl}. likely the page w/ the upcoming mets games. may look sumtin
    like: https://mpv.tickets.com/schedule/?agency=MLB_MPV&orgid=38129&tfl=New_York_Mets-tickets-New_York_Mets%3A_\
    Tickets%3A_Mets_Single_Game_Tickets-single_game_tickets-x0-Desktop-Landscape#/?view=list&includePackages=true""")
    if schedUrl == getUrl[:len(schedUrl)]:
        return print(wrngPgMsg, "ps: run a function for that site")  # delete later
        # if browser.find_element_by_class_name("mpv-application").tag_name == "body":
        #     print(wrngPgMsg, 1, sep=" ")
        #     return
        # elif browser.find_element_by_tag_name("mpv-schedule-page"):
        #     print(wrngPgMsg, 2, sep=" ")
        #     return
    # except selErr.NoSuchElementException:
    #     pass
    gmSecLis = browser.find_elements_by_class_name("section-row")
    for sitSec in gmSecLis:
        secNm = int(sitSec.find_element_by_css_selector('[translate="sectionList_LIST_PRIMARY"]').text)
        # as opposed to the class name route, cause then there'll be a lot more steps and the below may chng too
        price = sitSec.find_element_by_class_name("price-rg").text.strip("$")
        if "," in price:
            price = price.replace(",", "")
        price = float(price)
        if secNm in goodSecs and price <= maxPrice:
            print(f"""Section {secNm} only goes for like ${price} each at the {browser.find_element_by_class_name(
            'event-data').find_element_by_css_selector('[ng-if="!vm.isPackage && eventTime"]').text} game biHtch!""")
def mlbTicketsSite():
    browser.get("https://www.mlb.com/mets/tickets/single-game-tickets")
    time.sleep(random.randint(4, 8))
    try:
        if browser.find_element_by_class_name("p-alert__text"):  # if it exist in the page
            print(browser.find_element_by_class_name("p-alert__text").text)
            return print("no upcoming games here. it said -^")
    except selErr.NoSuchElementException:
        pass
    gmePgs, pgStop, pgList = browser.find_elements_by_class_name("p-button__link"), 0, []
    for href in gmePgs:
        if pgStop >= pgStopNum:
            break
        pgList.append(href.get_attribute("href"))
        pgStop += 1
    time.sleep(random.randint(4, 8))
    for pg in pgList:
        time.sleep(random.randint(4, 8))
        mlbTicketsSiteTickPg(pg)
# --***--
def mlbTickAlt(**luckTest):
    try:
        if len(luckTest) == 0:
            browser.get("https://mpv.tickets.com/schedule/?agency=MLB_MPV&orgid=38129")
        else:
            browser.get(luckTest)
        assert "technical difficulties" not in browser.find_element_by_tag_name("html").text, "ya lynx ned sum luk baiy"
    except selErr.InvalidArgumentException:
        return print("yah lynx ned sum luk baiy")
    time.sleep(random.randint(4, 8))
    try:
        noGmeTst = browser.find_element_by_id("eventsTabpanel")
        logging.debug(noGmeTst, noGmeTst.find_element_by_class_name("mpv-theme-primary-color"))
        if int(noGmeTst.find_element_by_class_name("mpv-theme-primary-color").text) == 0 or "No events" in noGmeTst.text:
            return print("dey ain't got no gaaaaaaammmessssssssssss doooooooeeeeeeeeee")
    except ValueError:
        pass
    gmeId, pgStop, pgList = browser.find_elements_by_css_selector('[fthook="scheduleEventList_eventListItem"]'), 0, []
        # or find_elements_by_class_name("mpv-panel-button").find elem by tag name (button)
    for id in gmeId:
        if pgStop >= pgStopNum:
            break
        pgList.append(id.get_attribute("eventid"))
        pgStop += 1
    time.sleep(random.randint(4, 8))
    for eId in pgList:
        time.sleep(random.randint(4, 8))
        mlbTicketsSiteTickPg("https://mpv.tickets.com/?agency=MLB_MPV&orgid=38129&pid=" + eId)
# ----------------------
def stubhubTickPg(hrefList):
    # i supposed looping thru the links here isn't the better idea since if we already had the game page link that we
    # wanted, we would have to put the it in a list before passing it directly to this function
    for tickLink in hrefList:  # oooo look im over here now
        browser.get(tickLink)
        browser.implicitly_wait(random.randint(6, 13))

        # gettinDwn = browser.find_element_by_class_name("ListingsFilter__scrollable_container")
        #     # ListingsFilter, EventRoyal__DesktopLayout__BodyContainer__RightRail, ListingsFilter__scrollable_container
        # gettinDwn.send_keys(keys.DOWN)  # .PAGE_DOWN
        browser.find_element_by_id("bestSeats").click()
        time.sleep(random.randint(4, 8))
        # instead of clicking the reset filter btn i chose to:
        feeSee = browser.find_element_by_css_selector('[aria-label="Show prices with estimated fees"]')
            # '[for="price-with-fees"]')  # id("price-with-fees")
        if feeSee.is_selected() == False:  # don't know whether to use isSelected or isEnabled
            feeSee.click()
        time.sleep(random.randint(4, 8))

        # if the link + f"?sid={the id number found in a attribute-less script tag in the
        # (JS?) sources tab --> stubhub.com folder --> {tickLink} subfolder --> '(index)' file or the html... maybe}"
        # scrollDis = browser.find_element_by_class_name(  # RoyalTicketList__container  # ---------************
        #     "EventRoyal__DesktopLayout__BodyContainer__LeftRail__AnimationContainer__TicketList")
        # scrollable class = RoyalTicketList__container
        # for i in range(50):
        browser.refresh()
        browser.implicitly_wait(random.randint(6, 13))
        scrllbleElem, lisElemClssNm = browser.find_element_by_class_name("RoyalTicketList__container"), 19
        b4ScrlElmHght = browser.execute_script(f"return arguments[0].scrollHeight", scrllbleElem)
        updtedHght = browser.execute_script(f"return arguments[0].scrollHeight", scrllbleElem) + 1
        while updtedHght != b4ScrlElmHght:
            updtedHght = browser.execute_script(f"return arguments[0].scrollHeight", scrllbleElem)
            b4ScrlElmHght = updtedHght
        #     print("before")
        #     scrollDis.send_keys(keys.ARROW_DOWN)
        #     print("after")
            scroll2bottom = f'''scrollOpts = {{left: 0, top: {b4ScrlElmHght}, behavior: 'smooth'}}'''
            #                                                             need to put extra () for some reason
            #       cant use browser.find_element_by_class_name(f"RoyalTicketListPanel__{lisElemClssNm}") for above.
            #         it needs a selenium 'locator' and not a selenium 'webElement'
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-wuz last here
            browser.implicitly_wait(random.randint(3, 5))  # replacement for time.sleep
            browser.execute_script(f'''document.getElementsByClassName("RoyalTicketList__container")[0].scrollTo({
            scroll2bottom})''')
            browser.implicitly_wait(random.randint(3, 5))  # explicit wait wasn't working and i don't have time so i
            #         moved on. maybe check out (link found after seaching "wait.until(expected_conditions.presence_of_
            #         element_located element found timeoutexception"): https://stackoverflow.com/questio
            #               ns/48940286/selenium-expected-conditions-select-element-with-multiple-attributes
            # browser.execute_script("return arguments[0].scrollIntoView(true);", browser.find_element_by_class_name(
            #     f"""RoyalTicketListPanel__{lisElemClssNm}"""))
            # try:
            #     # if updtedHght != b4ScrlElmHght:
            #     print(lisElemClssNm)
            #     # wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, f"""
            #     wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, f"""
            #        RoyalTicketListPanel__{lisElemClssNm}""")))  # although i ended up using this explicit wait instead
            # except selErr.TimeoutException:
            #     pass  # once everything is loaded the lisElemCl# is too large. but the height hasn't been updated.
            #     # if the update is put before it may not update correctly.
            # time.sleep(random.randint(8, 18))  # needs time to load
            # time.sleep(random.randint(4, 8))  # however i did put a range of fifty
            # time.sleep(random.randint(6, 13))  # but i commented out that loop for this prevHeight == newHeight thing
            updtedHght = browser.execute_script(f"return arguments[0].scrollHeight", scrllbleElem)
            # if updtedHght != b4ScrlElmHght:  # don't think this if stmt is necessary
            # lisElemClssNm += 20
        # wanted to do browser.execute_script("arguments[0].scrollIntoView();", browser.find_element_by_class_name("
        # RoyalTicketListPanel__{19 + (20 * n)}")) and n initialized at 0

        seatList = browser.find_elements_by_class_name("RoyalTicketListPanel")
        seatRgx, gdSeats, gmDate = re.compile(r"([a-z ]*)(\d{1,3})", re.I), 0, browser.find_element_by_class_name(
                    'event-info').text
        for seatInf in seatList:
            seatNm = int(re.findall(seatRgx, seatInf.find_element_by_class_name("RoyalTicketListPanel__SectionName")
                                    .text)[0][1])  # this class name may also works: .SectionRowSeat__sectionTitle
            price = seatInf.find_element_by_class_name("AdvisoryPriceDisplay__content").text.strip("$")
            if "," in price:  # avoids error if $1,000+ altho a try/except may work cuz we def wudn't buy @ those prices
                price = price.replace(",", "")
            price = float(price)
            if seatNm in goodSecs and price <= maxPrice:
                print(f"""Section {seatNm} only goes for like ${price} each at the {gmDate} game biHtch!""")
                gdSeats += 1
        if gdSeats == 0:
            print(f"sorry, no good seats for the {gdSeats} game")
        else:
            print(f'we got {gdSeats} good seats for this game')

def stubhub():
    browser.get("https://www.stubhub.com/new-york-mets-tickets/performer/5649/?pbH=h")
    time.sleep(random.randint(4, 8))
    try:
        if "No events" in browser.find_element_by_class_name("SearchNoResultsPanel").text:
            return print("hopes of a game here have been stubbed")
    except selErr.NoSuchElementException:
        pass
    # listin da links
    gmeLnks, linkStop, linkListFr = browser.find_elements_by_class_name("EventItem__TitleLink"), 0, []
    for lnkRef in gmeLnks:
        if linkStop >= pgStopNum:
            break
        linkListFr.append(lnkRef.get_attribute("href"))  # "https://www.stubhub.com" +
        linkStop += 1
    time.sleep(random.randint(4, 8))
    stubhubTickPg(linkListFr)
# ------------------------
# def razorgator():
    # browser.get("https://www.razorgator.com/new-york-mets-tickets/")  # decided not to do this one
# -------------------------

# ticketmaster()  # blocked
# seatgeek()  # worked
# mlbTicketsSite()  # denied
# mlbTickAlt()  # denied
stubhub()  # work in progress
