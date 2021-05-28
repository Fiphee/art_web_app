from django.shortcuts import reverse


class CommentUtils:
    def __init__(self, recipient=None, next_url=None, content_owner=None):
        self.recipient = recipient
        self.next_url = next_url
        self.content_owner = content_owner
