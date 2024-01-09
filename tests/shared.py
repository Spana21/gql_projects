import sqlalchemy
import sys
import asyncio

# setting path
sys.path.append("../gql_projects")

import pytest

# from ..uoishelpers.uuid import UUIDColumn
from gql_projects.DBDefinitions.FinanceModel import FinanceModel
from gql_projects.DBDefinitions.BaseModel import BaseModel
from gql_projects.DBDefinitions.ProjectModel import ProjectModel
from gql_projects.DBDefinitions.ProjectTypeModel import ProjectTypeModel
from gql_projects.DBDefinitions.ProjectCategoryModel import ProjectCategoryModel
from gql_projects.DBDefinitions.FinanceTypeModel import FinanceTypeModel
from gql_projects.DBDefinitions.FinanceCategory import FinanceCategory
from gql_projects.DBDefinitions.MilestoneLinkModel import MilestoneLinkModel
from gql_projects.DBDefinitions.MilestoneModel import MilestoneModel



async def prepare_in_memory_sqllite():
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker

    asyncEngine = create_async_engine("sqlite+aiosqlite:///:memory:")
    # asyncEngine = create_async_engine("sqlite+aiosqlite:///data.sqlite")
    async with asyncEngine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async_session_maker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session_maker

from gql_projects.utils.DBFeeder import get_demodata

async def prepare_demodata(async_session_maker):
    data = get_demodata()

    from uoishelpers.feeders import ImportModels

    await ImportModels(
        async_session_maker,
        [
            ProjectModel, ProjectTypeModel, ProjectCategoryModel,
            FinanceModel, FinanceTypeModel, FinanceCategory,
            MilestoneModel, MilestoneLinkModel
        ],
        data,
    )


from gql_projects.utils.Dataloaders import createLoaders


async def createContext(asyncSessionMaker):
    return {
        "asyncSessionMaker": asyncSessionMaker,
        "all": await createLoaders(asyncSessionMaker),
    }
