import boto3
from s3key import SECRET_ACCESS_KEY, ACCESS_KEY

def upload_file_to_s3(file_path, bucket_name, object_name, aws_access_key_id, aws_secret_access_key):
    # Create an S3 client with your credentials
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
   
    # Upload the file
    try:
        response = s3.upload_file(file_path, bucket_name, object_name)
        print("Upload successful")
    except Exception as e:
        print(f"Upload failed: {e}")
    # Update permissions
    try:
        s3.put_object_acl(Bucket=bucket_name, Key=object_name, ACL='public-read')
        print("Object ACL set to 'public-read'")
    except Exception as e:
        print(f"Failed to set object ACL: {e}")

# Example usage
file_path = 'static/images/stock-fish.jpg'  # Replace with the path to your file
bucket_name = 'fish-wallet'      # Replace with your S3 bucket name
object_name = 'stock-fish3.jpg'              # Replace with the desired object (file) name in S3
aws_access_key_id = ACCESS_KEY  # Replace with your AWS access key ID
aws_secret_access_key = SECRET_ACCESS_KEY

upload_file_to_s3(file_path, bucket_name, object_name, aws_access_key_id, aws_secret_access_key)