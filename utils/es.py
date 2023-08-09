import json

from typing import List
from langchain.schema import Document

from google.cloud import discoveryengine_v1beta
from google.protobuf.json_format import MessageToDict

default_max_extractive_answer_count = 5
default_max_extractive_segment_count = 1
default_query_expansion_condition = 1


def es_raw_search_result(result):
    for i in result:
        print("-"*79)
        #print(i.getId())
        print(i)
        print("-"*79)

def es_raw_search_summary(project,
              search_engine,
              query,
              filtername = None,           
              location="global",
              serving_config_id='default_config',                          
              ):
    
    search_client = discoveryengine_v1beta.SearchServiceClient()
    serving_config: str = search_client.serving_config_path(
        project=project,
        location=location,
        data_store=search_engine,
        serving_config=serving_config_id
    )
    content_search_spec = {
        "extractive_content_spec": {
            "max_extractive_answer_count": default_max_extractive_answer_count,
        },
        "extractive_content_spec": {
            "max_extractive_segment_count": default_max_extractive_segment_count,
        }
    }
    content_search_spec = {
        "summary_spec": {
            "summary_result_count": 5
        },
        "extractive_content_spec": {
            "max_extractive_answer_count" : 1,
            "max_extractive_segment_count": default_max_extractive_segment_count,
        },
        "snippet_spec":
        {
            "max_snippet_count": 1
        }
    }    
    query_expansion_spec = {
            "condition": default_query_expansion_condition
    }
    print("Filter is :{}".format(filtername))
    request = discoveryengine_v1beta.SearchRequest(
            query=query,
            filter=filtername,
            serving_config=serving_config,
            page_size=5,
            content_search_spec=content_search_spec,
            query_expansion_spec=query_expansion_spec,
        )

    #request = discoveryengine_v1beta.SearchRequest(serving_config=serving_config, query=query)
    result = search_client.search(request)
    #es_raw_search_result(result)
    #print(result)
    return result.summary.summary_text, result

