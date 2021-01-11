## Instructions to run the app

github location to dowload the files if not able load or use, is: https://github.com/prajwalkk/SearchEngineFS

use master branch to run it locally

command:
	`git clone https://github.com/prajwalkk/SearchEngineFS.git`

### app deployed online: https://uic-search-pkk.herokuapp.com/


required python verson 3.7 and above.
recommended - python3.8

This is tested in linux systems. I do not recommend windows as I do not own a windows machine.
the python command may differ in your system. It could be python3 or python3.8 or python. My system has python3.8 as the command.


1) Upgrade pip
	Windows powershell:
	
```
py -m pip --version
py -m pip install --upgrade pip
```
	Linux and macOS:
	
```
python3 -m pip install --user --upgrade pip
python3 -m pip --version
```
		
2) install virtualenv Create a virtual environment and activate it
	Windows:
	
```
py -m pip install --user virtualenv
py -m venv env
.\env\Scripts\activate
```
	
	Linux:
	
```
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
python -m pip install --user --upgrade pip  (this upgraded the pip of the virtualenv)
```

3) Install the required dependencies

```pip install wheel
pip install -r requirements.txt
```
		
 ** if any wheel error comes, do:
		
```pip install wheel```
		
4) place the files in the search_engine folder (the one which contains manage.py) Run
	
```python manage.py runserver```
	

Wait for sometime until the message says the server is created and press Ctrl+C to exit.
now go to the address specified in the terminal. normally localhost:8000

### Files needed:

Crawling - Independent module. Present in the Crawler folder. 
To run use, Do not run it in the Crawler folder. Run it in the manage.py folder 
	python Crawler/main.py
It save the data in DataFiles/Crawled and DataFiles/Links with the current date as the folder.

- `PageRanker.py` - this does the pagerank computation. To use the latest file, just open the python file and change the date eg 20200510 to the date on which the crawler was run (everywhere)
- `Vectorizer_pipeline.py` - does all preprocessing. To use the latest file, just open the python file and change the date eg 20200510 to the date on which the crawler was run (everywhere)
- `analyse_query.py` controller component to calculate. To use the latest file, just open the python file and change the date eg 20200510 to the date on which the crawler was run (everywhere)



Basic app execution flow:
1. Crawl using 
```python Crawler/main.py```

2. Change the dates in the `PageRanker.py, analyse_query.py, vectorizer_pipeline.py` to the latest crawled date  wherever a date exists. Eg 20200510 becomes 20200511 (if run)

3. Run the indexer files:

```
python vectorizer_pipeline.py
python analyse_query.py
```

4. Run the app server.
```python manage.py runserver```
5. In brower, open http://127.0.0.1:8000/ (or any other port as specified in the console) 
6. Profit

This app will not run if the DataFiles are empty. 	
Following files need to be in DataFiles Dir:
|`CrawledData\  ` | this has all the crawled pages |
|`Links\ `  | this has all the graph data |
|`dataFrame_bk.pkl  ` | this is the dataframe to persist the values |
|`page_rank.pkl  ` |  pagerank file |
|`tfidf.joblib `  |  TFIDF matrix |
|`vectorizer.joblib` | Inverted Index |
