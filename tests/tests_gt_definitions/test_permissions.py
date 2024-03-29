import logging
import os
import uuid

from .gt_utils import createFrontendQuery

def uuidstr():
    return f"{uuid.uuid1()}"



_test_request_permitted = createFrontendQuery(
    query="""query ($id: UUID!) {
        projectById(id: $id) {
            id
            name
            created
    		createdby{ id }

        }
    }""",
    variables={"id": "43dd2ff1-5c17-42a5-ba36-8b30e2a243bb"}
)

# def test_raise(AccessToken):
#     print(AccessToken)
#     assert False

import pytest


@pytest.mark.asyncio
async def test_low_role_say_hello(DemoFalse, OAuthServer, ClientExecutorNoDemo, Env_GQLUG_ENDPOINT_URL_8123):
    GQLUG_ENDPOINT_URL = os.environ.get("GQLUG_ENDPOINT_URL", None)
    logging.info(f"test_low_role GQLUG_ENDPOINT_URL: \n{GQLUG_ENDPOINT_URL}")
    DEMO = os.environ.get("DEMO", None)
    logging.info(f"test_low_role DEMO: {DEMO}")
    query = """
    query($id: UUID!) { 
        result: sayHelloProjects(id: $id)
    }
    """
    variable_values = {"id": "43dd2ff1-5c17-42a5-ba36-8b30e2a243bb"}
    result = await ClientExecutorNoDemo(query=query, variable_values=variable_values)
    logging.info(f"test_low_role_say_hello: \n {result}")
    print(result)
    errors = result.get("errors", None)
    assert errors is None, result




@pytest.mark.asyncio
async def test_demo_role(DemoFalse, ClientExecutorAdmin, FillDataViaGQL, Context, Env_GQLUG_ENDPOINT_URL_8124):
    GQLUG_ENDPOINT_URL = os.environ.get("GQLUG_ENDPOINT_URL", None)
    logging.info(f"test_low_role GQLUG_ENDPOINT_URL: \n{GQLUG_ENDPOINT_URL}")
    DEMO = os.environ.get("DEMO", None)
    logging.info(f"test_low_role DEMO: {DEMO}")
    query = """
    query($id: UUID!) { 
        result: projectById(id: $id) { 
            id           
        }
    }
    """
    variable_values = {"id": "43dd2ff1-5c17-42a5-ba36-8b30e2a243bb"}
    result = await ClientExecutorAdmin(query=query, variable_values=variable_values)
    logging.info(f"test_demo_role result: \n {result}")
    print(result)
    errors = result.get("errors", None)
    data = result.get("data", None)
    assert errors is None, result
    assert data["result"] is not None, data
    assert data["result"]["id"] == variable_values["id"], data
    

# @pytest.mark.asyncio
# async def test_low_role(DemoFalse, ClientExecutorNoAdmin, FillDataViaGQL, Context, Env_GQLUG_ENDPOINT_URL_8124):
#     GQLUG_ENDPOINT_URL = os.environ.get("GQLUG_ENDPOINT_URL", None)
#     logging.info(f"test_low_role GQLUG_ENDPOINT_URL: \n{GQLUG_ENDPOINT_URL}")
#     DEMO = os.environ.get("DEMO", None)
#     logging.info(f"test_low_role DEMO: {DEMO}")
#     query = """
#     query($id: UUID!) { 
#         result: projectById(id: $id) { 
#             id           
#         }
#     }
#     """
#     variable_values = {"id": "43dd2ff1-5c17-42a5-ba36-8b30e2a243bb"}
#     result = await ClientExecutorNoAdmin(query=query, variable_values=variable_values)
#     logging.info(f"test_demo_role result: \n {result}")
#     print(result)
#     errors = result.get("errors", None)
#     data = result.get("data", None)
#     assert errors is None, result
#     assert data["result"] is not None, data
#     assert data["result"]["id"] == variable_values["id"], data
    

# @pytest.mark.asyncio
# async def test_low_role(DemoFalse, ClientExecutorNoAdmin, FillDataViaGQL, Context, Env_GQLUG_ENDPOINT_URL_8124):
#     GQLUG_ENDPOINT_URL = os.environ.get("GQLUG_ENDPOINT_URL", None)
#     logging.info(f"test_low_role GQLUG_ENDPOINT_URL: \n{GQLUG_ENDPOINT_URL}")
#     DEMO = os.environ.get("DEMO", None)
#     logging.info(f"test_low_role DEMO: {DEMO}")
#     query = """
#     query($id: UUID!) { 
#         result: projectById(id: $id) { 
#             id           
#         }
#     }
#     """
#     variable_values = {"id": "43dd2ff1-5c17-42a5-ba36-8b30e2a243bb"}
#     result = await ClientExecutorNoAdmin(query=query, variable_values=variable_values)
#     logging.info(f"test_demo_role result: \n {result}")
#     print(result)
#     errors = result.get("errors", None)
#     data = result.get("data", None)
#     assert errors is None, result
#     assert data["result"] is not None, data
#     assert data["result"]["id"] == variable_values["id"], data
    

# @pytest.mark.asyncio
# async def test_low_role2(DemoFalse, ClientExecutorNoAdmin2, FillDataViaGQL, Context, Env_GQLUG_ENDPOINT_URL_8123):
#     GQLUG_ENDPOINT_URL = os.environ.get("GQLUG_ENDPOINT_URL", None)
#     logging.info(f"test_low_role GQLUG_ENDPOINT_URL: \n{GQLUG_ENDPOINT_URL}")
#     DEMO = os.environ.get("DEMO", None)
#     logging.info(f"test_low_role DEMO: {DEMO}")
#     query = """
#     query($id: UUID!) { 
#         result: projectById(id: $id) { 
#             id          
#         }
#     }
#     """
#     variable_values = {"id": "43dd2ff1-5c17-42a5-ba36-8b30e2a243bb"}
#     result = await ClientExecutorNoAdmin2(query=query, variable_values=variable_values)
#     logging.info(f"test_demo_role got for query \n {query} \n\t with variables \n {variable_values} \n\t the result: \n {result}")
#     print(result)
#     errors = result.get("errors", None)
#     data = result.get("data", None)
#     assert errors is None, result
#     assert data is not None, data
#     assert data.get("result", None) is not None, data
#     assert data["result"].get("id", None) == variable_values["id"], data