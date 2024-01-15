#/bin/zsh
# Create the role
curl -X POST \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-H 'X-Trino-Role: system=ROLE{sysadmin}' \
-H "Authorization: Basic YWRtaW46YWRtaW4=" \
-d '{"name":"autorole2","description":"This is a role created by API"}' \
"https://sep.mwpov.sa.fieldeng.starburstdata.net/api/v1/biac/roles"
# id 5
# Create the column mask 
curl -X POST \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-H 'X-Trino-Role: system=ROLE{sysadmin}' \
-H "Authorization: Basic YWRtaW46U3RhcmJ1cnN0UjBja3Mh" \
-d "{\"name\":\"testcolumnmask\",\"description\":\"This is will replace vowels with stars\",\"expression\":\"regexp_replace(\\\"@column\\\",'[aeiou]','*')\"}" \
"https://sep.saipov.az.starburstdata.net/api/v1/biac/expressions/columnMask"
# id 8
# Create a column mask for the role
curl -X POST \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-H 'X-Trino-Role: system=ROLE{sysadmin}' \
-H "Authorization: Basic YWRtaW46U3RhcmJ1cnN0UjBja3Mh" \
-d '{"expressionId":8, "entity":{"category":"TABLES","allEntities":false,"catalog":"tpch","schema":"tiny","table":"customer","columns":["nationkey"]}}' \
"https://sep.saipov.az.starburstdata.net/api/v1/biac/roles/5/columnMasks"
# Attach the role to the user
curl -X POST \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-H 'X-Trino-Role: system=ROLE{sysadmin}' \
-H "Authorization: Basic YWRtaW46U3RhcmJ1cnN0UjBja3Mh" \
-d '{"roleId":5,"roleAdmin":"false"}' \
"https://sep.saipov.az.starburstdata.net/api/v1/biac/subjects/users/admin/assignments"

curl -X GET \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-H 'X-Trino-Role: system=ROLE{sysadmin}' \
-H "Authorization: Basic YWRtaW46YWRtaW4=" \
"https://sep.mwpov.sa.fieldeng.starburstdata.net/api/v1/biac/roles?pageToken=&pageSize=&pageSort="