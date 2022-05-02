import json
from functools import wraps
import os
from urllib import response
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Post, Reply
from flask_cors import CORS
from jose import jwt
from urllib.request import urlopen

POSTS_PER_PAGE = 15
AUTH0_DOMAIN = 'dev-royzhu.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'boardgameforum'

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"*" : {"origins": 'http://localhost:3000/'}})

    class AuthError(Exception):
        def __init__(self, error, status_code):
            self.error = error
            self.status_code = status_code

    def get_token_auth_header():
        """Obtains the Access Token from the Authorization Header
        """
        auth = request.headers.get('Authorization', None)
        if not auth:
            raise AuthError({
                'code': 'authorization_header_missing',
                'description': 'Authorization header is expected.'
            }, 401)

        parts = auth.split()
        if parts[0].lower() != 'bearer':
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization header must start with "Bearer".'
            }, 401)

        elif len(parts) == 1:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Token not found.'
            }, 401)

        elif len(parts) > 2:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization header must be bearer token.'
            }, 401)

        token = parts[1]
        return token

    def verify_decode_jwt(token):
        jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        if 'kid' not in unverified_header:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization malformed.'
            }, 401)

        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer='https://' + AUTH0_DOMAIN + '/'
                )

                return payload

            except jwt.ExpiredSignatureError:
                raise AuthError({
                    'code': 'token_expired',
                    'description': 'Token expired.'
                }, 401)

            except jwt.JWTClaimsError:
                raise AuthError({
                    'code': 'invalid_claims',
                    'description': 'Incorrect claims. Please, check the audience and issuer.'
                }, 401)
            except Exception:
                raise AuthError({
                    'code': 'invalid_header',
                    'description': 'Unable to parse authentication token.'
                }, 400)
        raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

    def check_permissions(permission, payload):
        if 'permissions' not in payload:
            abort(400)

        if permission not in payload[permission]:
            abort(403)
        
        return True
 
    def requires_auth(permission=''):
        def requires_auth_decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                token = get_token_auth_header()
                try:
                    payload = verify_decode_jwt(token)
                except:
                    abort(401)

                check_permissions(permission, payload)

                return f(payload, *args, **kwargs)

            return wrapper
        return requires_auth_decorator

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')  
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
        return response

    @app.route('/posts', methods=['GET'])
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
    @requires_auth('post:posts')
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
        'post_id': post.id,
        'subject': post.subject,
        'content': post.content,
        'replies':formatted_replies[start:end],
        'total_replies': len(replies)})

    @app.route('/posts/<int:post_id>', methods=["POST"])
    @requires_auth('post:replies')
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
