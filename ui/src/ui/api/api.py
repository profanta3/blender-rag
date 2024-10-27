import os
import requests

from lib.models.api import MWRequest, MWResponse


def send_user_query(query: str) -> MWResponse:

    mw_request = MWRequest(query=query)

    with requests.post(url=os.environ["MW_HOST"], data=mw_request) as r:
        return MWResponse.model_validate(r.json())
