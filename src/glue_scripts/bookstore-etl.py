import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# 데이터 소스 읽기 - 테이블 이름과 컬럼명을 실제와 일치하도록 수정
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="bookstore_db",
    table_name="bookstore_source_bucket"  # 실제 테이블명으로 수정됨
)

# 스키마 매핑 - 실제 컬럼명으로 수정
mapped_dyf = ApplyMapping.apply(frame=datasource, mappings=[
    ("title", "string", "title", "string"),
    ("price", "double", "price", "double"),
    ("age_group", "string", "age_group", "string"),
    ("genre", "string", "genre", "string"),
    ("book_id", "string", "book_id", "string"),
    ("transaction_id", "string", "transaction_id", "string")
])

# S3에 Parquet로 저장
glueContext.write_dynamic_frame.from_options(
    frame=mapped_dyf,
    connection_type="s3",
    connection_options={
        "path": "s3://bookstore-processed-bucket/",
        "partitionKeys": ["genre"]
    },
    format="parquet"
)

'''
# DynamoDB에 저장 부분 수정
glueContext.write_dynamic_frame.from_options(
    frame=mapped_dyf,
    connection_type="dynamodb",
    connection_options={
        "dynamodb.output.tableName": "bookstore_transactions",  # 변경된 부분
        "dynamodb.throughput.write.percent": "1.0",
        "dynamodb.output.hashkey": "transaction_id"  # 파티션 키 지정 / 만약에 문제가 생기면 이걸 지울 것
    }
)

'''
# Redshift 부분 활성화
#glueContext.write_dynamic_frame.from_jdbc_conf(
#    frame=mapped_dyf,
#    catalog_connection="Redshift connection",  # Glue의 연결 이름과 정확히 일치해야 함
#    connection_options={
#        "dbtable": "bookstore_transactions",
#        "database": "dev",
#        "tempdir": "s3://bookstore-processed-bucket/temp/"
#    }
#)

job.commit()

