from typing import Optional
import strawberry
from strawberry import ID
from sqlalchemy.orm import Session
from strawberry.types import Info

from db import engine
from core import UserType, UserConnection, UserNode, PageMeta
from core.schemas.user import User
from utils.cursor_pagination import decode_cursor, encode_cursor

_db = Session(engine)


def get_users(first: Optional[int] = None, after: Optional[str] = 30) -> UserConnection:
  users_query = _db.query(User)

  users_query = users_query.order_by(User.id)
  if after:
    decoded_id = decode_cursor(after)
    users_query = users_query.filter(User.id > decoded_id)

  users = users_query.limit(first + 1).all()

  has_next_page = len(users) > first
  end_cursor = None
  if has_next_page:
    end_cursor = encode_cursor(users[first - 1].id)

  all_users = [
    UserNode(
      node=user,
      cursor=encode_cursor(user.id)
    )
    for user in users[:first]
  ]

  page_info = PageMeta(end_cursor=end_cursor, has_next_page=has_next_page)

  return UserConnection(edges=all_users, page_info=page_info)


@strawberry.type
class UserQuery:
  @strawberry.field
  def user(id: ID) -> UserType:
    user = _db.query(User).filter(User.id == id).first()
    return UserType(
      id=user.id,
      username=user.username,
      password=user.password,
      email=user.email,
    )

  @strawberry.field
  def users(self, first: Optional[int] = 10, after: Optional[str] = None) -> UserConnection:
    users = get_users(first, after)
    return users

  @strawberry.field
  def my_user(self, info: Info) -> UserType:
    context = info.context.user
    return context
