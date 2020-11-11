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
module: sda_auth_profile
short_description: Manage SdaAuthProfile objects of Sda
description:
- Add default authentication profile in SDA Fabric.
- Get default authentication profile from SDA Fabric.
- Add default authentication profile in SDA Fabric.
- Update default authentication profile in SDA Fabric.
version_added: '1.0'
author: first last (@GitHubID)
options:
    site_name_hierarchy:
        description:
        - SiteNameHierarchy query parameter.
        type: str
    payload:
        description:
        - An object to send in the Request body.
        type: list
        required: True
        elements: dict
        suboptions:
            authenticateTemplateName:
                description:
                - It is the sda auth profile's authenticateTemplateName.
                type: str
            siteNameHierarchy:
                description:
                - It is the sda auth profile's siteNameHierarchy.
                type: str


requirements:
- dnacentersdk
seealso:
# Reference by module name
- module: cisco.dnac.plugins.module_utils.definitions.sda_auth_profile
# Reference by Internet resource
- name: SdaAuthProfile reference
  description: Complete reference of the SdaAuthProfile object model.
  link: https://developer.cisco.com/docs/dna-center/api/1-3-3-x
# Reference by Internet resource
- name: SdaAuthProfile reference
  description: SDK reference.
  link: https://dnacentersdk.readthedocs.io/en/latest/api/api.html#v2-1-1-summary
'''

EXAMPLES = r'''
'''

RETURN = r'''
data_0:
    description: Add default authentication profile in SDA Fabric.
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
    description: Get default authentication profile from SDA Fabric.
    returned: success,changed,always
    type: dict
    contains:
        siteNameHierarchy:
            description: Site Name Hierarchy, property of the response body.
            returned: success,changed,always
            type: str
            sample: 'sample_string'
        authenticateTemplateName:
            description: Authenticate Template Name, property of the response body.
            returned: success,changed,always
            type: str
            sample: 'sample_string'
        authenticateTemplateId:
            description: Authenticate Template Id, property of the response body.
            returned: success,changed,always
            type: str
            sample: 'sample_string'

data_2:
    description: Add default authentication profile in SDA Fabric.
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

data_3:
    description: Update default authentication profile in SDA Fabric.
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
from ansible_collections.cisco.dnac.plugins.module_utils.definitions.sda_auth_profile import module_definition


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

    elif state == "update":
        dnac.disable_validation()
        dnac.exec("put")

    dnac.exit_json()


if __name__ == "__main__":
    main()