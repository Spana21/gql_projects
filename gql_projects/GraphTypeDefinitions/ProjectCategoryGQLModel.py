from typing import List, Union, Annotated, Optional
import strawberry as strawberryA
import datetime
import typing
import uuid
import strawberry
from gql_projects.utils.DBFeeder import randomDataStructure
from gql_projects.utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

from gql_projects.GraphResolvers import (
    resolveProjectAll,
    resolveProjectById,
    resolveProjectsForGroup,
    resolveFinancesForProject
)

@strawberryA.federation.type(
    keys=["id"], 
    description="""Entity representing a project"""
)

class ProjectCategoryGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
        loader = getLoadersFromInfo(info).projectcategories
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> uuid.UUID:
        return self.id

    @strawberryA.field(description="""Name of the project""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Name en""")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="""End date""")
    def enddate(self) -> datetime.date:
        return self.enddate

    @strawberryA.field(description="""Last change""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

###########################################################################################################################
#
# Query 
#
###########################################################################################################################

from contextlib import asynccontextmanager

@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass

from dataclasses import dataclass
from .utils import createInputs
@createInputs
@dataclass
class ProjectCategoryWhereFilter:
    name: str
    type_id: uuid.UUID
    value: str

@strawberryA.field(description="""Returns a list of projects""")
async def project_category_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[ProjectCategoryWhereFilter] = None
) -> List[ProjectCategoryGQLModel]:
    # otazka: musi tady byt async? 
    # async with withInfo(info) as session:
    loader = getLoadersFromInfo(info).projectcategories
    wf = None if where is None else strawberry.asdict(where)
    #result = await resolveProjectAll(session, skip, limit)
    result = await loader.page(skip, limit, where = wf)
    return result

###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################
from typing import Optional

@strawberryA.input(description="Definition of a project used for creation")
class ProjectCategoryInsertGQLModel:
    name: str = strawberryA.field(description="Name/label of the project")
    
    name_en: str = strawberryA.field(description="", default=None)
    id: Optional[uuid.UUID] = strawberryA.field(description="Primary key (UUID), could be client-generated", default=None)
    createdby: strawberry.Private[uuid.UUID] = None 

@strawberryA.input(description="Definition of a project used for update")
class ProjectCategoryUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the project")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

    name: Optional[str] = strawberryA.field(description="The name of the project (optional)", default=None)
    name_en: Optional[str] = strawberryA.field(description="The name of the project (optional)", default=None)
    changedby: strawberry.Private[uuid.UUID] = None


@strawberryA.type(description="Result of a mutation over Project")
class ProjectCategoryResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the project", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the project")
    async def project(self, info: strawberryA.types.Info) -> Union[ProjectCategoryGQLModel, None]:
        result = await ProjectCategoryGQLModel.resolve_reference(info, self.id)
        return result


@strawberryA.mutation(description="Adds a new project.")
async def project_category_insert(self, info: strawberryA.types.Info, project: ProjectCategoryInsertGQLModel) -> ProjectCategoryResultGQLModel:
    # user = getUserFromInfo(info)
    # project.createdby = uuid.UUID(user["id"])

    loader = getLoadersFromInfo(info).projectcategories
    row = await loader.insert(project)
    result = ProjectCategoryResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the project.")
async def project_category_update(self, info: strawberryA.types.Info, project: ProjectCategoryUpdateGQLModel) -> ProjectCategoryResultGQLModel:
    # user = getUserFromInfo(info)
    # project.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).projectcategories
    row = await loader.update(project)
    result = ProjectCategoryResultGQLModel()
    result.msg = "ok"
    result.id = project.id
    if row is None:
        result.msg = "fail"
    return result