

1- BingSearch.ipynb
    - This code uses the Bing Web Search API to retrieve search results for "Firm_Name + Field" and stores this in a sqlite database "firms_web_search_results.db".

2- WebscraperForBingResults.ipynb
    - This code uses selenium and requests to scrape the contents of the top 5 websites found in the bing web search results for each Firm_Name and Field. It reads in data from "firms_web_search_results.db" and stores website scraping results in "firms_web_search_website_scrapings.db".
    - It will skip over fields that are already populated

3- Gemini Database Builder
    - Read in data from firms_web_search_results.db and firms_web_search_website_scrapings.db and feed these into Gemini API.