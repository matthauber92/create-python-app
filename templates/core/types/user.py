import strawberry
import importlib

from typing import Optional
from strawberry import ID
from typing import TYPE_CHECKING, Annotated

if TYPE_CHECKING:
  from core.types import PageMeta


@strawberry.type
class UserType:
  id: ID
  username: str
  password: str
  email: str

@strawberry.type
class UserNode:
  node: UserType
  cursor: str


@strawberry.type
class UserConnection:
  edges: list[UserNode]
  page_info: Annotated['PageMeta', strawberry.lazy("core.types.page_meta")]


import strawberry


@strawberry.input
class CreateUserInput:
  username: str
  password: str
  email: str


@strawberry.input
class UpdateUserInput:
  user_id: strawberry.ID
  username: Optional[str] = None
  password: Optional[str] = None
  email: Optional[str] = None


@strawberry.input
class DeleteUserInput:
  user_id: strawberry.ID

