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
module: global_credential_http_write
short_description: Manage GlobalCredentialHttpWrite objects of Discovery
description:
- Adds global HTTP write credentials.
- Updates global HTTP write credentials.
version_added: '1.0'
author: first last (@GitHubID)
options:
    payload:
        description:
        - An object to send in the Request body.
        type: list
        required: True
        elements: dict
        suboptions:
            comments:
                description:
                - It is the global credential http write's comments.
                type: str
            credentialType:
                description:
                - It is the global credential http write's credentialType.
                type: str
            description:
                description:
                - It is the global credential http write's description.
                type: str
            id:
                description:
                - It is the global credential http write's id.
                type: str
            instanceTenantId:
                description:
                - It is the global credential http write's instanceTenantId.
                type: str
            instanceUuid:
                description:
                - It is the global credential http write's instanceUuid.
                type: str
            password:
                description:
                - It is the global credential http write's password.
                type: str
                required: True
            port:
                description:
                - It is the global credential http write's port.
                type: int
                required: True
            secure:
                description:
                - It is the global credential http write's secure.
                type: bool
            username:
                description:
                - It is the global credential http write's username.
                type: str
                required: True

    comments:
        description:
        - HTTPWriteCredentialDTO's comments.
        type: str
    credentialType:
        description:
        - HTTPWriteCredentialDTO's credentialType.
        - Available values are 'GLOBAL' and 'APP'.
        type: str
    description:
        description:
        - HTTPWriteCredentialDTO's description.
        type: str
    id:
        description:
        - HTTPWriteCredentialDTO's id.
        type: str
    instanceTenantId:
        description:
        - HTTPWriteCredentialDTO's instanceTenantId.
        type: str
    instanceUuid:
        description:
        - HTTPWriteCredentialDTO's instanceUuid.
        type: str
    password:
        description:
        - HTTPWriteCredentialDTO's password.
        type: str
        required: True
    port:
        description:
        - HTTPWriteCredentialDTO's port.
        type: int
        required: True
    secure:
        description:
        - HTTPWriteCredentialDTO's secure.
        type: bool
    username:
        description:
        - HTTPWriteCredentialDTO's username.
        type: str
        required: True

requirements:
- dnacentersdk
seealso:
# Reference by module name
- module: cisco.dnac.plugins.module_utils.definitions.global_credential_http_write
# Reference by Internet resource
- name: GlobalCredentialHttpWrite reference
  description: Complete reference of the GlobalCredentialHttpWrite object model.
  link: https://developer.cisco.com/docs/dna-center/api/1-3-3-x
# Reference by Internet resource
- name: GlobalCredentialHttpWrite reference
  description: SDK reference.
  link: https://dnacentersdk.readthedocs.io/en/latest/api/api.html#v2-1-1-summary
'''

EXAMPLES = r'''
'''

RETURN = r'''
data_0:
    description: Adds global HTTP write credentials.
    returned: success,changed,always
    type: dict
    contains:
        response:
            description: HTTPWriteCredentialDTO's response.
            returned: success,changed,always
            type: dict
            contains:
                taskId:
                    description: It is the global credential http write's taskId.
                    returned: success,changed,always
                    type: dict
                url:
                    description: It is the global credential http write's url.
                    returned: success,changed,always
                    type: str
                    sample: 'sample_string'

        version:
            description: HTTPWriteCredentialDTO's version.
            returned: success,changed,always
            type: str
            sample: 'sample_string'

data_1:
    description: Updates global HTTP write credentials.
    returned: success,changed,always
    type: dict
    contains:
        response:
            description: HTTPWriteCredentialDTO's response.
            returned: success,changed,always
            type: dict
            contains:
                taskId:
                    description: It is the global credential http write's taskId.
                    returned: success,changed,always
                    type: dict
                url:
                    description: It is the global credential http write's url.
                    returned: success,changed,always
                    type: str
                    sample: 'sample_string'

        version:
            description: HTTPWriteCredentialDTO's version.
            returned: success,changed,always
            type: str
            sample: 'sample_string'

'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.dnac.plugins.module_utils.dnac import ModuleDefinition, DNACModule, dnac_argument_spec
from ansible_collections.cisco.dnac.plugins.module_utils.definitions.global_credential_http_write import module_definition


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

    if state == "create":
        dnac.disable_validation()
        dnac.exec("post")

    elif state == "update":
        dnac.disable_validation()
        dnac.exec("put")

    dnac.exit_json()


if __name__ == "__main__":
    main()