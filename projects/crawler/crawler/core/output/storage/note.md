这样 MinIO 配置：

storage:
  type: s3
  bucket: downloads
  endpoint_url: http://minio:9000
  access_key: minioadmin
  secret_key: minioadmin
  prefix: crawler

storage:
  type: s3
  bucket: crawler
  endpoint_url: http://minio:9000
  region: us-east-1
  access_key: minioadmin
  secret_key: minioadmin

实际上就是：

s3://downloads/crawler/xxxx.jpg

而 AWS S3 只需要：

storage:
  type: s3
  bucket: my-bucket
  region: eu-west-1

storage:
  type: s3
  bucket: crawler
  region: eu-west-1


outputs:
  - name: images
    type: binary_file

    storage:
      type: s3
      bucket: crawler
      endpoint_url: http://minio:9000
      region: us-east-1
      access_key: minioadmin
      secret_key: minioadmin
      prefix: downloads/images

    filename: "{{ ... }}"