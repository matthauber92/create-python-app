import strawberry

from core.types import UserType, UserConnection
from .query_resolvers import UserQuery
from middleware import IsAuthenticated


@strawberry.type
class Query:
  # USER
  user: UserType = strawberry.field(resolver=UserQuery.user, permission_classes=[IsAuthenticated])
  users: UserConnection = strawberry.field(resolver=UserQuery.users, permission_classes=[IsAuthenticated])
  my_user: UserType = strawberry.field(resolver=UserQuery.my_user, permission_classes=[IsAuthenticated])
