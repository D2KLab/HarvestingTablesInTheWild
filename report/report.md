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
---

## Introduction

An introduction to the general topic, current interest etc.

The world wide web is full of information. Already the number of web pages indexed by search engines is more than 5 billion [2].
The information on these web pages is mostly aimed at solely human consumption, which at the same time makes it very difficult to be automatically processed by machines.
Plain text data (such as regular HTML websites) are still comprehendable by machines, but with complex layouts and designs it becomes increasingly difficult for a machine to access this data in a meaningful way - in the end, we want to turn data into information.

One such example are HTML tables. From human perspective they are intuitively easy to understand (just by looking at them), but for a machine they are difficult to assess because of the graphical nature of them: all the little visual details (such as delimiters and orientation) matter a lot.
At the same time, the tables themselves usually just contain the data (e.g. statistics), while the surrounding text (headers, captions and description) gives this data meaning.
For example, the information pair "TSLA, 2007-12-03, 1234" is useless if we do not know what we are dealing with stock prices.

As we will outline in Section 2, there has already been significant academic work in the field of semantic table interpretation.
To develop, compare and optimize these systems however, large datasets are required.
Therefore, the goal of our semester project has been the design and development of a system that collects tables
from HTML on pages on the web

## Related work

In this section we will give an overview of background literature and related work.

### Datasets

### Semantic Table Interpretation


## System requirements and design

What we were planning to do (initial goals), an overview of our system and explanation of the design choices.

Requirements:

* TODO

System Design:

* Python 3
* Scrapy
* Kafka Message Queue
* ArangoDB Database

## Implementation and Milestones

After familiarizing ourselves with the topic and having studied the relevant literature, we began designing and implementing our data processing pipeline.
This section will cover our implementation and the milestones we have completed in the course of our semester project.
<!-- Specific implementation details and design choices will be expanded in the following sections. -->

### Basic crawling and table extraction

The first significant milestone we reached (2020-11-02) was the basic crawling of web pages (i.e. downloading the HTML contents) and extracting the HTML tables.
The first version would simply take a list of URLs, download and parse these pages and finally store the results in a JSON file.

We opted for the Python programming language for our implementation because it very well suited for the task of crawling web pages, its flexibility and loose typing make it very convenient to deal with arbitrary and unformatted data and finally it has many excellent open source libraries available.
For the crawling itself, we decided to use the Scrapy framework \cite{scrapy} **TODO** *why?*

### Advanced table parsing

The next big step was implementing advanced table extraction and parsing algorithms.
In particular, we decided to use two different algorithms for parsing tables on Wikipedia pages and the rest of the web pages.
This decision was made because Wikipedia pages follow a much stricter format than the average table on the web.
**TODO** @eelisk *Expand on the wikipedia algorithm*

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

### Data format

By now, we were collecting many different pieces of information and had to come up with data format to store this data in.

refer to https://github.com/D2KLab/HarvestingTablesInTheWild/issues/5

### Common Crawl

In addition to crawling pages from the world wide web, we also wanted to explore using the CommonCrawl dataset \cite{}.
**TODO** @rohitshubham *Explain what the CC is and how we use it*

### Crawling strategy

### First crawl

### Visualization

Describe visualization and exploration in the arangodb dashboard.

### Topic annotation

(*TBD*) with Orange API.

## Results

What we managed to do and why/how it could be useful (and what we didn't achieve and why).

## Future work

How the work we have done so far can be continued or improved.

\clearpage

## References

[1] Hassan, Md Imrul, Hai L. Vu, and Taka Sakurai. *"Performance analysis of the IEEE 802.11 MAC protocol for DSRC safety applications."* IEEE Transactions on vehicular technology 60.8 (2011): 3882-3896.

[2] https://www.worldwidewebsize.com/
