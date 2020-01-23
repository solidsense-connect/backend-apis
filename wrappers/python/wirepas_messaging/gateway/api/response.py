"""
    Response
    ========

    .. Copyright:
        Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

import wirepas_messaging
from .gateway_result_code import GatewayResultCode

from time import time

class Response(object):
    """
    Response

    Attributes:
        gw_id (str): unique gateway identifier
        sink_id(str): sink identifier
        req_id (int): identifier to help distinguish a response/request pair (same as in request)
        res(GatewayResultCode): result of the operation
    """

    # pylint: disable=unused-argument
    def __init__(self, req_id, gw_id, res, sink_id=None, **kwargs):
        super(Response, self).__init__()
        self.gw_id = gw_id
        self.sink_id = sink_id
        self.req_id = req_id
        self.res = res

    def __str__(self):
        return str(self.__dict__)

    @property
    def payload(self):
        """ Implement how to serialize child Event classes """
        raise NotImplementedError()

    def _make_response_header(self):
        """ Creates the generic messaging header """
        header = wirepas_messaging.gateway.ResponseHeader()
        header.req_id = self.req_id
        header.gw_id = str(self.gw_id)
        # No conversion needed as one to one mapping
        header.res = self.res.value

        if self.sink_id is not None:
            header.sink_id = str(self.sink_id)

        return header

    @staticmethod
    def _parse_response_header(header):
        """
        Parses the header details from a protobuff message

        Args:
            header (proto): proto buff message

        Returns:
            A dictionary with the header details
        """
        d = dict()
        d["req_id"] = header.req_id
        d["gw_id"] = header.gw_id
        d["res"] = GatewayResultCode(header.res)

        if header.HasField("sink_id"):
            d["sink_id"] = header.sink_id
        else:
            d["sink_id"] = None

        return d

    @staticmethod
    def add_client_status(message):
        message.customer.customer_name = "Maersk"
        message.customer.response.header.gateway_epoch_ms = int(time() * 1000)
        message.customer.response.client_resp.SetInParent()

    @staticmethod
    def add_gateway_status(message, req_id):
        message.customer.customer_name = "Maersk"
        message.customer.response.header.gateway_epoch_ms = int(time() * 1000)

        message.customer.response.gateway_resp.header.req_id = req_id
        message.customer.response.gateway_resp.header.gw_id = Response.gw_id
        message.customer.response.gateway_resp.header.res = GatewayResultCode.GW_RES_OK.value
        message.customer.response.gateway_resp.gw_status_resp.app_software = Response.firmware;
        message.customer.response.gateway_resp.gw_status_resp.wirepas_software = Response.wirepas_version
        message.customer.response.gateway_resp.gw_status_resp.imsi = Response.imsi

    @staticmethod
    def add_config_status(message, req_id, res):
        message.customer.customer_name = "Maersk"
        message.customer.response.header.gateway_epoch_ms = int(time() * 1000)

        message.customer.response.gateway_resp.header.req_id = req_id
        message.customer.response.gateway_resp.header.gw_id = Response.gw_id
        message.customer.response.gateway_resp.header.res = res.value

