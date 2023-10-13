from cloudscraper import create_scraper
from bs4 import BeautifulSoup
from texttable import Texttable


def get_latest_update(tracking_id):
    scraper = create_scraper()
    res = scraper.get(f"https://bluedart.com/trackdartresultthirdparty?trackFor=0&trackNo={tracking_id}")
    if res.status_code == 200 and "Status and Scans" in res.text:
        soup = BeautifulSoup(res.text, "html.parser")
        tr = [x for x in soup.find_all("div", {'class': 'table-responsive'}) if "Status and Scans" in x.text][0].find(
            "tbody").find("tr")
        data = [x.text for x in tr.find_all("td")]
        table = Texttable()
        table.set_deco(Texttable.VLINES)
        table.header(["Hub", "Shipment Status", "Date", "Time"])
        table.add_row(data)
        # print  html markup for this table

        return table.draw()
    else:
        return False

