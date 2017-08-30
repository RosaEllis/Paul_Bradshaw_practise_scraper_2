###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html 

# scrape_table function: gets passed an individual page to scrape. Root is a variable just for this function (I think
#... inside functions variables don't have to be made with the equals sign, it just knows it's a variable 
def scrape_table(root):
    # cssselect 
    rows = root.cssselect("table.data tr")  # selects all <tr> blocks within <table class="data">
    for row in rows:
        # Below sets up a dictionary that is inside the variable called record, so we can put info inside it 
        record = {}
        # below 
        table_cells = row.cssselect("td")
        if table_cells: 
            record['Artist'] = table_cells[0].text
            record['Album'] = table_cells[1].text
            record['Released'] = table_cells[2].text
            record['Sales m'] = table_cells[4].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Artist"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    # below scrapes the page from the url you give it as an argument, and puts it in the variable called html
    html = scraperwiki.scrape(url)
    # below just prints out the html
    print html
    # below a function called fromstring, which is from the library lxml.html, takes the url which is inside the 
    #... variable html and turns it into an xml object, and that xml object is now inside the variable called root 
    root = lxml.html.fromstring(html)
    # below the funcion called scrape_table, which was defined above, takes the scraped html page as an xml object and carries out the function on it 
    scrape_table(root)
    # below takes root.cssselect 
    next_link = root.cssselect("a.next")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'https://paulbradshaw.github.io/'
starting_url = urlparse.urljoin(base_url, 'scraping-for-everyone/webpages/example_table_1.html')
scrape_and_look_for_next_link(starting_url)
