#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2021, Cisco Systems
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: discovery_device_range_info
short_description: Information module for Discovery Device Range
description:
- Get all Discovery Device Range.
version_added: '3.1.0'
extends_documentation_fragment:
  - cisco.dnac.module_info
author: Rafael Campos (@racampos)
options:
  headers:
    description: Additional headers.
    type: dict
  id:
    description:
    - Id path parameter. Discovery ID.
    type: str
  startIndex:
    description:
    - StartIndex path parameter. Start index.
    type: int
  recordsToReturn:
    description:
    - RecordsToReturn path parameter. Number of records to return.
    type: int
  taskId:
    description:
    - TaskId query parameter.
    type: str
requirements:
- dnacentersdk >= 2.3.1
- python >= 3.5
seealso:
# Reference by Internet resource
- name: Discovery Device Range reference
  description: Complete reference of the Discovery Device Range object model.
  link: https://dnacentersdk.readthedocs.io/en/latest/api/api.html#v3-0-0-summary
"""

EXAMPLES = r"""
- name: Get all Discovery Device Range
  cisco.dnac.discovery_device_range_info:
    dnac_host: "{{dnac_host}}"
    dnac_username: "{{dnac_username}}"
    dnac_password: "{{dnac_password}}"
    dnac_verify: "{{dnac_verify}}"
    dnac_port: "{{dnac_port}}"
    dnac_version: "{{dnac_version}}"
    dnac_debug: "{{dnac_debug}}"
    headers:
      custom: value
    taskId: string
    id: string
    startIndex: 0
    recordsToReturn: 0
  register: result

"""

RETURN = r"""
dnac_response:
  description: A dictionary or list with the response returned by the Cisco DNAC Python SDK
  returned: always
  type: dict
  sample: >
    {
      "response": [
        {
          "anchorWlcForAp": "string",
          "authModelId": "string",
          "avgUpdateFrequency": 0,
          "bootDateTime": "string",
          "cliStatus": "string",
          "duplicateDeviceId": "string",
          "errorCode": "string",
          "errorDescription": "string",
          "family": "string",
          "hostname": "string",
          "httpStatus": "string",
          "id": "string",
          "imageName": "string",
          "ingressQueueConfig": "string",
          "interfaceCount": "string",
          "inventoryCollectionStatus": "string",
          "inventoryReachabilityStatus": "string",
          "lastUpdated": "string",
          "lineCardCount": "string",
          "lineCardId": "string",
          "location": "string",
          "locationName": "string",
          "macAddress": "string",
          "managementIpAddress": "string",
          "memorySize": "string",
          "netconfStatus": "string",
          "numUpdates": 0,
          "pingStatus": "string",
          "platformId": "string",
          "portRange": "string",
          "qosStatus": "string",
          "reachabilityFailureReason": "string",
          "reachabilityStatus": "string",
          "role": "string",
          "roleSource": "string",
          "serialNumber": "string",
          "snmpContact": "string",
          "snmpLocation": "string",
          "snmpStatus": "string",
          "softwareVersion": "string",
          "tag": "string",
          "tagCount": 0,
          "type": "string",
          "upTime": "string",
          "vendor": "string",
          "wlcApDeviceStatus": "string"
        }
      ],
      "version": "string"
    }
"""