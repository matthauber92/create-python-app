from typing import Optional
import strawberry


@strawberry.type
class PageMeta:
  end_cursor: Optional[str]
  has_next_page: Optional[bool]
