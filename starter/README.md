# Full Stack Final Project
URL: https://boardgame-forum.herokuapp.com/

## Full Stack Boardgame Forum
I am a huge fan of boardgame, so I want to build a place for boardgame fans.
It is boardgame forum for all boardgame fans to share their hobbies.

## Role and permission:
### Visitor(Everyone):
1. Check all posts - /posts GET
2. Check all replies in each post - /posts/:id GET
3. Search posts' subject - /posts/result POST

### Register users:
1. Make post - /posts POST
2. Make a reply to a post  - /posts/:id POST
3. Update post  - /posts/:id PATCH

### Administrator
1. Delete post - /posts/:id DELETE
2. Delete replies -/replies/:replies_id DELETE
3. Make post - /posts POST
4. Make a reply to a post - /posts/:id POST

## Endpoints

### "GET" /posts:
- Retrives all posts and make the list with 15 posts each page.
- Returns: Json opject contains: 
    {
        'success':True,
        'posts':formatted_posts[start:end],
        'total_posts': len(posts)
    }
- sample : curl -X GET http://127.0.0.1:5000/posts'

### "POST" /posts:
- Creat a new post with post's subject and content.
- Request Arguments: json object contains at least all values (subject, content)
- Returns: Json opject contains: {'succes': True}
- sample : curl -X POST http://127.0.0.1:5000/posts -H "Authorization: Bearer <ACCESS_TOKEN>" -d '{"subject":"mahmoud", "content":"mahmoud"}'

### "GET" /post/:id:
- Retrives a specific post with its id, and server will return post's subject, content and its replies
- Returns: Json opject contains: 
    {
        'success':True,'post_id': post.id,
        'subject': post.subject,
        'content': post.content,
        'replies':formatted_replies[start:end],
        'total_replies': len(replies)
    }
- sample : curl -X GET http://127.0.0.1:5000/posts/1'

### "POST" /post/:id:
- Create a new reply to the specific post with post id.
- Request Arguments: json object contains one value (reply)
- Returns: Json opject contains {'succes': True}
- sample : curl -X POST http://127.0.0.1:5000/posts/1 -H "Authorization: Bearer <ACCESS_TOKEN>" -d '{"reply":"mahmoud"}'

### "PATCH" /post/:id:
- Update a specific post with a new subject and/or a new content.(Only Administrator allow to do that)
- Request Arguments: json object contains at least one of these values (subject, content)
- Returns: Json opject contains {'succes': True, 'updated': X}
- sample : curl -X PATHCH http://127.0.0.1:5000/posts/6 -H "Authorization: Bearer <ACCESS_TOKEN>" -d '{"subject":"mahmoud", "content":"content"}'

### "DELETE" /post/:id:
- Delete a specified post with its id.
- Returns: Json opject contains {'succes': True, 'deleted': X}
- sample : curl -X DELETE http://127.0.0.1:5000/posts/2 -H "Authorization: Bearer <ACCESS_TOKEN>'

### "DELETE" /replies/:replied_id:
- Delete a specified reply with its id
- Returns: Json opject contains {'succes': True, 'deleted': {}}
- sample : curl -X DELETE http://127.0.0.1:5000/replies/6 -H "Authorization: Bearer <ACCESS_TOKEN>"'

### /posts/result - POST:
- Search posts' subject and server will return all posts which are relevant to the search term.
- Request Arguments: json object contains one values (searchTerm)
- Returns: Json opject contains 
            {
                'success': True,
                'posts': formatted_posts,
                'totalPosts': len(formatted_posts)
            }
- sample : curl -X POST http://127.0.0.1:8080/posts/result -H "Authorization: Bearer <ACCESS_TOKEN>" -d '{"searchTerm":"mahmoud"}'


## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository](https://github.com/youzai62/boardgame_forum_sample) your forked repository to your machine.

Backend set up:
# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip3 install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.

### Database Setup
**Remember to update your database url config and auth0 config in setup.sh in starter folder.**

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
### On linux:
export FLASK_ENV=development
### On windows:
set FLASK_ENV=development
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