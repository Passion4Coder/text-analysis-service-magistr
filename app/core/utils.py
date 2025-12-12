import math
from typing import Any, List

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10
DEFAULT_MAX_PAGE_SIZE = 100


class PagedList:
    def __init__(self, items: List[Any], total_items: int, page, page_size):
        self.items = items
        self.total_items = total_items
        self.set_page_size(page_size)

        self.total_pages = math.ceil(self.total_items / self.page_size)
        self.set_page(page)

    def set_page(self, page):
        if page <= 0:
            self.page = DEFAULT_PAGE
        elif page > self.total_pages:
            self.page = self.total_pages
        else:
            self.page = page

    def set_page_size(self, page_size):
        if page_size <= 0:
            self.page_size = DEFAULT_PAGE_SIZE
        elif page_size > DEFAULT_MAX_PAGE_SIZE:
            self.page_size = DEFAULT_MAX_PAGE_SIZE
        else:
            self.page_size = page_size


async def paginate(session: AsyncSession, query: Select, page: int, page_size: int) -> PagedList:
    limit = page_size
    offset = (page - 1) * page_size

    total_items = await session.scalar(select(func.count()).select_from(query.subquery()))
    items_result = await session.execute(query.limit(limit).offset(offset))
    items = items_result.mappings().all()

    return PagedList(items, total_items, page, page_size)
