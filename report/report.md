---
author: "Jack Henschel, Rohit Raj, Eelis Kostiainen"
title: "Harvesting Tables In The Wild"
date: 2021-01-10
lang: en-US
papersize: a4
documentclass: article
titlepage: true
code-block-font-size: '\footnotesize'
fontsize: 11pt
logo: "images/tree.png"
logo-width: 200
title-page-rule-color: "000081"
toc: true
toc-own-page: true
numbersections: true
---

# Introduction

<!-- An introduction to the general topic, current interest etc. -->

The world wide web is full of information. Already the number of web pages indexed by search engines is more than 5 billion [2].
The information on these web pages is mostly aimed at solely human consumption, which at the same time makes it very difficult to be automatically processed by machines.
While plain text data (such as regular HTML websites) are still comprehendible by machines, with complex layouts and designs it becomes increasingly difficult for a machine to access this data in a meaningful way - in the end, we want to turn data into information.

One such example are HTML tables. From human perspective they are intuitively easy to understand (just by looking at them), but for a machine they are difficult to assess because of the graphical nature of them: all the little visual details (such as delimiters and orientation) matter a lot.
At the same time, the tables themselves usually just contain the data (e.g. statistics), while the surrounding text (headers, captions and description) gives this data meaning.
For example, the information pair "TSLA, 2007-12-03, 1234" is useless if we do not know that we are dealing with stock prices.

As we will outline in Section 2, there has already been significant academic work in the field of semantic table interpretation.
To develop, compare and optimize these systems however, large datasets are required.
Therefore, the goal of our semester project has been the design and development of a system that collects tables
from HTML on pages on the web.
In Section 3 we detail the development and design choices of this system.
...
Finally, in Section 5 we provide additional suggestions on how the system should be improved and extended.

# Related work

In this section we will give an overview of background literature and related work.

**TODO** *Give a brief overview of the papers we have studied, especially the ones from the literature review presentation*

## Datasets

Macdonald and Barbosa have produced one of the most recent public corpora of web tables.
More specifically, their research introduces a publicly available dataset [^macdonald] for benchmarking information extraction from HTML tables.

