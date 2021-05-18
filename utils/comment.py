from django.shortcuts import reverse


class CommentUtils:
    def __init__(self, recipient=None, next_url=None, content_owner=None):
        self.recipient = recipient
        self.next_url = next_url
        self.content_owner = content_owner


    @staticmethod
    def get_comment_url(content):
        from users.models import AuthUserModel
        from artworks.models import Artwork
        from comments.models import Comment

        urls = {
            Artwork:reverse('artworks:view', args=(getattr(content, 'id', 0),)),
            AuthUserModel:reverse('users:profile', args=(content,))
        }
   
        if isinstance(content, Comment):
            return CommentUtils.get_comment_url(getattr(content.content_object, 'user', 'author'))

        for class_type in [Artwork, AuthUserModel]:
            if isinstance(content, class_type):
                return urls[class_type]


    @staticmethod
    def get_reply_url(content):
        from comments.models import Comment

        if not isinstance(content, Comment):
            return CommentUtils.get_comment_url(content)
            
        return CommentUtils.get_reply_url(content.content_object)