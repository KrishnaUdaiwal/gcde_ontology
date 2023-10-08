#!bin/py

import requests

base_id = "app7RE8RMnzTYwNdK"
table_name = "tbleoIx4Vj2VFRpcm"
PAT= "patGjbV69ImemNkgA.471e040d51d12fc38d2905ca00f9f39a52f00ad27f7bfdca103ad3cbafe92d96"
r = requests.get("https://api.airtable.com/v0/meta/bases/{base_id}/tables/{table_name}/records", headers=('Authorization',PAT))
r.status_code
##  -H \ "Authorization: Bearer YOUR_TOKEN"