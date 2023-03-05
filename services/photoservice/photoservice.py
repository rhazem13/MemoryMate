import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv
load_dotenv()
class PhotoService:
    photoService = None
    cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
    api_secret=os.getenv('API_SECRET'))
    @staticmethod
    def getInstance():
        if not PhotoService.photoService:
            PhotoService.photoService = PhotoService()
        return PhotoService.photoService
    
    def addPhoto(self, photo):
        upload_result = cloudinary.uploader.upload(photo)
        return upload_result['secure_url']