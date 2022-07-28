from pymed import PubMed

def getSummaries_PubMed(PIName):

    # Create a PubMed object that GraphQL can use to query
    # Note that the parameters are not required but kindly requested by PubMed Central
    # https://www.ncbi.nlm.nih.gov/pmc/tools/developers/
    pubmed = PubMed(tool="PhDProgramDirectoryMaker", email="jun.allard@uci.edu")

    # Create a GraphQL query in plain text
    queryTemplate = '((Irvine[Ad]) AND ("2017/01/01"[Date - Create] : "3000"[Date - Create])) AND ({thisPIName}[Author])'
    query=queryTemplate.format(thisPIName=PIName)

    # Execute the query against the API
    results = pubmed.query(query, max_results=500)


    # Loop over the retrieved articles
    text = []
    allKeywords = []
    for article in results:

        # Extract and format information from the article
        article_id = article.pubmed_id
        title = article.title
        if article.keywords:
            if None in article.keywords:
                article.keywords.remove(None)
            keywords = '", "'.join(article.keywords)
            allKeywords.append(article.keywords)
        publication_date = article.publication_date
        abstract = article.abstract

        # Show information about the article
        # print(
        #     f'{publication_date} - {title}\nKeywords: "{keywords}"\n{abstract}\n'
        # )

        # load into text string
        text.append(title)
        text.append(abstract)
        text.append(keywords)

    #print(text) 
    return text, allKeywords

if __name__ == "__main__":
    getSummaries_PubMed("Lander")