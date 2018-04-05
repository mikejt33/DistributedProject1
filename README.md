# Distributed Computing Project 1

## Team

[Lilly](https://github.com/lillyraud), [Joe](https://github.com/joecomerisnotavailable), [Adriana](https://github.com/acastrops), [Mike](https://github.com/mikejt33), Stephanie.

## Introduction and Data

[Complete Wikipedia edit history (up to January 2008)](http://snap.stanford.edu/data/wiki-meta.html)

**Dataset Information**

+ The data contains the complete edit history (all revisions, all pages) of all Wikipedia since its inception till January 2008.

+ The data set contains processed metadata for all revisions of all articles extracted from the full Wikipedia XML dump as of 2008-01-03.

+ For each specified namespace, there is a bzipped file with pre-processed data and also a file with all redirects. The output data is in the tagged multi-line format (14 lines per revision, space-delimited). Each revision record contains the following lines:

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

## Goal

![:)](https://imgs.xkcd.com/comics/duty_calls.png)

Find evidende of edit wars or overall interenet bickering in Wikipedia edits.

## Plan

### Steps Taken

* Initially took a look at top 10,000 lines from the unzipped data (bash);

$ bzcat enwiki-20080103.main.bz2 | head -10000 > output.txt

From the output. txt file was able to determine next step:

* Get list of all articles and number of times each was revised;

run revision_count.py, from that list, compiled:

* top 1000 most revised articles;

* new mapreduce, created date, article pair with number of revisions (acbdl_redo.py), creating as complete list as the data allowed - articles_dates.csv

### * Joe explains how he created outliers.txt

* Picked 67 unique articles with a specific date from outliers.txt to look at, to see if any appears to be edit-wars

* Excluding the 67 unique articles from the articles_dates.csv, picked randomly another 67 articles with at least 10 edits on a single day, using mapreduce (mrjob_RandomArticle.py) and SQL 

First query created a input file for mrjob_RandomArticle.py

``` SQL
SELECT * FROM articles_dates
WHERE NAME NOT IN (
'Albert_Einsteir',
'Alcoholics_Anonymous',
'Anarchism',
'Anarcho-capitalism',
'Ark_of_the_Covenant',
'Arsenal_F.C.',
'Autism',
'Batman_(1989_film)',
'Bipolar_disorder',
'Black_hole',
'Black_people',
'Blaise_Pascal',
'Blitzkrieg',
'Blue_Angels',
'Blue_whale',
'Britney_Spears',
'Caffeine',
'Capitalism',
'Cat',
'Chicago_White_Sox',
'Christmas',
'Christopher_Columbus',
'Claudius',
'Color_Temperature',
'Comet_Shoemaker-Levy_9',
'Condom',
'Cyberpunk',
'Deaths_in_2003',
'Diamond',
'Dianetics',
'Doctor_Who',
'Drum_and_bass',
'Eight_queens_puzzle',
'Fermi_paradox',
'Freemasonry',
'Fundamental_Dimensions',
'Game_theory',
'Glycerine',
'Henry_Ford',
'History_of_China',
'History_of_Russia',
'Human',
'Intelligent_design',
'Jim_Morrison',
'Kilogram',
'Loch_Ness_Monster',
'March_1',
'Mathematical_economics',
'Nikola_Tesla',
'October_2003',
"People's_Republic_of_China",
'Pit_Bull',
'Scriptures',
'The_Ashes',
'The_Cure',
'Wikipedia_bugs',
'World_Trade_Center/Plane_crash',
'Down_syndrome',
'Donald_Rumsfeld',
"Barnard's_Star",
'DNA',
'Augusto_Pinochet',
'Cane_Toad',
'Astrology',
'Dinosaur',
'Abortion'
) AND COUNT >9
GROUP BY NAME;
```
after Mapreduce produced the random list, created a temp table:

``` SQL
CREATE TABLE temp_list
SELECT DATE, NAME, COUNT FROM articles_dates
WHERE NAME IN 
(
"Kangaroo","Warmia","Astronaut","Group_sex","Laura_Bush","Lagrange_equations","Astronomical_unit","Abner_Doubleday","Federal_Bureau_of_Investigation","AutoCAD","Antarctic_Treaty_System","Amoeba","Alabama","Elliptic_integral","Apollo_11","Benelux","Functional_programming","Series_(mathematics)",
"Methylenedioxymethamphetamine","Detroit_Red_Wings","Big_bang","Connective","Psychedelic","Albinism","December_10","Racism","F-117_Nighthawk","Cauchy_sequence","Aston_Martin",
"Rochester_Institute_of_Technology","Atari_2600","History_of_Germany","Cable_car_(railway)","Commodore_64","Andrew_S._Tanenbaum","Ampere","Chiba_Prefecture",
"Diocletian","London_Heathrow_Airport","AppleTalk","German_cuisine","Edgar_Rice_Burroughs","Cathode","List_of_Latin_phrases","Esperanto_grammar",
"Architectural_style","Demon","DC_Comics","December_25","Albert_Einstein","Background_radiation","Impressionism","Interlingua","Afghan","Bach_(disambiguation)","Opera_(browser)",
"Inca_Empire","Nudity","Joseph_Conrad","Berlin","Battle_of_Stalingrad","Bestiality","Eastern_Orthodox_Church","Argument_from_evolution","Diesel_engine",
"Anaximander","Brigitte_Bardot")  AND COUNT >9
```

and from that temp table, selected the highest count edited day for the random group:

``` sql
SELECT * 
FROM (SELECT * FROM temp_list ORDER BY `Name`, COUNT DESC, DATE) X
GROUP BY `Name`;
```


