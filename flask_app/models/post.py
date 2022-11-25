from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Post:
    db_name = "exam_schema"
    def __init__(self, data):
        self.content = data['content']
        self.user_id = data['user_id']
        self.post_id = data['post_id']

    @classmethod
    def create_post(cls, data):
        query = "INSERT INTO posts (content, user_id) VALUES (%(content)s, %(user_id)s);"
        return  connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all_posts(cls, data):
        query = "SELECT posts.id, content, COUNT(likes.id) as like_num, users.id as creator_id, email FROM posts LEFT JOIN users on posts.user_id = users.id LEFT JOIN likes on likes.post_id = posts.id GROUP BY posts.id;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def add_like(cls, data):
        query = "INSERT INTO likes (post_id, user_id) VALUES (%(post_id)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def remove_like(cls, data):
        query = "DELETE FROM likes WHERE post_id = %(post_id)s and user_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def remove_post(cls, data):
        query = "DELETE FROM posts WHERE id = %(post_id)s and user_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update_post(cls, data):
        query = "UPDATE posts SET content = %(content)s WHERE posts.id = %(post_id)s and posts.user_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validate_post(data):
        is_valid = True
        if len(data['content']) < 5:
                flash("*Post must have at least 5 characters.", "contentPost")
                is_valid = False
        return is_valid