import json
from models.blog import Blog
from models.exception import ComplexEncoder
from models.user import User
from models.userblog import UserBlog


def format_db_blogs(blogs_db):
    """ format user-blog relationships to a json

    Args:
        blogs_db (list[UserBlog]): list of UserBlog relationships
    
    Returns:
        list: list of UserBlog json

    """
    blogs = []

    for blog in blogs_db:

        blog.blog_id = str(blog.blog_id)
        blog.user_id = str(blog.user_id)
        blog.id = str(blog.id)
        user_model = User(**blog.user.as_dict()).__dict__
        blog_model = Blog(**blog.blog.as_dict(), user=blog.blog.user.as_dict()).__dict__
        blog_model["content"] = "" # dont need the content in the list of blogs
        user_blog_model = UserBlog(blog_id=blog.blog_id, user_id=blog.user_id, id=blog.id, user=user_model, blog=blog_model)
        user_blog_json = json.dumps(user_blog_model.reprJSON(), cls=ComplexEncoder)
        blogs.append(json.loads(user_blog_json))
    return blogs