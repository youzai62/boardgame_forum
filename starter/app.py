import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Post, Reply
from flask_cors import CORS

POSTS_PER_PAGE = 15

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"*" : {"origins": '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')  
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
        return response

    @app.route('/posts', methods=['GET'])
    #@cross_origin
    def retrieve_posts():
        page=request.args.get('page',1,type=int)
        start=(page-1)*POSTS_PER_PAGE
        end=start+POSTS_PER_PAGE

        posts = Post.query.order_by(Post.id).all()
        formatted_posts=[post.format() for post in posts]

        if (len(formatted_posts[start:end])==0):
            abort(404)

        return jsonify({'success':True,
        'posts':formatted_posts[start:end] ,
        'total_posts': len(posts)})
    
    @app.route('/posts', methods=["POST"])
    #@cross_origin
    def create_post():
        try:
            body = request.get_json()
            subject = body.get('subject', None)
            content = body.get('content', None)
            post = Post(subject, content)
            post.insert()

            return jsonify({
                'success': True
            })
        except:
            abort(400)

    @app.route('/posts/<int:post_id>', methods=["DELETE"])
    #@cross_origin
    def delete_specific_post(post_id):
        post = Post.query.filter(Post.id == post_id).one_or_none()
        if post is None:
            abort(404)
        post.delete()

        return jsonify({
            'success': True,
            'deleted': post_id
        })
        
    @app.route('/posts/<int:post_id>', methods=["PATCH"])
    #@cross_origin
    def update_specific_post(post_id):
        try:
            body = request.get_json()
            subject = body.get('subject', None)
            content = body.get('content', None)
            post = Post.query.filter(Post.id == post_id).one_or_none()
            if post is None:
                abort(404)
            post.subject = subject
            post.content = content
            post.update()

            return jsonify({
                'success': True,
                'updated': post_id
            })
        except:
            abort(400)

    @app.route('/posts/<int:post_id>', methods=['GET'])
    def retrieve_specific_post(post_id):
        page=request.args.get('page',1,type=int)
        start=(page-1)*POSTS_PER_PAGE
        end=start+POSTS_PER_PAGE

        post = Post.query.filter(Post.id == post_id).one_or_none()
        replies = Reply.query.filter(Reply.post_id == post_id).order_by(Reply.id).all()
        formatted_replies=[reply.format() for reply in replies]

        if post is None:
            abort(404)

        return jsonify({'success':True,
        'subject': post.subject,
        'content': post.content,
        'replies':formatted_replies[start:end],
        'total_replies': len(replies)})

    @app.route('/posts/<int:post_id>', methods=["POST"])
    #@cross_origin
    def create_reply(post_id):
        try:
            body = request.get_json()
            content = body.get('content', None)
            reply = Reply(post_id, content)
            reply.insert()

            return jsonify({
                'success': True
            })
        except:
            abort(400)
    
    @app.route('/replies/<int:reply_id>', methods=["DELETE"])
    #@cross_origin
    def delete_specific_reply(reply_id):
        reply = Reply.query.filter(Reply.id == reply_id).one_or_none()
        if reply is None:
            abort(404)
        reply.delete()

        return jsonify({
            'success': True,
            'deleted': reply_id
        })

    @app.route('/posts/result', methods=["POST"])
    #@cross_origin
    def search_post():
        try:
            body = request.get_json()
            search_term = body.get('searchTerm', None)
            result=Post.query.filter(Post.subject.ilike('%{}%'.format(search_term))).order_by(Post.id).all()
            formatted_posts = [post.format() for post in result]
            if len(formatted_posts) == 0:
                abort(404)
            return jsonify({
                'success': True,
                'posts': formatted_posts,
                'totalPosts': len(formatted_posts)
            })
        except:
            abort(400)
    
    return app


app = create_app()

if __name__ == '__main__':
    app.run()
