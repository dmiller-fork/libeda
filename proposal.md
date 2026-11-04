# Overview
I want to do a study on patent quality
by separating data into allowance rate by examiner by year, and then

separating applications into allowed and abandoned

the goal is to find situations where the allowance rate metrics are roughly the same as the abandonment metrics, and whether this corresponds with a particular examiner allowance rate for that particular year.

Datasets are available here:
https://www.uspto.gov/ip-policy/economic-research/research-datasets/patent-examination-research-dataset-public-pair

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
		- count_rows(df) — establish the starting population.
		- remove_null(df, key) — test by removing records with missing days_to_disposal.
		- print(count_rows) - run test to see how many removes
		- remove_negative(df, key) - test by removing records with negative days_to_disposal
		- print(count_rows) - run test to see how many removes
