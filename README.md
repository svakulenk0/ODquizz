# Open Data Quizz Builder

Web-site for constructing Open Data (OD) Quizzes.

OD Quizz is a quiz featuring tables with official goverment statistics pulled out from the Open Data portals designed to motivate citizens participation, awareness and transparancy.


Goals: 

(1) provide easy access to and further encorage discovery, exploration and utilization of the goverment statistical data;

(2) crowdsourcing OD annotations for question answering (QA) from tables.


Method: gamification: game-with-a-purpose providing support for semi-automated quiz construction.

## Requirements

pip install:

* Flask

* Flask-OAuth

* Flask-SQLAlchemy

* pyyacp:

git clone https://github.com/ODInfoBiz/pyyacp.git
git checkout tags/v1.0

to add to $PYTHONPATH: export PYTHONPATH=$PYTHONPATH:/home/svakulenko/pyyacp/
to check: echo $PYTHONPATH  

* python-dateutil

* structlog

* pip install git+git://github.com/sebneu/anycsv.git

* unicodecsv

bower install: (run inside static folder! sudo chown -R <user>:<user> /home/<user>/.config/configstore)

* webcomponentsjs

* handsontable/handsontable#^0.25

* Polymer/polymer#^1.2.4

* requirejs

* jquery


## Features

* Facebook authentication

## Deployment

Set up Facebook app at developers.facebook.com

App Domains: localhost
Add Platform -> Website -> Site URL: http://localhost:5000/

Run:

python quizz.py

## Acknowledgments

* Jürgen Umbrich, Sebastian Neumaier, Vadim Savenkov. Open Data Hackathon WU. 2017.

* Declarative widgets Polymer elements https://github.com/jupyter-widgets/declarativewidgets/tree/master/elements

* Armin Ronacher. PyLadies Flask Workshop tutorial. https://github.com/mitsuhiko/pyladies-flask

## Inspiration and Related Work

* CSV Engine http://data.wu.ac.at/csvengine/clean

* Alan Smith. https://www.ted.com/talks/alan_smith_why_we_re_so_bad_at_statistics

* http://www.neighbourhood.statistics.gov.uk

* Gapminder. Global Ignorance Project. http://www.gapminder.org/ignorance/

* https://www.typeform.com/examples/quizzes/

* https://www.buzzfeed.com/quizzes
