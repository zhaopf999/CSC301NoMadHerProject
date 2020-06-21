from flask import jsonify, request
from . import nomadher_api as api
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

#cred = credentials.Certificate("nomadherd2-firebase-adminsdk-1l2wh-a12557d542.json")
db = firestore.client()

def upload_img_pair(user_id, pose_id, user_uploaded_img):
    users_ref = db.collection('users')
    docs = users_ref.document(user_id).get().to_dict()
    if not docs:
        return {'status': 'error', 'message': 'User Not Found'}
    which_pose = "pose-1"
    # We assume front-end will NOT send back any pose_id other than what is assigned to user
    # so after if-statements which_pose will never be "pose-1" 
    if(docs["pose1"]["pose_id"] == int(pose_id)):
        which_pose = "pose1"
    if(docs["pose2"]["pose_id"] == int(pose_id)):
        which_pose = "pose2"
    if(docs["pose3"]["pose_id"] == int(pose_id)):
        which_pose = "pose3"
    
    users_ref.document(user_id).update(
        {which_pose : 
            {"pose_id" : pose_id, 
            "user_uploaded_img" : user_uploaded_img
            }
        })

    return {'status': 'success'}

def check_pending(user_id):
    """
    If all three required photos are uploaded to this user's db, change verified status to 'Pending'.
    """
    users_ref = db.collection('users')
    docs = users_ref.document(user_id).get().to_dict()
    if docs["verified"] != "False":
        return
    else:
        users_ref.document(user_id).update({"verified" : "Pending"})
    
    # print(docs)
    for doc in docs :
        #print(docs[doc])
        if "pose" in doc and docs[doc]["user_uploaded_img"] == "None" :
            users_ref.document(user_id).update({"verified" : "False"})


@api.route('/post_poses', methods=['POST'])
def post_poses():
    data = request.json
    user_id = data['user_id']
    user_uploaded_img = data['user_uploaded_img']
    original_pose_id = data['original_pose_id']

    result = upload_img_pair(user_id, original_pose_id, user_uploaded_img)
    check_pending(user_id)
    '''
    dict_object = {
        'user_id' : user_id,
        'user_uploaded_img': user_uploaded_img,
        'original_pose_id': original_pose_id
    }
    '''

    return jsonify(result)