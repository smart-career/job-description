# Smart-Career Scraper v3.0

## Changelog v3.0:
### Additions/Changes
+ Finally gets the size of company! A new statistic for MongoDB
### Removals:
### To do:
+ Work on similarsearch processing for All+
+ Add ability to change fields and upload back to MongoDB.

## Changelog v2.9:
### Additions/Changes
+ No longer uses the convoluted list method I had before, instead gets documents directly from MongoDB and runs using dictionary.get() method.
+ Grouping now works for specific user text input.
+ Grouping slightly broken for All+. Needs a lot of work.
### Removals:
+ Old method (the new method is much cleaner)
+ jobs.json as we have automatic document input now.
### To do:
+ Make it so location, company names, etc. are standardized... maybe combine with similarsearch?
+ Gather more data and more fields.
+ Add ability to change fields and upload back to MongoDB.

## Changelog v2.8:
### Additions/Changes
+ Temporarily fixed bad inputs by skipping them. Not sure what the real problem is other than some docs having an apostrophe in their fields.
### Removals:
### To do:
+ Make it so location, company names, and job titles are standardized... maybe combine with similarsearch?
+ Trying to make similarsearch work with pymongo connection.
+ Gather more data and more fields

## Changelog v2.7:
### Additions/Changes
+ Mr. Song uploaded more job description files to MongoDB so I switched back over to smart career database for the mongodb-neo4j uploader. 
+ get_jobs.py was also modified by Mr. Song and some bugs were fixed.
+ Fixed a bug where getting the key for job functions would throw an error and stop input of data (for MongoDB_Neo4j)
### Removals:
+ get_jobs.py as test_jobs.py fixes a bunch of issues get_jobs.py had.
+ cfg.txt as the new .json one matches with test_jobs.py
+ cd, not sure what this file was but it was completely empty.
### To do:
+ Make it so location, company names, and job titles are standardized... maybe combine with similarsearch?
+ Trying to make similarsearch work with pymongo connection.
+ Optimizations if possible...

## Changelog v2.6:
### Additions/Changes
+ Changed the graph structure to be more location-focused.
+ Updated the neo4j ip.
### Removals:
### To do:
+ Make it so location, company names, and job titles are standardized... maybe combine with similarsearch?
+ Trying to make similarsearch work with pymongo connection.
+ Optimizations if possible...

## Changelog v2.5:
### Additions/Changes
+ Changed the node structures so we only need companies, locations, and job titles.
+ Fixed bug where some nodes would be blank instead of saying "not specified".
### Removals:
### To do:
+ Make it so location, company names, and job titles are standardized... maybe combine with similarsearch?
+ Trying to make similarsearch work with pymongo connection.

## Changelog v2.4:
### Additions/Changes
+ Mr. Song has pushed a tool to insert job description documents to neo4j.
+ Changed limiter to 50 to get some more data to explore.
+ Closed the neo4j driver to get rid of an error at the end.
### Removals:
### To do:
+ Change job description neo4j uploader to match our plan for data visualization

## Changelog v2.3:
### Additions/Changes
+ Added lemmatization. Resulting graphs have shifted slightly.
+ Removed any numbers from description text for extra pre-processing
### Removals:
### To do:
+ Group function bug fixes... works fine with one topic but not multiple. Not sure how to proceed.
+ Indeed Script

## Changelog v2.2:
### Additions/Changes
+ Moved the extractor to its own function just in case I want to add more features that aren't about that.
+ Added Grouping between the full extractor and the description extractor. The program will now group together certain topics and display how many variants there are.
+ Fixed bug where punctuation and spaces would mess up the grouping.
+ Fixed bug where the grouping would never grab the smallest possible string. (I.E. Software Engineer and Software Engineer Intern would be considered seperate).
+ Graph is now included at the end for top 10 description words!
### Removals:
+ Pymongo connector as it did not help speed up the program or work correctly in general. Maybe revisit it a different time.
### To do:
+ Group function takes an extremely long time for all 6,995 documents
+ Group function has unreliable output with All+
+ Grouping by location is a little weird not sure if fixable
+ Indeed Script

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
+ Colored output?
+ Grouping of similar texts
+ Graph visualization
+ Connect to MongoDB so it runs faster

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
