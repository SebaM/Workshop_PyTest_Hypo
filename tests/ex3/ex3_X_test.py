from http.client import HTTPException

import pytest


@pytest.mark.negative
def test_create_mug_with_null_name(shopen_client):
    """
    Using null as name should result in 400.
    """
    # GIVEN
    mug = None
    name = None

    # WHEN
    try:
        mug = shopen_client.mug.create_mug({"name": name})
        # note(f'MUG name {mug["name"]} has id {mug["id"]}')
    # THEN
    except HTTPException as _exp:
        assert _exp.status == 400
        assert "Validation failed for argument" in str(_exp)

    # TEARDOWN
    finally:
        if mug and "id" in mug:
            shopen_client.mug.delete_mug(mug["id"])
