from flask import Blueprint

nomadher_api = Blueprint('nomadher_api', __name__)

from . import route_post_login, post_poses, get_pose, photoID
