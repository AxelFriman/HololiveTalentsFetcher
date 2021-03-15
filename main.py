from bs4 import BeautifulSoup
import urllib.request

fp = urllib.request.urlopen("https://virtualyoutuber.fandom.com/wiki/Hololive")
myBytes = fp.read()

html = myBytes.decode("utf8")
fp.close()

parsedHtml = BeautifulSoup(html)
tables = parsedHtml.findAll('table', attrs={'class': ['article-table style=', 'article-table style']})

i = 1

for table in tables:
    links = table.findAll('a')
    links_filtered = [link for link in links if not link.has_attr('class')]

    for link in links_filtered:
        fp = urllib.request.urlopen("https://virtualyoutuber.fandom.com" + link.attrs['href'])
        myBytes = fp.read()

        wikiPage = myBytes.decode("utf8")
        fp.close()

        parsedWikiPage = BeautifulSoup(wikiPage)
        affiliation = parsedWikiPage.find('div', attrs={'data-source': 'affiliation'})

        if 'formerly' in str(affiliation) or 'China' in str(affiliation):
            continue

        channelDiv = parsedWikiPage.find('div', attrs={'data-source': 'channel'}).find('div').find('a')

        if 'Aloe' in str(channelDiv):
            continue

        linkEnding = 'videos' if (channelDiv.attrs['href'][-1] == '/') else '/videos'
        if 'youtube' in channelDiv.attrs['href']:
            print('{' + '"followId": ' + str(i) + ',' + '"linkToVideosPage": "' + channelDiv.attrs['href'] + linkEnding
                  + '","channelName": "' + channelDiv.text + '"},')
            i += 1
