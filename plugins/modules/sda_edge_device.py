#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, first last <email>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '0.0.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: sda_edge_device
short_description: Manage SdaEdgeDevice objects of Sda
description:
- Delete edge device from SDA Fabric.
- Get edge device from SDA Fabric.
- Add edge device in SDA Fabric.
version_added: '1.0'
author: first last (@GitHubID)
options:
    device_ipaddress:
        description:
        - Device IP Address.
        type: str
    payload:
        description:
        - An object to send in the Request body.
        type: list
        required: True
        elements: dict
        suboptions:
            deviceManagementIpAddress:
                description:
                - It is the sda edge device's deviceManagementIpAddress.
                type: str
            siteNameHierarchy:
                description:
                - It is the sda edge device's siteNameHierarchy.
                type: str


requirements:
- dnacentersdk
seealso:
# Reference by module name
- module: cisco.dnac.plugins.module_utils.definitions.sda_edge_device
# Reference by Internet resource
- name: SdaEdgeDevice reference
  description: Complete reference of the SdaEdgeDevice object model.
  link: https://developer.cisco.com/docs/dna-center/api/1-3-3-x
# Reference by Internet resource
- name: SdaEdgeDevice reference
  description: SDK reference.
  link: https://dnacentersdk.readthedocs.io/en/latest/api/api.html#v2-1-1-summary
'''

EXAMPLES = r'''
'''

RETURN = r'''
data_0:
    description: Delete edge device from SDA Fabric.
    returned: success,changed,always
    type: dict
    contains:
        status:
            description: Status, property of the response body.
            returned: success,changed,always
            type: str
            sample: 'sample_string'
        description:
            description: Description, property of the response body.
            returned: success,changed,always
            type: str
            sample: 'sample_string'
        executionStatusUrl:
            description: Execution Status Url, property of the response body.
            returned: success,changed,always
            type: str
            sample: 'sample_string'

data_1:
    description: Get edge device from SDA Fabric.
    returned: success,changed,always
    type: dict
    contains:
        status:
            description: Status, property of the response body.
            returned: success,changed,always
            type: str
            sample: 'sample_string'
        description:
            description: Description, property of the response body.
            returned: success,changed,always
            type: str
            sample: 'sample_string'
        name:
            description: Name, property of the response body.
            returned: success,changed,always
            type: str
            sample: 'sample_string'
        roles:
            description: Roles, property of the response body (list of strings).
            returned: success,changed,always
            type: list
        deviceManagementIpAddress:
            description: Device Management Ip Address, property of the response body.
            returned: success,changed,always
            type: str
            sample: 'sample_string'
        siteHierarchy:
            description: Site Hierarchy, property of the response body.
            returned: success,changed,always
            type: str
            sample: 'sample_string'

data_2:
    description: Add edge device in SDA Fabric.
    returned: success,changed,always
    type: dict
    contains:
        status:
            description: Status, property of the response body.
            returned: success,changed,always
            type: str
            sample: 'sample_string'
        description:
            description: Description, property of the response body.
            returned: success,changed,always
            type: str
            sample: 'sample_string'
        executionStatusUrl:
            description: Execution Status Url, property of the response body.
            returned: success,changed,always
            type: str
            sample: 'sample_string'

'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.dnac.plugins.module_utils.dnac import ModuleDefinition, DNACModule, dnac_argument_spec
from ansible_collections.cisco.dnac.plugins.module_utils.definitions.sda_edge_device import module_definition


def main():

    moddef = ModuleDefinition(module_definition)

    argument_spec = dnac_argument_spec()
    argument_spec.update(moddef.get_argument_spec_dict())

    required_if = moddef.get_required_if_list()
    
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False,
        required_if=required_if
    )

    dnac = DNACModule(module, moddef)

    state = module.params.get("state")

    if state == "query":
        dnac.exec("get")

    elif state == "delete":
        dnac.exec("delete")

    elif state == "create":
        dnac.disable_validation()
        dnac.exec("post")

    dnac.exit_json()


if __name__ == "__main__":
    main()