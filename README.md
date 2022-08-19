# fantasy-scraper
Trying to scrape all data from our fantasy league with NFL.com. Since we are moving to Sleeper. It might end up include myfantasyleague as well

## Simple Usage

First off you will need to ensure you have chromedriver installed in your path [StackOverflow](https://stackoverflow.com/a/40556092/1248536).
You should be able to set your path with `PATH="$PATH:/usr/local/bin/chromedriver"` or where ever your chromedriver is. If you
can `which chromedriver` then you are good.


To use the package, you should be able to pull your league id from NFL.com, email, you know your password, and whatever you want to use for a name of the
league (this does not need to be the actually name of the league)

```shell
_email="youremail@email.com"
_pass="TheP@SSWordYouUse"
_leagueid=123456
_name="Some random name"
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps nfl_scraper

# Should work
nfl_scraper -e $_email -p $_pass -i $_leagueid -n $_name

# Could be
python3 run nfl_scraper -e $_email -p $_pass -i $_leagueid -n $_name


```
## Developer Notes

If you are familiar with Python. You can work with the repo directly. Below are some of the steps I used to get the project running, building, etc...


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

### Running as locally Non Dev

```shell
poetry install --without dev --sync
poetry run python -V
# Help
poetry run python main.py -h 
# Sub out the params
poetry run python main.py -e <email> -p <password> -i <id> -n <name>
# Test need to beef these up
poetry run pytest
```

### Running as Dev

```shell
poetry check
poetry build
#poetry update #gets latest package version

```

### Running in CICD

```shell
poetry check
# output version
poetry version -s

poetry version major|minor|patch --dry-run
```