[^macdonald]: [https://dataverse.library.ualberta.ca/dataset.xhtml?persistentId=doi:10.7939/DVN/SHL1SL](https://dataverse.library.ualberta.ca/dataset.xhtml?persistentId=doi:10.7939/DVN/SHL1SL)

## Semantic Table Interpretation

Table interpretation is the act of giving semantic meaning to raw table data.
Among many other steps, this includes determining the data types of columns, the semantic object entities of each column and the relations between columns.

Ritze et al. have developed an algorithm to match HTML tables to DBpedia [7].
The "T2K Match" algorithm is an iterative matching method combining schema and instance matching for matching mostly small and narrow HTML tables against cross-domain knowledge bases.
The source code for this matching system is publicly available [^t2k]
Associating the table cells to semantic entities in knowledge bases greatly helps machines to deal with the logic of tables.

[^t2k]: [https://github.com/T2KFramework/T2K](https://github.com/T2KFramework/T2K)

More recently, Chabot et al. have described a similar system named "DAGOBAH" [8].
DAGOBAH semantically annotates tables with entities either from Wikidata or DBpedia.
It does this by determining the column types as well as performing cell and column annotation and relationship identification.
The system delivered promising results in the "Tabular Data to Knowledge Graph Matching" challenge [8], therefore we will be using it to annotate the tables in our processing pipeline.
Furthermore, we had access to an API of this system in private beta as part of the Orange API [^orangeAPI].

[^orangeAPI]: [https://developer.orange.com/products/all-apis/](https://developer.orange.com/products/all-apis/)

# System requirements and design

<!-- What we were planning to do (initial goals), an overview of our system and explanation of the design choices. -->

This section gives a high-level overview of the table collection pipeline we have designed and built.
Specific implementation details will be outlined in Section 3.

![System architecture](images/archi.png)

Our pipeline consists of three main components: Scrapy Spiders (CommonCrawl and Web Spider) for downloading web pages, Kafka message queue for buffering extracted tables and ArangoDB database for storing them.
To integrate these individual components, we have developed services to integrate them: an ingestion service for taking items from the message queue, performing annotations and inserting them into the database; and post-processing service for performing processing on the entire dataset (e.g. creating a graph structure).

We opted for the Python programming language for our implementation because it very well suited for the task of crawling web pages.
Its flexibility and loose typing make it very convenient to deal with arbitrary and unformatted data.
Finally, it has many excellent open source libraries available.

For the crawling itself, we decided to use the open-source Scrapy application framework [^scrapy]. It not only crawls the webpages using the spiders, but also has built-in support for web-page parsing with parsel [^parsel].
This is in contrast with the libraries such as BeautifulSoup [^beautiful-soup] that only support parsing.

Scrapy provides well thought-out scaffolding and project structure for each of its main components: spiders (modules for crawling web pages), middlewares (modules for modifying and discarding requests) and items (the pipeline result).
Since all of them are combined into a pipeline by Scrapy's "engine", they are running in parallel and independent from each other.
Furthermore, for each of these components either project-level (download speed, parallel connections etc.) or individual settings (e.g. log verbosity) can be applied.

![Scrapy Architecture, *Scrapy Documentation*](images/scrapy_architecture_02.png)

[^scrapy]: [https://scrapy.org/](https://scrapy.org/)
[^parsel]: Parsel is a library to extract individual elements of web pages with XPath or CSS selectors.
[^beautiful-soup]: [https://www.crummy.com/software/BeautifulSoup/](https://www.crummy.com/software/BeautifulSoup/)

Messages queues are extensively used for asynchronous communication. A message queue serves as a buffer, meaning that the crawler is never slowed down by a slow ingestion rate (e.g. due to high load on the database).
Moreover, as the ingestion service (consumer) is not interacting directly with the crawler (producer), it does not become a bottleneck and allows the ingestion service to process items out of the message queue at any speed.
This gives the ingestion service more headroom to perform time consuming tasks, such as augmenting the tables with data obtained from external APIs.

Our preferred choice of message queue was Kafka [^kafka] as it is one of the most popular message queue systems and is extensively used for distributed _event_ streaming services.
Kafka follows a log-commited approach for message bus and hence can also be used as a temporary store of messages for a desirable unit of time.
This is unlike other message queues, such as RabbitMQ [^rabbit-mq], that cannot store any message in case of a database failure.

Since we were using containerized Kafka images, it was also easy to control the topics, replication of topics and partitions using the environment variables instead of using an admin API.

[^kafka]: https://kafka.apache.org/
[^rabbit-mq]: https://www.rabbitmq.com/

<!-- DONE: What was the motivation for using ArangoDB (while the Kibana stack is generally associated with ElasticSearch)? -->
Finally, we decided use ArangoDB as our storage backend [^arangodb].
Unlike other NoSQL databases, ArangoDB natively supports multiple data models: document store, graph store and full-text search.
This means it combines the capabilities of databases such as MongoDB, Neo4j and Elasticsearch all into one database [12].
This is excellent for quick prototyping, because it allows us to focus on the data collection and ingestion first, and later we can explore various ways of accessing and analyzing the data.

[^arangodb]: [https://www.arangodb.com](https://www.arangodb.com)

## Monitoring Infrastructure

In addition to the web table harvesting system, we also deployed a parallel monitoring infrastructure for a proper log monitoring and visualization. This infrastructure was based on the popular ELK stack i.e. Elasticsearch, Logstash, and Kibana. ELK stack is a popular platform to analyze and visualize logs from multiple sources in real time.

![Monitoring architecture](images/elk.png)

Monitoring infrastructure components:

* Logspout: used for docker logs redirection to logstash.
* LogStash: used for log aggregation
* Elasticsearch: used for indexing and storage
* Kibana: used for analytics and visualization


# Implementation and Milestones

After familiarizing ourselves with the topic and having studied the relevant literature, we began designing and implementing our data processing pipeline.
This section will cover our implementation and the milestones we have completed in the course of our semester project.

## Basic crawling and table extraction

The first significant milestone we reached was the basic crawling of web pages (i.e. downloading the HTML contents) and extracting the HTML tables.
At this stage, our tool would simply take a list of URLs, download and parse these pages and finally store the results in a JSON file.

<!-- TODO: What library, if any, did you use to actually perform the table extraction (or was it coded from scratch)? Does Scrapy only manage the crawling part?  -->

## Advanced table parsing

The next big step was implementing advanced table extraction and parsing algorithms.
In particular, we decided to use two different algorithms for parsing tables on Wikipedia pages and the rest of the web pages.
This decision was made because Wikipedia pages follow a much stricter format than the average table on the web.
**TODO** @eelisk *Expand on the Wikipedia algorithm*

Based on the literature we studied previously, we identified and implemented several important criteria which allow us to collect tables with meaningful content:

* ignore layout tables (table used for designing the webpage)
* ignore tables irregular bodies (number of rows and columns varies)
* ignore small tables (table with less than two rows)

As mentioned in the introduction, the value of information inside a table is not only embedded in the table itself, but also in the context.
Thus, we wanted to collect as much contextual information as possible.
To this end, we also implemented algorithms the extract the following information from the web page:

* Page title
* Table title
* Paragraph before / after the table
* Most frequent terms
* Language of the page

To make sure our algorithms work correctly and we don't accidentally introduce any regressions, we also added unit and integration tests for our code.
The unit tests are testing small pieces of separate functionality (such as text extraction, cleaning and normalization), while the integration tests make sure that when we input a particular HTML page into our pipeline, we always obtain the same parsed result on the other end.

## Data format

<!-- DONE: What was the design decision for the JSON metadata format for representing the table metadata and content? Clearly, you have been influenced by the WDC format, http://webdatacommons.org/webtables/2015/downloadInstructions.html ... what else?  -->

By now, we were collecting many different pieces of information and had to come up with data format to store this data in.
We evaluated several data formats that have already been used in other projects.
Initially, we also considered using a storage format suitable for very large datasets, in particular Apache Avro, but decided against due to the difficulty of dealing with binary formats.
Furthermore, since we were planning to build a pipeline for table collection, a plaintext format that is easily serializable seemed more suitable for our purposes.
Despite these requirements, we still had several contenders:

* TableNet (JSON based) [3]
* DWTC Dresden Web Table Corpus (JSON based) [4]
* WTC Web Table Corpora (JSON based) [5]
* W3C CSV [6]

After comparing these options, we decided that the W3C CSV format is not suitable, because information about a single table is stored in multiple CSV files (one file for the table content, additional files for the metadata).
This would increase the complexity of our data pipeline significantly.

Since the WTC format is based on the DWTC format, the DWTC seemed to be a widely used and proven data format.
We also considered the attributes it contained relevant to our use case, but at the same time decided to extend it with additional metadata and also incorporate some fields from the TableNet format.
We hope that this common choice will enable others to easily reuse parts of our pipeline or the data.

To document our final data format and make sure our own application adheres to it, we created a JSON schema definition (Appendix TODO).

## Common Crawl

In addition to crawling pages from the world wide web, we also wanted to explore using the CommonCrawl dataset \cite{}.
**TODO** @rohitshubham *Explain what the CC is and how we use it*

## First crawl

<!-- TODO: When you go over a page which has been previously crawled, do you have mechanism to detect changes on the page or not?  -->

Approximately three months after the start of the project, we conducted a first, short test run of our table collection pipeline.
This was to make sure the components we had developed and integrated so far all worked correctly and could sustain operating for a prolonged period of time.
During the 8 hours run, we collected 22.000 tables from 5156 webpages on 153 unique domains.

```
db._query(`RETURN LENGTH(parsed_tables)`).toArray()[0];
> 22909

db._query(`FOR t in parsed_tables RETURN t.url`).toArray()\
  .filter((v, i, a) => a.indexOf(v) === i).length;
> 5156

db._query(`FOR t in parsed_tables RETURN t.url`).toArray()\
  .map(function(url) { return url.split("/")[2]; })\
  .filter((v, i, a) => a.indexOf(v) === i).length;
> 153
```

An in-depth look at the collected data revealed that our pipeline worked as intended.
The spider component downloaded web pages and extracted tables from them.
Occasionally, there were errors as websites were not reachable anymore (dead links).
The extracted table items were sent through the message queue and inserted into the database by our ingestion service.

This initial crawl was seeded with just a handful of URLs and therefore the content of the visited pages was heavily skewed towards certain topics.
This was not an issue however, since meaningful data collection was not en explicit goal of our first test.

## Crawling strategy

After analyzing the results from our first crawl, we had to (d/r)efine our crawling strategy.

*TBD*

* Seed URLs
* Domain blacklist
* Two-tier crawling strategy
* No re-crawling of visited web pages

## Visualization

<!-- Describe visualization and exploration in the arangodb dashboard. -->

With these first results, we started exploring the graph capabilities of the ArangoDB backend.
Until now we used the database only as a simple document store.

In ArangoDB, documents stored in a regular *collection* ("database table") act as *vertices* ("nodes").
In order to leverage the graph capabilities, we need insert additional documents into *edge collection*.
An edge document has at least two keys: `_from` and `_to`, which describe a directed edge from one vertex to another.
The value of these keys are the IDs of the vertex documents.

The following figure is an such a vertex document.
The `_id`, `_key` and `_rev` fields are database internals.
Additionally, in this example we used a `type` key to distinguish different types of edges.


```
{
  "_id"   : "htw_edges/40320",
  "_key"  : "40320",
  "_rev"  : "_btUZfLu---",
  "_from" : "visited_pages/40317",
  "_to"   : "parsed_tables/8787",
  "type"  : "page-contains"
}
```

In a post-processing step we establish the edges between all the relevant documents (tables and pages) we have previously collected.
Then, we can explore this graph programmatically with the Arango Query Language (AQL) or visually through the Arango Dashboard.

![Simple Graph in Arango Dashboard](images/simple-graph.png)

In Figure 1, the violet circles represent page vertices (a webpage that has been crawled), while the black vertices represent table vertices (a table that has been collected).
The virtual start node is "HTW Start" (where the crawl started), but this can adjusted through the UI to start traversing the graph.
Alongside the edges the edge type is displayed, in this example either "hyperlink" (one webpage links to another webpage) or "page-contains" (a table is embedded on a webpage).
The search depth and maximum number of nodes displayed in the graph can be dynamically adjusted in the UI to facilitate the exploration, though loading large graphs at all once breaks the visualization and has performance issues.

**TODO** *Once we have the table topics, do the same thing for them*

## Topic annotation

(*TBD*) with Orange API.

# Results

What we managed to do and why/how it could be useful (and what we didn't achieve and why).

# Future work

<!-- How the work we have done so far can be continued or improved. -->

For future work, the first would be measuring the current performance of the system.
For this task a dataset, such as the one released by Macdonald and Barbosa, could be used to measure the extraction and detection accuracy of the system.
However, this would first require a data format compatibility study.

Once these level of system performance has been captured, the table filtering and extraction algorithms implemented so far can be improved upon.
In particular, the works from Ritze et al. [7] as well as Eberius et al. [11] should serve as an excellent starting point for these optimizations.

Finally, the crawling strategy used for downloading pages from the world wide web should be tweaked. While a basic mechanism to avoid crawling the same URL multiple times has been implemented, websites have become very complex today and often host the same content on multiple distinct URLs. The knowledge that has been gained through search engine (and search engine optimization) in the last 15 years should be drawn upon.


At the same time, another interesting avenue for research is purposely re-visiting pages that have been crawled before, to check for updates made to those pages.

\clearpage

# References

[1] Hassan, Md Imrul, Hai L. Vu, and Taka Sakurai. *"Performance analysis of the IEEE 802.11 MAC protocol for DSRC safety applications."* IEEE Transactions on vehicular technology 60.8 (2011): 3882-3896.

[2] https://www.worldwidewebsize.com/

[3] https://github.com/bfetahu/wiki_tables/tree/master/data

[4] https://wwwdb.inf.tu-dresden.de/misc/dwtc/schema.json

[5] http://webdatacommons.org/webtables/#results-2015

[6] https://www.w3.org/TR/tabular-data-primer/

[7] https://dl.acm.org/doi/10.1145/2797115.2797118

[8] http://ceur-ws.org/Vol-2553/paper6.pdf

[9] http://ceur-ws.org/Vol-2775/

[10] Macdonald, Erin; Barbosa, Denilson, 2019, "An Annotated Corpus of Webtables for Information Extraction Tasks", https://doi.org/10.7939/DVN/SHL1SL, UAL Dataverse, V2

[11] J. Eberius, K. Braunschweig, M. Hentsch, M. Thiele, A. Ahmadov and W. Lehner, "Building the Dresden Web Table Corpus: A Classification Approach," 2015 IEEE/ACM 2nd International Symposium on Big Data Computing (BDC), Limassol, 2015, https://doi.org/10.1145/2791347.2791353

[12] https://www.arangodb.com/resources/white-paper/multi-model-database/

# Appendices

## JSON schema definition

\lstinputlisting[basicstyle=\scriptsize\ttfamily]{../data/schema.json}
