![Alt Text](assets/Overview.gif)
<p align="center">
<img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/Barashkis/ChampionatParser">
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Barashkis/ChampionatParser">
<img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/y/Barashkis/ChampionatParser">
</p>

# Project description
This repository contains files of my small project - parser of championat.com,
which publishes sports news.

After starting the parser you will be prompted to choose the type of sport and the number 
of pages with news, that you want to extract from the site.

As a result a directory *data* will be created, which will contain the HTML pages
with all the news (to avoid constant requests to the site); one *json* file,
file will contain information about each news (namely, its title, a link to it, 
the number of comments, tag, and publication date).

This project uses Python libraries (version 3.8) such as:
+ BeautifulSoup4
+ lxml
+ requests
+ json
+ os / shutil / pathlib
+ selenium

Altogether there are 2 branches available, with different versions of the parser: 
based on the library requests and selenium.
The requests based version parses several pages, the selenium version parses a certain page.

# How to use
Clone or fork the repository, then open it in PyCharm (or terminal) and enter the command to run the script:
```
python championat_parser.py //run the requests based version
python championat_parser_selenium.py //run the selenium based version (read additional information in the next section)
```

If it doesn't work, try these corresponding commands:
```
python3 championat_parser.py
python3 championat_parser_selenium.py
```

That's all, at the end of the script work you will get json file contains all information of the recent 
sport news!

# Important
The script has a break after each iteration (iterates through the news pages):
```
sleep(random.randint(2, 4)) //pauses the script from 2 to 4 seconds (in random order) 
```
Remove the call to this function if you don't need to pause between iterations. 

If you want to use the selenium version, you need to have Google Chrome version 96.0.4664.45,
or you will need to change the driver file (chromedriver.exe) to your
([here](https://chromedriver.storage.googleapis.com/index.html) you can download any version of Chrome). 
You do not need to change the name of the driver file.  

Also **don't create** any custom folders or files in data folder: the next time you run the script, 
all content of the data directory will be **rewrited**, i.e. the folder will be 
cleared for the next placement of fresh html files.
