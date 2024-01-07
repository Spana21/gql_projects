import pytest
from tests.tests_gt_definitions.gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_financetypes = createResolveReferenceTest(tableName='projectfinancetypes', gqltype='FinanceTypeItemGQLModel', attributeNames=["id", "name", "lastchange", "name_en"])

test_query_finance_type_by_id = createByIdTest(tableName="projectfinancetypes", queryEndpoint="financeTypeById")
test_query_finance_type_page = createPageTest(tableName="projectfinancetypes", queryEndpoint="financeTypePage")

test_insert_finance_type = createFrontendQuery(query="""
    mutation($id: UUID!, $name: String!, $name_en: String!) { 
        result: FinanceTypeInsert(finance: {id: $id, name: $name, nameEn: $name_en}) { 
            id
            msg
            finance {
                id
                name
                name_en
            }
        }
    }
    """, 
    variables={"id": "ee50b3bf-ac51-4dbb-8f73-d5da30bf8017", "name": "new finance", "name_en": "new en Finance"},
    asserts=[]
)


test_update_finance_type = createUpdateQuery(
    query="""
        mutation($id: UUID!, $name: String!, $lastchange: DateTime!,) {
            FinanceTypeUpdate(finance: {id: $id, name: $name, lastchange: $lastchange}) {
                id
                msg
                finance {
                    id
                    name
                    lastchange
                }
            }
        }

    """,
    variables={"id": "9e37059c-de2c-4112-9009-559c8b0396f1", "name": "new name"},
    tableName="projectfinancetypes"
)