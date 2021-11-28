from typing import List
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import sys
import urllib.error
import ssl



def get_links(url: str) -> list:
    """Find all links on page at the given url.
    Returns:
        a list of all unique hyperlinks on the page,
        without page fragments or query parameters.
    """
    browser: WebDriver = webdriver.Chrome('/Users/pattananprarom/Downloads/chromedriver')
    browser.get(url)
    all_link = browser.find_elements('tag name', 'a')
    all = []
    for link in all_link:
        url = link.get_attribute('href')
        if url == None:
            continue
        if '#' in url:
            url = url.split('#')[0]
        if '?' in url:
            url = url.split('?')[0]
        all.append(url)
    all = list(dict.fromkeys(all))
    return all


def is_valid_url(url: str) -> bool:
    """Check if the url is valid and reachable.

    Returns:
        True if the URL is OK, False otherwise.
    """
    try:
        urllib.request.Request(url, method="HEAD")
        urllib.request.urlopen(url)
        return True
    except urllib.error.HTTPError:
        if urllib.error.HTTPError.code != 403:
            return False
        return True


def invalid_urls(urllist: List[str]) -> List[str]:
    """Validate the urls in urllist and return a new list containing
    the invalid or unreachable urls.
    Returns:
        A new list containing only the invalid or unreachable URLs from the parameter list.
    """
    invalid_list = []
    for i in urllist:
        if not is_valid_url(url):
            invalid_list.append(i)
    return invalid_list


if __name__ == "__main__":
    import sys
    import os
    ssl._create_default_https_context = ssl._create_unverified_context
    filename = os.path.basename(sys.argv[0])
    num_args = len(sys.argv)
    if num_args != 2:
        print(f"Usage:  python3 Usage:  python3 link_scan.py url.")
        sys.exit()
    url = sys.argv[1]

    url_list = get_links(url)
    for url in url_list:
        print(url)
    print("\nBad Links:")
    for url in invalid_urls(url_list):
        print(url)