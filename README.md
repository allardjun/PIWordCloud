# Systems Biology PI Word Cloud generator

Automated text retrieval from PubMed, NIH Reporter, NSF Awards, processed using Python Natuaral Language Processing keyword extractors

## Quickstart

1. Edit the PI names in `PIList.xlsx`.

2. Run `drive_PIWordCloud.py`. This makes the word clouds

    * Calls 
        - `getSummaries_NIHReporter()`, `getSummaries_NSFAwardSearch()`, `getSummaries_PubMed()`
        - `get_keywords()`
        - `make_wordlcoud()`

3. Run `drive_vignettes`. This makes vignettes with the word cloud, optional lab photo, and PI name.

    * Calls `make_vignette()`

4. Run `merge_vignettes`. This combines the output of `drive_vignettes` into a single pdf.