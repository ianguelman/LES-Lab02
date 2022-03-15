from math import ceil
import os, datetime
from dateutil.parser import parse
from types import NoneType
from utils.graphql import GraphQL
from utils.mongo import Mongo

TOTAL_ITEMS = 1000
PER_PAGE = 25

def run():
    items_count = Mongo().get_documents_count()

    if items_count < TOTAL_ITEMS:
        nodes = []
        graphql = GraphQL(os.environ["API_URL"])
        last_cursor = None

        for x in range(0, ceil(TOTAL_ITEMS / PER_PAGE)):
            response = graphql.post(
                """
                query popularRepositories ($lastCursor: String, $perPage: Int) {
                    search(query: "stars:>100", type: REPOSITORY, after: $lastCursor, first: $perPage) {
                        nodes {
                        ... on Repository {
                                nameWithOwner
                                url
                                stargazerCount
                                createdAt
                                pullRequests(first: 10, states: MERGED) {
                                    totalCount
                                }
                                releases {
                                    totalCount
                                }
                                updatedAt
                                primaryLanguage {
                                    name
                                }
                                issues (first: 10){
                                    totalCount
                                }
                                closed: issues(first: 10, states: CLOSED) {
                                    totalCount
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
                "pullRequests": node["pullRequests"]["totalCount"],
                "releases": node["releases"]["totalCount"],
                "updatedAt": node["updatedAt"],
                "issues": node["issues"]["totalCount"],
                "closed": node["closed"]["totalCount"],
                "ratioOpenClosedIssues": get_percent(node["closed"]["totalCount"], node["issues"]["totalCount"]),
                "updateFrequency": (datetime.datetime.now().replace(tzinfo=None) - parse(node["updatedAt"]).replace(tzinfo=None)).total_seconds()/60,
                "age": (datetime.datetime.now().replace(tzinfo=None) - parse(node["createdAt"]).replace(tzinfo=None)).days
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