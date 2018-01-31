import boto3

# Create an S3 client
s3 = boto3.client(‘s3’)
def get_chart_object(s3_client, Bucket, Key):
    """returns chart object from specified s3 bucket and key"""
    chart_object = s3_client.get_object(Bucket = Bucket,
                                        Key = Key)
    return chart_object

def read_chart_from_object (chart_object):
    chart_txt = chart_object['Body'].read()
    return chart_txt

def upload_to_s3(filename, bucket_name, filename):
    s3.upload_file(filename, bucket_name, filename)

if __name__ == "__main__":
    
