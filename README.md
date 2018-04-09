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
  
### 2. Create two datasets
  - **Superset:** Output of our first MR job (`abcdl_redo.py`) with a list of every article's date and number of edits for that date. 
  - **Outliers:** From the Superset, we calculated the mean number of edits per day for each article. Then, assuming that edits by day are a Poisson distribution, we selected only the article date pairs that had the top 5\% edits for that day, for that article. From the top 5\% we picked 67 articles.
  - **Random:** From the rest, excluding the previous 67 articles, we radomly picked another 67 articles. We also did not consider anything with less than 9 edits.

  
### 3. Compute summary statistics for Outliers
  - Bickering flag
  - Vandalism flag

### 4. Condoms and Stars

- Barnard’s Star was the wikipedia “article of the day” when it saw its spike in edits.  We attribute the spike in edits to be due to the people “trolling” this article due to its unexpected exposure as being selected as the article of the day on October 18, 2007.

-  The condom article saw its spike in edits on December 26, 2005.  This occurred one day after the Catholic Church released a statement stating that “Safe sex” in regards to sexual activity using condoms is not actually safe.

https://catholicnews.sg/index.php?option=com_content&view=article&id=709:e2809csafe-sexe2809d-is-not-really-safe&catid=140:december-2005&Itemid=473&lang=en

We believe this statement ignited the extensive editing that this article experienced. 


  
### 5. Comparison and Results
  - Using the statistics computed above, we compare the two datasets
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
"Benelux",
(...)
"Functional_programming","Series_(mathematics)",  "Methylenedioxymethamphetamine","Detroit_Red_Wings","Big_bang","Connective","Psychedelic","Albinism","December_10","Racism",
"F-117_Nighthawk","Cauchy_sequence","Aston_Martin"
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
    * For each record  -- number of edits for a given day per article -- in the Superset, we collected the number of comments as well as the number of unique users making those comments. The idea was to narrow down articles that had a lot of edits made by not a lot of people; i.e., the ratio of unique users to comments would be quite small. Our assumption was that we would use this value to help us narrow down articles in which an edit war could be going on. 


- Vandalism flag
    * Selected records with the word "vandalism" in the comments. One of the reasons for editing is vandalism, where an edit is tagged with "vandalism"" by another user due to trolling. Our assumption is that these rows are edits that reverted vandalism. 

### 4. Condoms and Stars



### 5. Comparisons and results 



