# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from fastapi.openapi.models import Example

from msconsparser.adapters.inbound.rest.apis.mscons_parser_api_base import BaseMSCONSParserApi
import msconsparser.adapters.inbound.rest.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from msconsparser.adapters.inbound.rest.models.extra_models import TokenModel  # noqa: F401
from pydantic import Field, StrictBool, StrictStr
from typing_extensions import Annotated


router = APIRouter()

ns_pkg = msconsparser.adapters.inbound.rest.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/download-parsed-raw-format",
    responses={
        201: {"model": object, "description": "Created"},
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
    },
    tags=["MSCONS Parser"],
    summary="Trigger the process to parse the provided mscons messages as string format and download the result as a JSON file.",
    response_model_by_alias=True,
)
async def download_parsed_result(
    body: Annotated[
        StrictStr,
        Field(description="The raw MSCONS message as plain text.")] = Body(
            None,
            description="The raw MSCONS message as plain text.",
            media_type="text/plain",
            openapi_examples={
                "insert_your_data": Example(
                    summary="Insert your data",
                    description="The raw MSCONS message as plain text.",
                    value=""
                ),
                "mscons_sample": Example(
                    summary="Raw MSCONS sample",
                    description="The raw MSCONS message as plain text.",
                    value="""UNA:+.? '
UNB+UNOC:3+4012345678901:14+4012345678901:14+200426:1151+ABC4711++TL++++1'
UNH+1+MSCONS:D:04B:UN:2.4c+UNB_DE0020_nr_1+1:C'
BGM+7+MSI5422+9'
DTM+137:202106011315?+00:303'
RFF+AGI:AFN9523'
DTM+293:20210601060030?+00:304'
NAD+MS+9920455302123::293'
CTA+IC+:P GETTY'
COM+no-reply@example.com:EM'
NAD+MR+4012345678901::9'
UNS+D'
NAD+DP'
LOC+237+11XUENBSOLS----X+11XVNBSOLS-----X'
DTM+163:202102012300?+00:303'
DTM+164:202102022300?+00:303'
LIN+1'
PIA+5+1-1?:1.29.1:SRW'
QTY+220:4250.465:D54'
DTM+163:202101012300?+00:303'
DTM+164:202101312315?+00:303'
QTY+220:4250.465:D54'
DTM+163:202101312315?+00:303'
DTM+164:202101312320?+00:303'
UNT+2+1'
UNZ+1+ABC4711'"""
                )
            }
        ),
) -> object:
    if not BaseMSCONSParserApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseMSCONSParserApi.subclasses[0]().download_parsed_result(body)


@router.post(
    "/parse-raw-format",
    responses={
        200: {"model": object, "description": "OK"},
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
    },
    tags=["MSCONS Parser"],
    summary="Trigger the process to parse the provided mscons messages as string format.",
    response_model_by_alias=True,
)
async def parse_mscons_raw_format(
    limit_mode: Annotated[StrictBool, Field(description="If true, enables the parsing limit for max number of lines, as per default it is maximum 2442 lines.")] = Query(True, description="If true, enables the parsing limit for max number of lines, as per default it is maximum 2442 lines.", alias="limit_mode"),
    body: Annotated[
        StrictStr,
        Field(description="The raw MSCONS message as plain text.")] = Body(
            None,
            description="The raw MSCONS message as plain text.",
            media_type="text/plain",
            openapi_examples={
                "insert_your_data": Example(
                    summary="Insert your data",
                    description="The raw MSCONS message as plain text.",
                    value=""
                ),
                "mscons_sample": Example(
                    summary="Raw MSCONS sample",
                    description="The raw MSCONS message as plain text.",
                    value="""UNA:+.? '
UNB+UNOC:3+4012345678901:14+4012345678901:14+200426:1151+ABC4711++TL++++1'
UNH+1+MSCONS:D:04B:UN:2.4c+UNB_DE0020_nr_1+1:C'
BGM+7+MSI5422+9'
DTM+137:202106011315?+00:303'
RFF+AGI:AFN9523'
DTM+293:20210601060030?+00:304'
NAD+MS+9920455302123::293'
CTA+IC+:P GETTY'
COM+no-reply@example.com:EM'
NAD+MR+4012345678901::9'
UNS+D'
NAD+DP'
LOC+237+11XUENBSOLS----X+11XVNBSOLS-----X'
DTM+163:202102012300?+00:303'
DTM+164:202102022300?+00:303'
LIN+1'
PIA+5+1-1?:1.29.1:SRW'
QTY+220:4250.465:D54'
DTM+163:202101012300?+00:303'
DTM+164:202101312315?+00:303'
QTY+220:4250.465:D54'
DTM+163:202101312315?+00:303'
DTM+164:202101312320?+00:303'
UNT+2+1'
UNZ+1+ABC4711'"""
                )
            }
        ),
) -> object:
    if not BaseMSCONSParserApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseMSCONSParserApi.subclasses[0]().parse_mscons_raw_format(limit_mode, body)
