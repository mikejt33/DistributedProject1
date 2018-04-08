# Distributed Computing Project 1

## Team: [Lilly](https://github.com/lillyraud), [Joe](https://github.com/joecomerisnotavailable), [Adriana](https://github.com/acastrops), [Mike](https://github.com/mikejt33), [Stephanie](https://github.com/srive).

## Introduction and Data

[Complete Wikipedia edit history (up to January 2008)](http://snap.stanford.edu/data/wiki-meta.html)

**Dataset Information**

The data contains the complete edit history (all revisions, all pages) of all Wikipedia since its inception till January 2008. It  contains processed metadata for all revisions of all articles extracted from the full Wikipedia XML dump as of 2008-01-03.

For each specified namespace, there is a bzipped file with pre-processed data and also a file with all redirects. The output data is in the tagged multi-line format (14 lines per revision, space-delimited). Each revision record contains the following lines:

- `REVISION` article_id rev_id article_title timestamp [ip:]username user_id
- `CATEGORY` list of categories
- `IMAGE` list of images (each listed as many times as it occurs)
- `MAIN` through OTHER cross-references to pages in other namespaces
- `EXTERNAL` hyperlinks to pages outside Wikipedia
- `TEMPLATE` list of all templates (each listed as many times as it occurs)
- `COMMENT` contains the comments as entered by the author
- `MINOR` whether the edit was marked as minor by the author
- `TEXTDATA` word count of revision's plain text

For example:

```
REVISION 4781981 72390319 Steven_Strogatz 2006-08-28T14:11:16Z SmackBot 433328
CATEGORY American_mathematicians
IMAGE
MAIN Boston_University MIT Harvard_University Cornell_University
TALK
USER
USER_TALK
OTHER De:Steven_Strogatz Es:Steven_Strogatz
EXTERNAL http://www.edge.org/3rd_culture/bios/strogatz.html
TEMPLATE Cite_book Cite_book Cite_journal
COMMENT ISBN formatting &/or general fixes using [[WP:AWB|AWB]]
MINOR 1
TEXTDATA 229
[empty line]
```

## Goal: Find evidende of edit wars or overall interenet bickering in Wikipedia edits.

<p align="center">
  <img src="https://imgs.xkcd.com/comics/duty_calls.png" alt=":)" />
</p>

## Plan

### 1. Extract and Clean
  - MRJob: 
  
### 2. Create two datasets
  - **Superset:** Output of our first MR job (`abcds`*****) with a list of every article's date and number of edits for that date. 
  - **Outliers:** From the Superset, we calculated the mean number of edits per day for each article. Then, assuming that edits by day are a Poisson distribution, we selected only the article date pairs that had the top 5\% edits for that day, for that article. From the top 5\% we picked 67 articles.
  - **Random:** From the rest, excluding the previous 67 articles, we radomly picked another 67 articles. We also did not consier anything with less than 9 edits.

  
### 3. Compute summary statistics for Outliers
  - Bickering flag
  - Vandalism flag

### 4. Draw comparisons between two groups
  - Using the statistics computed above, we compare the two datasets.
  
### 5. Results
  - Our evidence for edit wars according to our assumptions
  - Visualizations
      * Basic vizes for summary statistics
      * Choropleth of user ip address

## Breakdown of steps taken


### 1. Munging

Initially took a look at top 10,000 lines from the unzipped data (bash). This command was adapted from one of the two you can find at the end of the page of the data documentation:

```
$ bzcat enwiki-20080103.main.bz2 | head -10000 > output.txt
```

After getting `output.txt` we were able to have a better idea of what the data looked like and started defining possible avenues for exploration. We got a list of all articles and number of times each was revised from that list (Pyhon script to do this: `revision_count.py`). 

This gave us the Top 1000 most revised articles. From here, we created a new MapReduce file that pulled pairs of dates with number of revisions (`acbdl_redo.py` creates Superset). Some records were not able to be processed for whatever reason so we skipped those :) the most complete list can be found in `articles_dates.csv`. 

### 2. Creating Outliers and Superset

Picked 67 unique articles with a specific date from outliers.txt to look at, to see if any appears to be edit-wars. We excluded the 67 unique articles from the `articles_dates.csv` and randomly picked 67 more articles with at least 10 edits on a single day, using mapreduce (`mrjob_RandomArticle.py`) and **SQL**. First query created a input file for `mrjob_RandomArticle.py`

``` SQL
SELECT * FROM articles_dates
WHERE NAME NOT IN (
'Albert_Einsteir',
'Alcoholics_Anonymous',
'Anarchism',
'Anarcho-capitalism',
'Ark_of_the_Covenant',
(...)
'Astrology',
'Dinosaur',
'Abortion'
) AND COUNT >9
GROUP BY NAME;
```
After Mapreduce produced the random list, we created a temporary table:

``` SQL
CREATE TABLE temp_list
SELECT DATE, NAME, COUNT FROM articles_dates
WHERE NAME IN 
(
"Kangaroo","Warmia","Astronaut","Group_sex","Laura_Bush","Lagrange_equations","Astronomical_unit","Abner_Doubleday",
"Federal_Bureau_of_Investigation","AutoCAD","Antarctic_Treaty_System","Amoeba","Alabama","Elliptic_integral","Apollo_11",
"Benelux","Functional_programming","Series_(mathematics)",  "Methylenedioxymethamphetamine","Detroit_Red_Wings","Big_bang","Connective","Psychedelic","Albinism","December_10","Racism",
"F-117_Nighthawk","Cauchy_sequence","Aston_Martin", 
"Rochester_Institute_of_Technology","Atari_2600","History_of_Germany","Cable_car_(railway)","Commodore_64",
"Andrew_S._Tanenbaum","Ampere","Chiba_Prefecture",
"Diocletian","London_Heathrow_Airport","AppleTalk","German_cuisine","Edgar_Rice_Burroughs","Cathode","List_of_Latin_phrases",
"Esperanto_grammar",
"Architectural_style","Demon","DC_Comics","December_25","Albert_Einstein","Background_radiation","Impressionism","Interlingua",
"Afghan","Bach_(disambiguation)","Opera_(browser)",
"Inca_Empire","Nudity","Joseph_Conrad","Berlin","Battle_of_Stalingrad","Bestiality","Eastern_Orthodox_Church",
"Argument_from_evolution","Diesel_engine",
"Anaximander","Brigitte_Bardot"
)  
AND COUNT >9
```

From this temp table, we selected the highest count edited day for the random group:

``` sql
SELECT * 
FROM (SELECT * FROM temp_list ORDER BY `Name`, COUNT DESC, DATE) X
GROUP BY `Name`;
```

### 3. Computing summary statistics for both groups

- Bickering flag
    * 


- Vandalism flag
    * Selected records with the word "vandalism" in the comments. One of the reasons for editing is vandalism, where an edit is tagged with "vandalism"" by another user due to trolling. Our assumption is that these rows are edits that reverted vandalism. 


### 4. Comparisons

### 5. Results

