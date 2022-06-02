import json


async def test_get(jp_fetch):
    response = await jp_fetch(
        "server_database_extension",
        "get_example"
    )

    assert response.code == 200
    payload = json.loads(response.body)
    assert payload == {
        "data": "This is /server_database_extension/get_example endpoint!"
    }
