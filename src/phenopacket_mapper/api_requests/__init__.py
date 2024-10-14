"""This module is intended to provide a set of functions that will be used to make requests to the APIs of various code
systems."""


from .api_request_super_class import APIRequestSuperClass
from .get import get
from .orpha_api_request import OrphaAPIRequest
from .hpo_api_request import HPOAPIRequest

__all__ = [
    "APIRequestSuperClass",
    "get",
    "OrphaAPIRequest",
    "HPOAPIRequest",

]
