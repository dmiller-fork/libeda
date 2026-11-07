# Overview
I want to do a study on patent quality
by separating data into allowance rate by examiner by year, and then

separating applications into allowed and abandoned

the goal is to find situations where the allowance rate metrics are roughly the same as the abandonment metrics, and whether this corresponds with a particular examiner allowance rate for that particular year.

Datasets are available here:
https://www.uspto.gov/ip-policy/economic-research/research-datasets/patent-examination-research-dataset-public-pair

# organization
	- build/ scripts of transforms that create tables, 
	- libeda.py class Transforms generally transforms dataframs into views

# quality indicators:

Need at least six quality indicators
	- days to disposal
    - number of actions
    - number of citations
    - number of NPL citations
    - length of shortest independent claim
    - whether appealed

# Requirements
	- create libeda.py (DONE)
	- create tests/ (DONE)
	- create eda.py has following api: <dataset> <column> <stat>.
	- create repo (DONE)
	- write some code to list the available datasets (DONE)
	- write transforms to stage 3 main datasets: 
		- stg_claimstats.py (DONE),NOTE BAD DATA because PGPUB
		- stg_citations.py (DONE)
		- stg_appdata.py (DONE)
	- write transforms to create derived columns, with APP_ID as primary key:
		- int_primaryindependent_claimstats.py  (DONE)
		- int_count_citations.py  (DONE)
		- int_daystodisposal_appdata.py (DONE)
	- write the following functions:
		- count_rows(df) — establish the starting population. (Done)
		- remove_null(df, key) —  (Done)
		- remove_negative(df, key) - (Done)
	- write a join function:
		- join(pd1, key1, pd2, key2) - (Done)
	- write a script that creates a table with allowance rate of the examiner that allowed application
		- int_examinerid_appdata.py [examiner_id, issue_ct, abandon_ct, total_ct] (DONE)
			- what to do when issue_ct + abandon_ct does not equal total_ct?
			- could be pending? let's explore
		- int_allowancerate_appdata.py [application_number, allowance_rate]
