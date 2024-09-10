from flask import request
from flask_restx import Resource, fields, Namespace, reqparse
from models import Member
from database import db

api = Namespace('members', description='Member operations', path='/members')

## user functions: login, logout, user profiles

## login request model
loginReq = api.model('Login', {
    'username': fields.String(required=True, description='Username is required'),
    'password': fields.String(required=True, description='Password is required'),
})

## User Profiles
userProfiles = api.model('UserProfile', {
    'id': fields.Integer(required=True, description='The user identifier'),
    'username': fields.String(required=True, description='The username'),
    'email': fields.String(required=True, description='The user email'),
})


# Login logics
@api.route('/login')
class Login(Resource):
    @api.expect(loginReq)  # 期待 JSON 格式的請求，根據 login_model 定義結構
    def post(self):
        # 從 JSON 請求中提取數據
        data = request.json
        username = data.get('username')
        password = data.get('password')

        # 此處應該加入驗證邏輯，比如查詢資料庫比對帳號密碼
        # 成功返回 token 或使用者信息，失敗返回錯誤訊息
        if username == 'admin' and password == 'admin':  # 範例邏輯
            return {'message': f'User {username} logged in successfully'}, 200
        else:
            return {'message': 'Invalid username or password'}, 401


# Logout logics
@api.route('/logout')
class Logout(Resource):
    def post(self):
        # 執行登出邏輯 (例如清除 session 或 token)
        return {'message': 'User logged out successfully'}, 200


# User Profile 資源
@api.route('/profile')
class UserProfile(Resource):
    @api.marshal_with(userProfiles)
    def get(self):
        # 取得使用者資料的邏輯，這裡應從資料庫中讀取使用者資料
        # 假設有一個已經登入的使用者，直接查詢他們的資料
        # 這裡使用硬編碼範例返回一個使用者的資料
        user_data = {
            'id': 1,
            'username': 'example_user',
            'email': 'example@example.com'
        }
        return user_data, 200