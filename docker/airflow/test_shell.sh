#!/bin/bash

CURRENT_DATE=$(date '+%Y-%m-%d')
NODES={"localhost:9200" "localhost:9201")
NODE=${NODES[0]}
INDEX="nginx-access-log-$CURRENT_DATE"
REQUEST_JSON_FILE="api-latency-over2sec-dsl.json"

sendMessageToSlack() {
  curl -XPOST -H "Content-Type: application/json; charset=utf-8" 
       -H "Authorization: Bearer xoxb-xxxxxxxxxxxxxxxxxxxxxxxxxx" 
       -d  "{ 'text': '$1'  }"  https:// #
}

echo "curl --request POST --url http://$NODE/$INDEX/_search --header 'Content-Type: application/json' --data @$REQUEST_JSON_FILE"
RESPONSE_JSON=`curl --request POST --url http://$NODE/$INDEX/_search --header 'Content-Type: application/json' --data @$REQUEST_JSON_FILE`

echo "+++++++++++++++++++++++++++++++++++++++++++++"
echo $RESPONSE_JSON | jq .aggregations.long_latency.buckets[0].doc_count
echo "+++++++++++++++++++++++++++++++++++++++++++++"

INDEX_NAME=$2
ACTION=$3
ALIAS_NAME=$4
TARGET_DATE=$5

RESULT=`curl -s -o /dev/null -w "%{http_code}\n" -XPOST 'http://'$NODE'/_aliases' -H 'Content-Type: application/json' -d '
{
  "actions" : [
      { "'$ACTION'" : { "index" : "'$INDEX_NAME'-'$TARGET_DATE'", "alias" : "'$INDEX_NAME'-'$ALIAS_NAME'" }}
  ]
}'`