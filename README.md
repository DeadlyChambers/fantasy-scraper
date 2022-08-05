# fantasy-scraper
Trying to scrape all data from our fantasy league with NFL.com. Since we are moving to Sleeper. It might end up include myfantasyleague as well


## Python Scraping

### Pipenv and Poetry

Setup

```bash
curl -sSL https://instcurl -sSL https://install.python-poetry.org | python3 -
pipenv install --python=/usr/loca/bin/python3.10
pipenv shell
poetry completions bash >> ~/.bash_completion
#export PIP_PYTHON_PATH="$VIRTUAL_ENV/bin/python3"
poetry new nfl_scraper
poetry new nfl_scraper
#pipenv install --index=pip
#pipenv install --index=distutils
poetry add requests
poetry add html5lib
poetry add bs4


#pip uninstall -y setuptools
#exit
#deactivate 
```

## Running

```bash
pipenv shell
cd nfl_scraper
poetry run python nfl_scraper/main.py

# Test
poetry run pytest
```




# print(table_text)
    # table = BeautifulSoup(table_text, features="html5lib")
    # print(table.prettify())
    # #table = tables.find_all("table")[0]
    # #TODO figure out how loop over the winner_tables
    # rows = table.find_all({"tbody", "tr"})
    # print(str(len(rows)))
    # for row in range(len(rows)):
    #     cells = rows.index(row).find("td")
    #     print(str(len(cells)))
    #     year = cells[0].get_text()
    #     team_a = cells[2]
    #     team_name = team_a.get_text()
    #     team_id = team_a.get_attribute("href").split('/')[-1]
    #     print(f"Year:{year} Name:{team_name} Id:{team_id}")
    # winner_rows = winner_tables[1].find_elements("xpath","/tbody//tr")
    # print("found")
    # print(str(len(winner_rows)))
    # for x in range(len(winner_rows)):
        
    #     year_el = driver.find_element("xpath",f"//table[@class='tableType-history hasGroups'][1]/tbody//tr[{x}]/td[1]")
    #     year = year_el.text
    #     team_a = driver.find_element("xpath",f"//table[@class='tableType-history hasGroups'][1]/tbody//tr[{x}]/td[3]/a[contains(@class, 'teamName')]")
    #     team_name = team_a.text
    #     team_id = team_a.getAttribute("href").split('/')[-1]
    #     print(f"Year:{year} Name:{team_name} Id:{team_id}")