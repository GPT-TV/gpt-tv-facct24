# gpt-tv-facct24

## Associated Research Paper: [Auditing GPT's Content Moderation Guardrails: Can ChatGPT Write Your Favorite TV Show?](https://dl.acm.org/doi/10.1145/3630106.3658932)

## SCHEMA

| Column Name | Source   | Explanation |
|---|---|---|
| index       | -   | \[0..1392\] Unique Identifier per Episode     |
| show-name   | IMDb    | Name of TV Show       |
| episodes-link     | IMDb    | URL of Episode's IMDb Page  |
| episode-name    | IMDb    | Title of Episode       |
| director    | IMDb    | List of Episode's Director(s)   |
| age-rating       | IMDb    | Official US Age Rating (TV-PG, TV-14, TV-MA)   |
| release-date       | IMDb    | US Release Date       |
| clean-tags       | IMDb    | List of User-generated Episode Tags     |
| clean-genres       | IMDb   | List of Episode's Genre(s)      |
| characters       | IMDb    | List of Main Characters in Episode       |
| stars       | IMDb   | List of Main Actors in Episode (max 3)     |
| writers       | IMDb   | List of Episode's Writer(s)     |
| wiki-urls       | Wikipedia   | URL of Episode's Wikipedia Page      |
| short-imdb-descs       | IMDb    | Short Synopsis (~1-3 sentences)       |
| wiki-descs       | Wikipedia    | Medium Synopsis (~1-3 paragraphs)     |
| long-imdb-descs     | IMDb    | Long Synopsis (~1-3 pages)      |
| cleaned-short-imdb-descs       | IMDb    | Anonymized Short Synopsis     |
| cleaned-wiki-descs     | Wikipedia   | Anonymized Medium Synopsis   |
| cleaned-long-imdb-descs    | IMDb    | Anonymized Long Synopsis        |
| API_response_short_descs      | GPT API\*   | List of GPT Responses for Short Synopsis Prompt       |
| API_response_wiki_descs     | GPT API\*    | List of GPT Responses for Medium Synopsis Prompt  |
| API_response_imdb_descs     | GPT API\*    | List of GPT Responses for Long Synopsis Prompt  |
| ME_short_descs_prompt | GPT API - `text-moderation-006` | List of Moderation Endpoint Outputs for Short Synopsis **Prompt** |
| ME_wiki_descs_prompt | GPT API - `text-moderation-006` | List of Moderation Endpoint Outputs for Short Synopsis **Prompt** |
| ME_imdb_descs_prompt | GPT API - `text-moderation-006` | List of Moderation Endpoint Outputs for Short Synopsis **Prompt** |
| ME_short_descs | GPT API - `text-moderation-006` | List of Moderation Endpoint Outputs for Short Synopsis **GPT Response**\*\* |
| ME_wiki_descs | GPT API - `text-moderation-006` | List of Moderation Endpoint Outputs for Medium Synopsis **GPT Response**\*\* |
| ME_imdb_descs | GPT API - `text-moderation-006` | List of Moderation Endpoint Outputs for Long Synopsis **GPT Response**\*\* |

\*for the file labeled _-3.5.csv_, the model used is GPT-3.5 (`gpt3.5-turbo-1106`), and for the file labeled _-4.0.csv_, the model used is GPT-4.0 (`gpt-4.0-1106-preview`).

\*\*in file labeled _-3.5.csv_, this list includes repeated runs of the ME on both the first and the second GPT API response from the `API_response_short_descs`, `API_response_wiki_descs`, and `API_response_imdb_descs` columns.

## COLLECTION & PREP
Shows selected from IMDb's [Top 100 TV Shows of All Time](https://web.archive.org/web/20231104142125/https://www.imdb.com/list/ls095964455/) list. This dataset contains each episode in S1 of each of these 100 shows, with a total of 1,392 unique episodes. Further information about data collection, anonymization, and preparation is discussed in [the associated paper](https://dl.acm.org/doi/10.1145/3630106.3658932).

See **Figure 1** below for a clear outline of the audit pipeline, lifted from [the associated paper](https://dl.acm.org/doi/10.1145/3630106.3658932).

![Figure 1](https://github.com/GPT-TV/gpt-tv-facct24/assets/10174767/4777cd07-a610-44b9-bc1f-e36d998db456)

## FILESTRUCTURE

## HOW TO RUN AUDIT

## CITATION

Yaaseen Mahomed, Charlie M. Crawford, Sanjana Gautam, Sorelle A. Friedler, and Danaë Metaxa. 2024. Auditing GPT's Content Moderation Guardrails: Can ChatGPT Write Your Favorite TV Show? In Proceedings of the 2024 ACM Conference on Fairness, Accountability, and Transparency (FAccT '24). Association for Computing Machinery, New York, NY, USA, 660–686. https://doi.org/10.1145/3630106.3658932
