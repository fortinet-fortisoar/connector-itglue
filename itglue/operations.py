""" Copyright start
  Copyright (C) 2008 - 2022 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """

import requests
from connectors.core.connector import get_logger, ConnectorError

logger = get_logger('itglue')

errors = {
    400: 'Invalid Argument/Invalid Time Range',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Method Not Allowed',
    415: 'Bad Content Type',
    422: 'Bad Request'
}


class ITGlue:
    def __init__(self, config, *args, **kwargs):
        self.api_key = config.get('api_key')
        url = config.get('server').strip('/')
        if not url.startswith('https://') and not url.startswith('http://'):
            self.url = 'https://{0}/'.format(url)
        else:
            self.url = url + '/'
        self.sslVerify = config.get('verify_ssl')

    def make_rest_call(self, endpoint, params=None, data=None, method='GET'):

        try:
            url = self.url + endpoint
            headers = {'Content-Type': 'application/vnd.api+json', 'x-api-key': 'ITG.' + self.api_key}
            response = requests.request(method, url, headers=headers, verify=self.sslVerify, data=data, params=params)
            if response.ok or response.status_code == 200:
                logger.info('Successfully got response for url {0}'.format(url))
                if 'json' in str(response.headers):
                    return response.json()
                else:
                    return response.content
            else:
                raise ConnectorError("{0}".format(errors.get(response.status_code, '')))
        except requests.exceptions.SSLError:
            raise ConnectorError('SSL certificate validation failed')
        except requests.exceptions.ConnectTimeout:
            raise ConnectorError('The request timed out while trying to connect to the server')
        except requests.exceptions.ReadTimeout:
            raise ConnectorError(
                'The server did not send any data in the allotted amount of time')
        except requests.exceptions.ConnectionError:
            raise ConnectorError('Invalid endpoint or credentials')
        except Exception as err:
            raise ConnectorError(str(err))


def build_payload(params):
    payload = {k: v for k, v in params.items() if v is not None and v != ''}
    logger.debug("Query Parameters: {0}".format(payload))
    return payload


def get_organizations(config, params):
    try:
        itg = ITGlue(config)
        endpoint = "organizations"
        payload = {
            'filter[id]': params.get('org_id'),
            'filter[name]': params.get('org_name'),
            'filter[organization_type_id]': params.get('org_type_id'),
            'filter[organization_status_id]': params.get('org_status_id'),
            'filter[created_at]': params.get('created_at'),
            'filter[updated_at]': params.get('updated_at'),
            'page[number]': params.get('page_size'),
            'page[size]': params.get('page_number')
        }
        additional_fields = params.get('additional_fields')
        if additional_fields:
            payload.update(additional_fields)
        payload = build_payload(payload)
        response = itg.make_rest_call(endpoint, 'GET', params=payload)
        return response.get('data')
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def get_locations(config, params):
    org_id = params.get('org_id')
    try:
        itg = ITGlue(config)
        endpoint = "organizations/{0}/relationships/locations".format(org_id)
        payload = {
            'filter[id]': params.get('loc_id'),
            'filter[name]': params.get('loc_name'),
            'filter[country_id]': params.get('country_id'),
            'filter[region_id]': params.get('region_id'),
            'page[number]': params.get('page_size'),
            'page[size]': params.get('page_number')
        }
        additional_fields = params.get('additional_fields')
        if additional_fields:
            payload.update(additional_fields)
        payload = build_payload(payload)
        response = itg.make_rest_call(endpoint, 'GET', params=payload)
        return response.get('data')
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def get_configurations(config, params):
    org_id = params.get('org_id')
    try:
        itg = ITGlue(config)
        endpoint = "organizations/{0}/relationships/configurations".format(org_id)
        payload = {
            'filter[id]': params.get('config_id'),
            'filter[name]': params.get('config_name'),
            'filter[configuration_type_id]': params.get('config_type_id'),
            'filter[configuration_status_id]': params.get('config_status_id'),
            'page[number]': params.get('page_size'),
            'page[size]': params.get('page_number')
        }
        additional_fields = params.get('additional_fields')
        if additional_fields:
            payload.update(additional_fields)
        payload = build_payload(payload)
        response = itg.make_rest_call(endpoint, 'GET', params=payload)
        return response.get('data')
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def get_domains(config, params):
    org_id = params.get('org_id')
    try:
        itg = ITGlue(config)
        endpoint = "organizations/{0}/relationships/domains".format(org_id)
        payload = {
            'filter[id]': params.get('domain_id'),
            'page[number]': params.get('page_size'),
            'page[size]': params.get('page_number')
        }
        additional_fields = params.get('additional_fields')
        if additional_fields:
            payload.update(additional_fields)
        payload = build_payload(payload)
        response = itg.make_rest_call(endpoint, 'GET', params=payload)
        return response.get('data')
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def get_flexible_asset(config, params):
    try:
        itg = ITGlue(config)
        endpoint = "flexible_assets"
        payload = {
            'filter[flexible-asset-type-id]': params.get('flex_type_id'),
            'filter[name]': params.get('flexible_asset_name'),
            'filter[organization-id]': params.get('org_id'),
            'page[number]': params.get('page_size'),
            'page[size]': params.get('page_number')
        }
        additional_fields = params.get('additional_fields')
        if additional_fields:
            payload.update(additional_fields)
        payload = build_payload(payload)
        response = itg.make_rest_call(endpoint, 'GET', params=payload)
        return response.get('data')
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def _check_health(config):
    try:
        response = get_organizations(config, params={})
        if response:
            return True
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


operations = {
    'get_organizations': get_organizations,
    'get_locations': get_locations,
    'get_configurations': get_configurations,
    'get_domains': get_domains,
    'get_flexible_asset': get_flexible_asset
}
