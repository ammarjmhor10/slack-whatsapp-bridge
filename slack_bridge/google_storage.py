# from datetime import datetime
# import os
# import environ 
# from google.cloud import secretmanager
# import google.auth
# from google.cloud import storage
# import requests

# try:
#     _, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()
# except google.auth.exceptions.DefaultCredentialsError:
#     pass


# def upload_blobs(meme_type:str,media_id:str,content):
#     """Lists all the blobs in the bucket."""
#     bucket_name = "slack_bridge"

#     storage_client = storage.Client()

#     # Note: Client.list_blobs requires at least package version 1.17.0.
#     # blobs = storage_client.list_blobs(bucket_name)
#     bucket = storage_client.bucket(bucket_name)
#     # blob = bucket.blob('prom.png')
#     # blob.download_to_filename('test.png')
#     file_name = media_id+"."+meme_type.split('/')[1]
#     blob = bucket.blob(file_name)
#     blob.upload_from_string(content)
#     url_file = "https://storage.googleapis.com/"+bucket_name+"/"+file_name
#     return url_file

# r = requests.get(url='https://files.slack.com/files-pri/T046LKXJ3KP-F05C1V9TL4C/test.jpg'
#                  ,headers={
#             'Authorization': 'Bearer xoxb-4224677615669-5395305320821-mXpJIJh2MvtxtqNtpjcXhxPR',
#             # 'Content-Type': 'application/json'
#             }).content
# d = datetime.now().timestamp()
# print(upload_blobs('image/jpg',str(d),r))
