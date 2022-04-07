
async def test_hello_handler(jp_serverapp, jp_fetch):
    assert "contrib_hour" in jp_serverapp.extension_manager.extensions

    resp = await jp_fetch("hello")
    assert resp.code == 200
