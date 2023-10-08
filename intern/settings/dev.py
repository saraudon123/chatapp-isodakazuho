import os

from .base import *  

DEBUG = os.getenv("DEBUG", "y")

CORS_ALLOW_ALL_ORIGINS = DEBUG

