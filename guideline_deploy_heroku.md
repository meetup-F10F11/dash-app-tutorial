### Step 1. Go to your directory where python app is located

`$ cd <location of your app>`



### Step 2. Initialize the folder with git and a virtualenv

- Initialize an empty git repository

`$ git init`

- Create a virtualenv called “venv”

`$ virtualenv venv`

- Activate virtualenv

`$ source venv/bin/activate`

virtualenv creates a fresh and blank Python instance just for your current project.


### Step 3. Reinstall your app’s dependencies with this virtualenv:

Install dependencies. This part may differ depending on your app.

```
$ pip install dash  
$ pip install dash-renderer  
$ pip install dash-core-components  
$ pip install dash-html-components  
$ pip install dash-table==3.1.11
$ pip install plotly  
$ pip install pandas  
$ pip install numpy
```

- Install gunicorn for deploying your app

`$ pip install gunicorn`


### Step 4. Initialize the directory with a .gitignore file, requirements.txt, and a Procfile for deployment

`$ vi .gitignore`

```
venv
*.pyc
.DS_Store
.env
```

`$ vi Procfile`

```
web: gunicorn app:server
```

equirements.txt describes your current Python dependencies.

`$ pip freeze > requirements.txt`



### Step 5. Initialize Heroku, add files to Git, and deploy

- Create Heroku app

`$ heroku create <app name> --buildpack heroku/python`

- Add all files to git

`$ git add .`
`$ git commit -m '<your commit message>'`

- Deploy code to Heroku

`$ git push heroku master`

Run the app with a heroku “dyno” number 1

`$ heroku ps:scale web=1`

Now you can check your app on http://<app name>.herokuapp.com !!



### Step 6. Update change on your app.

- View if there’s any change in your app. 

`$ git status`

- Add all changes and commit

```
$ git add .
$ git commit -m 'a description of the changes'
$ git push heroku master
```