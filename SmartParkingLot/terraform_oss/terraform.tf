provider "alicloud" {
  alias  = "sh-prod"
  region = "cn-shanghai"
}

resource "alicloud_oss_bucket" "bucket-new" {
  provider = alicloud.sh-prod
  bucket = "bucket-20200322-2"
  acl    = "public-read"
}