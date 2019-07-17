# Smart-Career Scraper v2.1

## Changelog v2.1:
### Additions/Changes
+ Fixed case sensitive bug on input. The program will now automatically capitalize the first letter for each letter of
field and text input.
+ Program now makes all words lowercase post tokenization to avoid duplicates in the top 10 section (Capital and lowercase words would be considered seperate)
+ Moved the description extractor to its own function.
+ Typing in "All+" in the text section will output count/unique words for all documents not just those that have a certain word or phrase.
+ Fixed bug where if a certain field didn't exist the program would crash. Now skips over lines that don't have a specific field type.
+ Fixed bug where if a certain field was the last thing on the line, the text returned would have a bracket.
### Removals:
### To do:
+ Indeed script
+ TBD
+ Colored output?
+ Grouping of similar texts
+ Graph visualization

## Changelog v2.0:
### Additions/Changes
+ New jobs.json that has all 6,995 documents. The previous version did not have all documents exported.
+ Fixed a bug where if the job title had "Company" in it, the parser would incorrectly try to index there.
+ Fixed bug where the sum of the word counts would not match the total number of lines.
+ Added nicer formatting of output. (Rounded decimal to 2 places, nicely done columns)
+ Added some pre-processing to the description analyzer to remove stop words and punctuation.
+ Fixed a bug where the description via location could not be parsed.
### Removals:
+ jsonconverter.py as this went nowhere
### To do:
+ Additional pre-processing
+ Graphs and more statistics for the presentation
+ Fix case-sensitive bug

## Changelog v1.9:
### Additions:
+ jobs.json A file exported with all the documents we have on MongoDB at the present.
+ similarsearch.py Which finds all instances of similar words and outputs statistics about them.
  E.G.: Typing in jobs.json then Company then Amazon will yield 4 different variants of the company Amazon.
### Changes:
### Removals:

## Changelog v1.8:
### Additions:
+ Added get_indeedjobs.py *Not Finished* (Currently stuck on job iteration) 
### Changes:
+ Changed scheduler to 11 am
### Removals:

## Changelog v1.8:
### Additions:
### Changes:
+ Mr. Song fixed a bug with the period time not being correctly added to the scrape_url.
+ Mr. Song also took out the page restriction.
+ Changed formatting of output file.
+ Swapped run times of scheduler.py and pscheduler.py as get_jobs.py will take longer to run now.
### Removals:
+ Removed stuff about the period and the old output.json code as they are unecessary.

## Changelog v1.6:
### Additions:
+ Now outputs a .txt file with # of documents inserted.
### Changes:
+ Changed page limit from 5 to 6. (Slowly increasing to see how far we can go).
### Removals:

## Changelog v1.5:
### Additions:
### Changes:
+ Changed scheduler to update the database everyday at noon.
+ Capped page search to 3x5 jobs so 15 in total to not be kicked.
### Removals:

## Changelog v1.4:
### Additions:
+ Everyone is now connected to the company repository.
+ *NEW* file: scheduler.py that, when run, will run get_jobs.py once a day.
### Changes:
+ Config file can now take multiple job searches (one job per line).
+ Moved "main" to its own function to allow for this.
+ Capped page search to 5 for now so session is not kicked.
+ Seperated each script into its own folder.
### Removals:
+ My old repository (Still there, just not in use)

## Changelog v1.3:
### Additions:
+ Integration with the 2 new scripts.
+ Date Captured works for get_jobs, but not get_people not sure why.
+ Input is now automatic, to change, refer to the cfg.txt file.
  The first line is for the job title, the second line is period,
  the third and fourth lines are username and password respectively.
### Changes:
+ Config file changed to accomodate for login ID and password (Slots 2 and 3)
+ Period is now daily by default.
+ Script runs as long as it needs to, no hard limit unless I need to test.
### Removals:
+ The 2 old scripts, which have been replaced by these new ones.

## Changelog v1.2:
### Additions:
+ Added direct upload of any job description to MongoDB (and fixed weird issues with it)
+ Now ignores duplicates when adding data.
+ Added a config file where the first line = job description and second line = period
### Changes:
+ No longer takes user input. Use config file instead.
### Removals:
+ None

## Changelog v1.1:
### Additions:
+ Added direct upload of any job description to MongoDB
+ Filters results to past week only.
+ Added some comments to help understand code.
### Changes:
+ Changed hard limit to 100 job descriptions to A. Test and B. Avoid stalling.
+ Currently testing getting rid of duplicates.
### Removals (Just commented out):
+ Got rid of period selection as we are focusing on past week for now.

## Changelog v1.0:
+ Initial scraper
