import strawberry

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from services import api_router
from resolvers import Query, get_context

app = FastAPI()
app_queries = Query
schema = strawberry.Schema(query=app_queries)
graphql_app = GraphQLRouter(schema, context_getter=get_context)


def include_router(fastapi_app):
  fastapi_app.include_router(api_router)
  fastapi_app.include_router(graphql_app, prefix="/graphql")


include_router(app)
