import json
import boto3
import pandas as pd
import io

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))  # 디버깅용 로그
    
    s3_client = boto3.client('s3')
    
    try:
        # 이벤트에서 버킷과 키 추출
        bucket = event['detail']['bucket']['name']
        key = event['detail']['object']['key']
        
        print(f"Processing file: {bucket}/{key}")  # 디버깅용 로그
        
        # 파일 확장자 체크
        if not key.endswith(('.csv', '.json', '.xlsx')):
            raise Exception(f"Unsupported file format: {key}")
        
        # 파일 읽기
        response = s3_client.get_object(Bucket=bucket, Key=key)
        
        # 필수 컬럼 정의
        required_columns = ['title', 'price', 'age_group', 'genre', 
                          'book_id', 'transaction_id']
        
        # 파일 형식별 처리
        if key.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(response['Body'].read()))
        elif key.endswith('.json'):
            df = pd.read_json(io.BytesIO(response['Body'].read()))
        elif key.endswith('.xlsx'):
            df = pd.read_excel(io.BytesIO(response['Body'].read()))
        
        # 컬럼 검증
        missing_columns = [col for col in required_columns 
                         if col not in df.columns]
        if missing_columns:
            raise Exception(f"Missing required columns: {missing_columns}")
        
        return {
            'statusCode': 200,
            'body': {
                'message': 'Validation successful',
                'bucket': bucket,
                'key': key
            }
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")  # 디버깅용 로그
        return {
            'statusCode': 500,
            'body': {
                'error': str(e),
                'bucket': bucket if 'bucket' in locals() else 'unknown',
                'key': key if 'key' in locals() else 'unknown'
            }
        }
