import math
from typing import Any, List, Optional

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10
DEFAULT_MAX_PAGE_SIZE = 100
DEFAULT_TOTAL_PAGES = 0


class PagedList:

    def __init__(self, items: List[Any], total_items: int, page: int, page_size: int):
        self.items = items
        self.total_items = total_items
        self.page = page
        self.page_size = page_size
        self.total_pages = math.ceil(self.total_items / self.page_size)


class PagingParams:

    def __init__(self, page_size: Optional[int]):
        self.page = DEFAULT_PAGE
        self.__set_page_size(page_size)
        self.total_pages = DEFAULT_TOTAL_PAGES

    @property
    def limit(self) -> int:
        return self.page_size

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @staticmethod
    def create(total_items: Optional[int], page: Optional[int], page_size: Optional[int]):
        return PagingParams(page_size).__calc_total_pages(total_items).__set_page(page)

    def __set_page(self, page: Optional[int]):
        if page is None or page <= 0:
            self.page = DEFAULT_PAGE
        elif page > self.total_pages:
            self.page = self.total_pages
        else:
            self.page = page

        return self

    def __set_page_size(self, page_size: Optional[int]):
        if page_size is None or page_size <= 0:
            self.page_size = DEFAULT_PAGE_SIZE
        elif page_size > DEFAULT_MAX_PAGE_SIZE:
            self.page_size = DEFAULT_MAX_PAGE_SIZE
        else:
            self.page_size = page_size

        return self

    def __calc_total_pages(self, total_items: Optional[int]):
        if total_items is None or total_items < 0:
            self.total_pages = DEFAULT_TOTAL_PAGES
        else:
            self.total_pages = math.ceil(total_items / self.page_size)

        return self


async def paginate(session: AsyncSession, query: Select, page: int, page_size: int) -> PagedList:
    total_items = await session.scalar(select(func.count()).select_from(query.subquery()))
    paging_params = PagingParams.create(total_items, page, page_size)

    items_result = await session.execute(query.limit(paging_params.limit).offset(paging_params.offset))
    items = items_result.mappings().all()

    return PagedList(items, total_items, paging_params.page, paging_params.page_size)
