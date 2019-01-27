import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchAll,searchSiteID):
    url = PAsearchSites.getSearchSearchURL(searchSiteID) + searchTitle.lower().replace(" ","-").replace("'","-")
    searchResults = HTML.ElementFromURL(url)

    searchResult = searchResults.xpath('//div[@class="details col-sm-6 col-md-3 order-md-2 mb-2"]')[0]
    titleNoFormatting = searchResult.xpath('.//div[@class="row"]//div[@class="col-6 col-md-12"]//h1')[0].text_content()
    Log("Result Title: " + titleNoFormatting)
    curID = searchTitle.lower().replace(" ","-").replace("'","-")
    Log("CurID: " + curID)
    releasedDate = searchResult.xpath('.//div[@class="row"]//div[@class="col-6 col-md-12"]//p')[0].text_content()

    girlName = searchResult.xpath('.//div[@class="row"]//div[@class="col-6 col-md-12"]//a')[0].text_content()

    lowerResultTitle = str(titleNoFormatting).lower()

    titleNoFormatting = girlName + " - " + titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(searchSiteID) + ", " + releasedDate +"]"
    score = 100
    results.Append(MetadataSearchResult(id = curID + "|" + str(searchSiteID), name = titleNoFormatting, score = score, lang = lang))
    return results


def update(metadata,siteID,movieGenres,movieActors):
    temp = str(metadata.id).split("|")[0]

    url = PAsearchSites.getSearchSearchURL(siteID) + temp
    Log('scene url: ' + url)
    detailsPageElements = HTML.ElementFromURL(url)

    if (siteID >= 308 and siteID <= 327):
        metadata.studio = "Porn Pros"
    else:
        metadata.studio = PAsearchSites.getSearchSiteName(siteID)
    Log("Studio: " + metadata.studio)

    # Collections / Tagline
    siteName = PAsearchSites.getSearchSiteName(siteID)
    Log("Site Name: " + siteName)
    metadata.collections.clear()
    metadata.tagline = siteName
    metadata.collections.add(siteName)
    if metadata.tagline != metadata.studio:
        metadata.collections.add(metadata.studio)

    # Actors
    movieActors.clearActors()
    titleActors = ""
    actors = detailsPageElements.xpath('//div[@class="details col-sm-6 col-md-3 order-md-2 mb-2"]//div[@class="row"]//div[@class="col-6 col-md-12"]//a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content()
            actorPhotoURL = PAactors.actorDBfinder(actorName)
            titleActors = titleActors + actorName + " & "
            Log("actorPhoto: " + actorPhotoURL)
            movieActors.addActor(actorName,actorPhotoURL)
        titleActors = titleActors[:-3]

    # Genres
    movieGenres.clearGenres()
        # Based on site
    if siteName.lower() == "Lubed".lower():
        for genreName in ['Lube', 'Raw', 'Wet']:
            movieGenres.addGenre(genreName)
    elif siteName.lower() == "Holed".lower():
        for genreName in ['Anal', 'Ass']:
            movieGenres.addGenre(genreName)
    elif siteName.lower() == "POVD".lower():
        for genreName in ['Gonzo', 'POV']:
            movieGenres.addGenre(genreName)
    elif siteName.lower() == "MassageCreep".lower():
        for genreName in ['Massage', 'Oil']:
            movieGenres.addGenre(genreName)
    elif siteName.lower() == "DeepThroatLove".lower():
        for genreName in ['Blowjob', 'Deep Throat']:
            movieGenres.addGenre(genreName)
    elif siteName.lower() == "PureMature".lower():
        for genreName in ['MILF', 'Mature']:
            movieGenres.addGenre(genreName)
    # Based on number of actors
    if len(actors) == 3:
        movieGenres.addGenre('Threesome')
    if len(actors) == 4:
        movieGenres.addGenre('Foursome')
    if len(actors) > 4:
        movieGenres.addGenre('Orgy')

    # Posters
    background = "https:" + detailsPageElements.xpath('//video[@id="player"]')[0].get('poster')
    Log("BG DL: " + background)
    metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    metadata.posters[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    # Date
    date = detailsPageElements.xpath('//div[contains(@class,"details")]//p')[0].text_content()
    Log('Date: ' + date)
    date_object = datetime.strptime(date, '%B %d, %Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Title
    sceneTitle = detailsPageElements.xpath('//div[contains(@class,"details")]//h1')[0].text_content()
    metadata.title = siteName + " - " + sceneTitle

    return metadata