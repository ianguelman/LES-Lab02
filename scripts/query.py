from math import ceil
import os, datetime
from dateutil.parser import parse
from types import NoneType
from utils.graphql import GraphQL
from utils.mongo import Mongo

TOTAL_ITEMS = 1000
PER_PAGE = 100

def run():
    items_count = Mongo().get_documents_count()

    if items_count < TOTAL_ITEMS:
        nodes = []
        graphql = GraphQL(os.environ["API_URL"])
        last_cursor = None

        for x in range(0, ceil(TOTAL_ITEMS / PER_PAGE)):
            response = graphql.post(
                """
                query popularRepositories($lastCursor: String, $perPage: Int) {
                    search(
                        query: "stars:>100, language:Java"
                        type: REPOSITORY
                        after: $lastCursor
                        first: $perPage
                    ) {
                        nodes {
                        ... on Repository {
                            nameWithOwner
                            url
                            stargazerCount
                            createdAt
                            releases {
                                totalCount
                            }
                            primaryLanguage {
                                name
                            }
                        }
                        }
                        pageInfo {
                        endCursor
                        hasNextPage
                        }
                    }
                    }
                """,
                {
                    "lastCursor": last_cursor,
                    "perPage": min(PER_PAGE, TOTAL_ITEMS, (TOTAL_ITEMS - len(nodes))),
                },
            )
            
            last_cursor = response["data"]["search"]["pageInfo"]["endCursor"]
                        
            formatter = lambda node : {
                "nameWithOwner": node["nameWithOwner"],
                "url" : node["url"],
                "stargazerCount": node["stargazerCount"],
                "createdAt": node["createdAt"],
                "releases": node["releases"]["totalCount"],
                "primaryLanguage": node["primaryLanguage"]["name"],
                "age": (datetime.datetime.now().replace(tzinfo=None) - parse(node["createdAt"]).replace(tzinfo=None)).days,
                "processed": False
            }
            
            nodes = nodes + list(map(formatter, response["data"]["search"]["nodes"]))

            print('{} nodes of {}'.format(len(nodes), TOTAL_ITEMS))

            if not response["data"]["search"]["pageInfo"]["hasNextPage"]:
                break


        Mongo().insert_many(nodes)    

    else:
        print(f"DB já populado com {items_count} itens")    


def get_percent(x,y):
    try: 
        return (float(x) / float(y))
    except Exception:
        return 1