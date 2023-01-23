# Dependencies
Please install *Python 3.10.6* before you install the dependencies. If you already have an earlier version of Python installed, please upgrade your version.
You need to install the following packages on your machine or a virtual environment to run the website using the following pip commands:
- ```pip install django=4.1.4``` (for web development)
- ```pip install pysentimiento``` (for sentiment analysis using the BERT model)
- ```pip install vaderSentiment``` (for sentiment analysis the VADER lexicon)
- ```pip install nltk``` (for corpus, also includes VADER)


## A note on virtual environments
As much as possible, use ```venv``` as the name of your virtual environment. If you want to use another name, please add the name of your folder to the repository's ```.gitignore``` file.

# Documentations / Tutorials
For Django tutorials, I recommend Corey Schafer's YouTube tutorials that covers a lot of the features of Django, as well as Bootstrap 4 for designing the website. Supplemental readings can be found on Django's official website.
- [Corey Schafer's Django tutorial](https://www.youtube.com/watch?v=UmljXZIypDc&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p)
- [Django Documentation](https://www.djangoproject.com/)

For documentation on how to use VADER, please read their GitHub's documentation.
- [VADER GitHub Documentation](https://github.com/cjhutto/vaderSentiment)

For BERT, please read the following documentation.
- [PySentimiento GitHub Documentation](https://github.com/pysentimiento/pysentimiento)

# ==Implementing corpus into VADER==
The corpus folder should contain corpus.txt, just copy the contents of the file into vader_lexicon.txt, which should be located in `lib/python3.10/site-packages/vaderSentiment/` within your virtual environment or python installation folder.
Dataset sources:
- [Corpora](https://github.com/dariusk/corpora)
- [Adjectives list by Jordan Siem](https://www.kaggle.com/datasets/jordansiem/adjectives-list)

# Misc notes
- To log-in into the *administrator* page, use the following credentials:
  ```
  username: myadmin
  password: testing321
  ```
- The database to be used during development is SQLite3, but production DB is PostgreSQL

# BRANCHES
developM is the development branch for **Mu-Cepheus** 

# Other links
- [Web page sketches](https://www.figma.com/file/hXYV9D1kKhyBl5I5N21MsM/Website-Design?node-id=0%3A1&t=HLugZxy81sUyIc1p-1)
- [Entity-Relationship Diagram](https://lucid.app/lucidchart/1088a82a-d14a-456e-bd92-161808a6680d/edit?beaconFlowId=B0507B90833A6D8B&invitationId=inv_8bb9f62b-e8c8-4e9a-af9f-14032db8361a&page=0_0#)