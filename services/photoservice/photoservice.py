from config import required_env
import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv
load_dotenv()
class PhotoService:
    photoService = None
    cloudinary.config(cloud_name = required_env('CLOUD_NAME'), api_key=required_env('API_KEY'), 
    api_secret=required_env('API_SECRET'))
    @staticmethod
    def getInstance():
        if not PhotoService.photoService:
            PhotoService.photoService = PhotoService()
        return PhotoService.photoService
    
    def addPhoto(self, photo,destFolder):
        upload_result = cloudinary.uploader.upload(photo,folder=destFolder)
        return upload_result['secure_url']