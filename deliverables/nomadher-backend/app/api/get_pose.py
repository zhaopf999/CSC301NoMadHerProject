from flask import jsonify, request
from . import nomadher_api as api
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db
import random

# cred = credentials.Certificate("nomadherd2-firebase-adminsdk-1l2wh-a12557d542.json")
db = firestore.client()

# /api/
@api.route('/test')
def test():
    '''
    This function is for test purpose. It will return an image url to the frontend
    '''
    # get image data from database 
    pose = db.document('pose/poseList').get().to_dict()
    posePhotoList = pose["posePhotoList"]

    # take out the image url from the return object
    image_obj = random.choice(posePhotoList)
    pose_img_uri = image_obj['pose_img_uri']
    pose_id = image_obj['pose_id']

    return jsonify({'image_uri': pose_img_uri})

# /api/
@api.route('/get_pose/<string:user_id>')
def get_pose(user_id):
    '''
    This function will return a json includes image url and an image id
    '''
    used_image_id = 0

    # validate the incoming user 
    user = db.document('users/' + user_id).get().to_dict()
    if not user:
        return jsonify({'status': 'error', 'message': 'User Not Found'})

    if user["pose1"]['user_uploaded_img'] == "None":
        used_image_id = int(user["pose1"]['pose_id'])
    elif user["pose2"]['user_uploaded_img'] == "None":
        used_image_id = int(user["pose2"]['pose_id'])
    elif user["pose3"]['user_uploaded_img'] == "None":
        used_image_id = int(user["pose3"]['pose_id'])

    if used_image_id == 0:
        return jsonify({'status': 'error', 'message': 'User Already Uploaded all Images'})
    
    # get image data from database 
    pose = db.document('pose/poseList').get().to_dict()
    posePhotoList = pose["posePhotoList"]

    # take out the image url from the return object
    image_obj = posePhotoList[used_image_id - 1]
    pose_img_uri = image_obj['pose_img_uri']
    
    return jsonify({'original_pose_id': used_image_id,'image_uri': pose_img_uri, 'status': 'success'})