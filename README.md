# Full Stack Final Project


## Full Stack Boardgame Forum
I am a huge fan of boardgame, so I want to build a place for boardgame fans.
It is boardgame forum for all boardgame fans to share their hobbies.

## Role and permission:
### Visitor:
1. Check all posts 
2. Check all replies in each post
3. Search posts' subject

### Register users:
1. Make post
2. Make a reply to a post
3. Update post

### Administrator
1. Delete post
2. Delete replies
3. Make post
4. Make a reply to a post

## Endpoints

### /posts - GET:
Retrives all posts and make the list with 15 posts each page.

### /posts - POST:
Creat a new post with post's subject and content.

### /post/:id - GET:
Retrives a specific post with its id, and server will return post's subject, content and its replies

### /post/:id - POST:
Create a new reply to the specific post with post id.

### /post/:id - PATCH:
Update a specific post with a new subject and/or a new content.(Only Administrator allow to do that)

### /post/:id - DELETE:
Delete a specified post with its id.

### /replies/:replied_id - DELETE:
Delete a specified reply with its id

### /posts/result - POST:
Search posts' subject and server will return all posts which are relevant to the search term.


## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository](https://github.com/youzai62/boardgame_forum_sample) your forked repository to your machine.

Backend set up:
# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.

### Database Setup
Remember to update your database url config in setup.sh in starter folder.

With Postgres running, create a database named "boardgame" restore a database using the Test_db.psql file provided. From the starter Folder in terminal run:
```bash
psql boardgame < Test_db.psql
```

### Running the server

From within the `./starter` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
source setup.sh
flask run
```
If you want to test
```bash
source setup.sh
export FLASK_ENV=development
flask run
```

Frontend set up:
### Getting Setup

> _tip_: Set your backend first before working on Frontend

### Installing Dependencies

1. **Installing Node and NPM**<br>
This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**<br>
This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:
```bash
npm install
```
>_tip_: **npm i** is shorthand for **npm install**

# Required Tasks
Since we are using auth0 to handle all authorization jobs, please set up your auth0 config in .env file in the Frontend folder.


### Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```