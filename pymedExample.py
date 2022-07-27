from pymed import PubMed

# Create a PubMed object that GraphQL can use to query
# Note that the parameters are not required but kindly requested by PubMed Central
# https://www.ncbi.nlm.nih.gov/pmc/tools/developers/
pubmed = PubMed(tool="MyTool", email="my@email.address")

# Create a GraphQL query in plain text
query = 'Enciso[Author - Last]'

# Execute the query against the API
results = pubmed.query(query, max_results=500)

# numResults=0
# for article in results:
#     if(article.title):
#         numResults=numResults+1
# print(numResults)

# Loop over the retrieved articles
for article in results:

    # Extract and format information from the article
    article_id = article.pubmed_id
    title = article.title
    if article.keywords:
        if None in article.keywords:
            article.keywords.remove(None)
            keywords = ""
        keywords = '", "'.join(article.keywords)
    publication_date = article.publication_date
    abstract = article.abstract

    # Show information about the article
    # print(
    #     f'- {publication_date} - {title}\nKeywords: "{keywords}"\n{abstract}\n'
    # )
    print(
        f'- {publication_date} - {title}\n{abstract}\n'
    )