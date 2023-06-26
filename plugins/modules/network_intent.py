

import copy

try:
    from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
        AnsibleArgSpecValidator,
    )
except ImportError:
    ANSIBLE_UTILS_IS_INSTALLED = False
else:
    ANSIBLE_UTILS_IS_INSTALLED = True
from ansible_collections.cisco.dnac.plugins.module_utils.dnac import (
    DNACSDK,
    dnac_argument_spec,
    validate_list_of_dicts,
    log,
    get_dict_result,
    dnac_compare_equality,
)
from ansible.module_utils.basic import AnsibleModule


class DnacNetwork:
    def __init__(self, module):
        self.module = module
        self.params = module.params
        self.config = copy.deepcopy(module.params.get("config"))
        self.have = {}
        self.want = {}
        self.have_reserve = {}
        self.want_reserve = {}
        self.site_id = None
        self.validated = []
        dnac_params = self.get_dnac_params(self.params)
        log(str(dnac_params))
        self.dnac = DNACSDK(params=dnac_params)
        self.log = dnac_params.get("dnac_log")

        self.result = dict(changed=False, diff=[], response=[], warnings=[])


    def get_state(self):
        return self.params.get("state")

    
    def validate_input(self):

        temp_spec = dict(
            IpAddressSpace = dict(required = False, type="string"),
            dhcpServerIps = dict(required = False, type="list"),
            dnsServerIps = dict(required = False, type="list"),
            gateway = dict(required = False, type="string"),
            ipPoolCidr = dict(required = False, type="string"),
            ipPoolName = dict(required = False, type="string"),
            name = dict(required = False, type="string"),
            prev_name = dict(required = False, type="string"),
            type = dict(required = False, type = "string", choices=["generic", "tunnel", "LAN", "WAN", "management", "service"]),
            ipv6AddressSpace = dict(required = False, type = "string"),
            ipv4GlobalPool = dict(required = False, type = "string"),
            ipv4Prefix = dict(required = False, type = "string"),
            ipv4PrefixLength = dict(required = False, type = "integer"),
            ipv4GateWay = dict(required = False, type = "string"),
            ipv4DhcpServers = dict(required = False, type = "list"),
            ipv4DnsServers = dict(required =False, type = "list"),
            ipv6GlobalPool = dict(required = False, type = "string"),
            ipv6Prefix = dict(required = False, type = "string"),
            ipv6PrefixLength = dict(required = False, type = "integer"),
            ipv6GateWay = dict(required = False, type = "string"),
            ipv6DhcpServers = dict(required = False, type = "list"),
            ipv6DnsServers = dict(required = False, type = "list"),
            ipv4TotalHost = dict(required = False, type = "integer"),
            ipv6TotalHost = dict(required = False, type = "integer"),
            slaacSupport = dict(required = False, type = "string"),
            siteName = dict(required = False, type = "string")

        )
        if self.config:
            msg = None
            temp = []
            temp1 = []
            # Validate template params
            if self.config[0].get("GlobalPoolDetails") != None:
                temp = self.config[0].get("GlobalPoolDetails").get("settings").get("ippool")
            
            if self.config[0].get("ReservePoolDetails") != None:
                temp1 = [self.config[0].get("ReservePoolDetails")]

            temp = temp + temp1
            valid_temp, invalid_params = validate_list_of_dicts(
                temp, temp_spec
            )
            if invalid_params:
                msg = "Invalid parameters in playbook: {0}".format(
                    "\n".join(invalid_params)
                )
                self.module.fail_json(msg=msg)
            log(str(invalid_params))
            self.validated = valid_temp

            if self.log:
                log(str(valid_temp))
                log(str(self.result))
##                log(str(self.validated))

            log(str(self.validated))
            if self.params.get("config")[0].get("GlobalPoolDetails") != None:
                for temp in self.validated:
                    log(str(temp))
    ##                self.params.get("config")[0].get("GlobalPoolDetails").get("settings").get("ippool")[0]
                    if self.params.get("config")[0].get("GlobalPoolDetails").get("ipPoolName") != None:
                        msg = "missing required arguments: ipPoolName"
                        self.module.fail_json(msg=msg)

                    
    def get_dnac_params(self, params):
        dnac_params = dict(
            dnac_host=params.get("dnac_host"),
            dnac_port=params.get("dnac_port"),
            dnac_username=params.get("dnac_username"),
            dnac_password=params.get("dnac_password"),
            dnac_verify=params.get("dnac_verify"),
            dnac_debug=params.get("dnac_debug"),
            dnac_log=params.get("dnac_log"),
        )
        return dnac_params


    def requires_update(self, have, want, obj_params):
        current_obj = have
        requested_obj = want
        log(str(current_obj))
        log(str(requested_obj))
        
        
        return any(not dnac_compare_equality(current_obj.get(dnac_param),
                                             requested_obj.get(ansible_param))
                   for(dnac_param, ansible_param) in obj_params)


    def get_pool_id_from_name(self, pool_name):
        pool_id = None
        current_details = None
        try:
            
            response = self.dnac._exec(
                family = "network_settings",
                function = "get_global_pool",
            )

            if isinstance(response, dict):
                if "response" in response:
                    response = response.get("response")
            log(str(response))         
            current_details = get_dict_result(response, "ipPoolName", pool_name)
            log(str(current_details))
            if current_details:
                pool_id = current_details.get("id")
        
        except:
            result = None

        return (pool_id, current_details)
        

    def get_res_id_from_name(self, res_name):
        id = ""
        current_details = None
        try:
            response = self.dnac._exec(
                family="network_settings",
                function="get_reserve_ip_subpool",
                params={"site_id": self.site_id}
            )

            if isinstance(response, dict):
                if "response" in response:
                    response = response.get("response")
            log(str(response))  
            current_details = get_dict_result(response, "groupName", res_name)
            log(str(current_details))

            id = current_details.get("id")
        except:
            log("except")
            result = None
        return id


    def get_current_pool(self, pool):
        log(str(pool))
        pool_values = dict(
            settings = dict(
                    ippool = [dict(
                            dhcpServerIps = pool.get("dhcpServerIps"),
                            dnsServerIps = pool.get("dnsServerIps"),
                            ipPoolCidr = pool.get("ipPoolCidr"),
                            ipPoolName = pool.get("ipPoolName"),
                            type = pool.get("type"),
                        )]
                )
        )
        log(str(pool_values))
        if pool.get("ipv6") == False:
            pool_values.get("settings").get("ippool")[0].update({"IpAddressSpace": "IPv4"})
            log("ipv6 - false")
        else:
            pool_values.get("settings").get("ippool")[0].update({"IpAddressSpace": "IPv6"})
            log("ipv6 - true")
        if not pool["gateways"]:
            pool_values.get("settings").get("ippool")[0].update({"gateway": ""})
        else:
            pool_values.get("settings").get("ippool")[0].update({"gateway": pool.get("gateways")[0]})

        return pool_values


    def get_current_res(self, res):
        log(str(res))
        res_values = dict(
            name = res.get("groupName"),
            site_id = res.get("siteId"),
        )        

        if len(res.get("ipPools")) == 1:
            res_values.update({"ipv4DhcpServers": res.get("ipPools")[0].get("dhcpServerIps")})
            res_values.update({"ipv4DnsServers": res.get("ipPools")[0].get("dnsServerIps")})
            res_values.update({"ipv4GateWay": res.get("ipPools")[0].get("gateways")[0]})
            res_values.update({"ipv6AddressSpace": "False"})

        elif len(res.get("ipPools")) == 2:
            if res.get("ipPools")[0].get("ipv6") == False:
                res_values.update({"ipv4DhcpServers": res.get("ipPools")[0].get("dhcpServerIps")})
                res_values.update({"ipv4DnsServers": res.get("ipPools")[0].get("dnsServerIps")})
                res_values.update({"ipv4GateWay": res.get("ipPools")[0].get("gateways")[0]})
                res_values.update({"ipv6AddressSpace": "True"})
                res_values.update({"ipv4DhcpServers": res.get("ipPools")[1].get("dhcpServerIps")})
                res_values.update({"ipv4DnsServers": res.get("ipPools")[1].get("dnsServerIps")})
                res_values.update({"ipv4GateWay": res.get("ipPools")[1].get("gateways")[0]})

            elif res.get("ipPools")[1].get("ipv6") == False:
                res_values.update({"ipv4DhcpServers": res.get("ipPools")[1].get("dhcpServerIps")})
                res_values.update({"ipv4DnsServers": res.get("ipPools")[1].get("dnsServerIps")})
                res_values.update({"ipv4GateWay": res.get("ipPools")[1].get("gateways")[0]})
                res_values.update({"ipv6AddressSpace": "True"})
                res_values.update({"ipv4DhcpServers": res.get("ipPools")[0].get("dhcpServerIps")})
                res_values.update({"ipv4DnsServers": res.get("ipPools")[0].get("dnsServerIps")})
                res_values.update({"ipv4GateWay": res.get("ipPools")[0].get("gateways")[0]})
        
        return res_values

    def get_site_id(self, site_name):

        response = {}
        _id = None
        result = None
        try:
            response = self.dnac._exec(
                family="sites",
                function='get_site',
                params={"name":site_name},
            )
        
        except:
            result = None
        log(str(response))
        if not response:
            log("Invalid site name or site not present")
            self.result["response"] = []
            self.result["msg"] = "Invalid site name or site not present"
            self.module.fail_json(**self.result)
        else:
            _id = response.get("response")[0].get("id")
        log(str(_id))

        return _id


    def pool_exists(self):
        pool_exists = False
        pool_details = {}
        pool_id = None
        response = None
        name = None

      #get it from validated

        name = self.params.get("config")[0].get("GlobalPoolDetails").get("settings").get("ippool")[0].get("ipPoolName")
        try:
            
            response = self.dnac._exec(
                family = "network_settings",
                function = "get_global_pool",
            )
            log(str(response))  
            if isinstance(response, dict):
                if "response" in response:
                    response = response.get("response")
                   
            current_details = get_dict_result(response, "ipPoolName", name)
            log(str(current_details))
            if current_details:
                pool_exists = True
                pool_id = current_details.get("id")
            elif self.config[0].get("GlobalPoolDetails").get("settings").get("ippool")[0].get("prev_name") != None:
                pool_id = None
                (pool_id, current_details) = self.get_pool_id_from_name(self.config[0].get("GlobalPoolDetails").get("settings").get("ippool")[0].get("prev_name"))
                if pool_id == None:
                    msg = "Prev name doesn't exist\n"
                    self.module.fail_json(msg=msg)
                pool_exists = True
                current_details = get_dict_result(response, "id", pool_id)
                log(str(current_details))
            pool_details = self.get_current_pool(current_details)
        except Exception:
            result = None

        log(str(pool_details))
        log(str(pool_id))
        return (pool_exists, pool_details, pool_id)


    def res_exists(self):
        current_details = None
        res_exists = False
        res_details = None
        res_id = None
        response = None
        site_name = None
        _id = ""
        site_name = self.params.get("config")[0].get("ReservePoolDetails").get("siteName")
        log(str(site_name))

        if site_name != None:
            site_id = self.get_site_id(site_name)
            self.site_id = site_id

        name = self.config[0].get("ReservePoolDetails").get("name")
        prev_name =  self.config[0].get("ReservePoolDetails").get("prev_name")

        if prev_name:
            if not self.params.get("config")[0].get("ReservePoolDetails").get("siteName"):
                msg = "Mandatory Parameter siteName required\n"
                self.module.fail_json(msg=msg)
            _id = self.get_res_id_from_name(prev_name)
            
        log(str(_id))
        try:
            response = self.dnac._exec(
                family="network_settings",
                function="get_reserve_ip_subpool",
                params={"siteId":self.site_id}
            )
            if isinstance(response, dict):
                if "response" in response:
                    response = response.get("response")
            log(str(response))

            if _id:
                current_details = get_dict_result(response, "id", _id)
            elif name: 
                current_details = get_dict_result(response, "groupName", name)                 
                # o_id = current_details.get("id")

            
                
            # if name and _id and _id != o_id:
            #     msg = "Name and Id does belong to the same object\n"
            #     self.module.fail_json(msg=msg)

            log(str(current_details))

            if current_details:
                res_exists = True
                res_id = current_details.get("id")
                res_details = self.get_current_res(current_details)
        except Exception:
            result = None
        
        log(str(res_details))
        log(str(res_id))
        return (res_exists, res_details, res_id)


    def get_have(self):
        pool_exists = False
        pool_details = None
        pool_id = None
        have = dict()
        res_exists = False
        res_details = None
        res_id = None
        have_reserve = dict()
        #checking if the pool is already exists or not

        if self.params.get("config")[0].get("GlobalPoolDetails") != None:
            (pool_exists, pool_details, pool_id) = self.pool_exists()

            if self.log:
                log("pool Exists: " + str(pool_exists) + "\n Current Site: " + str(pool_details))

            if pool_exists:
                have["pool_id"] = pool_id
                have["pool_exists"] = pool_exists
                have["pool_details"] = pool_details
                log(str(pool_details))
            
            
            self.have = have
        
        if self.params.get("config")[0].get("ReservePoolDetails") != None:
            (res_exists, res_details, res_id) = self.res_exists()

            if self.log:
                log("Reservation Exists: " + str(res_exists) + "\n Reserved Pool: " + str(res_details))
            
            
            if res_exists:
                have_reserve["res_exists"] = res_exists
                have_reserve["res_id"] = res_id
                have_reserve["res_details"] = res_details
                if have_reserve.get("res_details").get("ipv6AddressSpace") == "False":
                    have_reserve.get("res_details").update({"ipv6AddressSpace": False})
                elif have_reserve.get("res_details").get("ipv6AddressSpace") == "True":
                    have_reserve.get("res_details").update({"ipv6AddressSpace": True})
            

            self.have_reserve = have_reserve

        
    def get_want(self):
        if self.params.get("config")[0].get("GlobalPoolDetails") != None:
            want = {}
            IpAddressSpace = self.params.get("config")[0].get("GlobalPoolDetails").get("settings").get("ippool")[0]
            dhcpServerIps = self.params.get("config")[0].get("GlobalPoolDetails").get("settings").get("ippool")[0]
            dnsServerIps = self.params.get("config")[0].get("GlobalPoolDetails").get("settings").get("ippool")[0]
            gateway = self.params.get("config")[0].get("GlobalPoolDetails").get("settings").get("ippool")[0]
            ipPoolCidr = self.params.get("config")[0].get("GlobalPoolDetails").get("settings").get("ippool")[0]
            ipPoolName = self.params.get("config")[0].get("GlobalPoolDetails").get("settings").get("ippool")[0]
            _type = self.params.get("config")[0].get("GlobalPoolDetails").get("settings").get("ippool")[0]

            want = dict(
                settings = dict(
                        ippool = [dict(
                                IpAddressSpace = IpAddressSpace.get("IpAddressSpace"),
                                dhcpServerIps = dhcpServerIps.get("dhcpServerIps"),
                                dnsServerIps = dnsServerIps.get("dnsServerIps"),
                                gateway = gateway.get("gateway"),
                                ipPoolCidr = ipPoolCidr.get("ipPoolCidr"),
                                ipPoolName = ipPoolName.get("ipPoolName"),
                                type = _type.get("type"),
                            )]
                    )
            )
            log(str(self.have))
            if not self.have.get("pool_exists"):
                if want.get("settings").get("ippool")[0].get("dhcpServerIps") == None:
                    want.get("settings").get("ippool")[0].update({"dhcpServerIps": []})
                if want.get("settings").get("ippool")[0].get("dnsServerIps") == None:
                    want.get("settings").get("ippool")[0].update({"dnsServerIps": []})
                if want.get("settings").get("ippool")[0].get("IpAddressSpace") == None:
                    want.get("settings").get("ippool")[0].update({"IpAddressSpace": ""})
                if want.get("settings").get("ippool")[0].get("gateway") == None:
                    want.get("settings").get("ippool")[0].update({"gateway": ""})
                if want.get("settings").get("ippool")[0].get("type") == None:
                    want.get("settings").get("ippool")[0].update({"type": "generic"})

                    
            else:
                if self.have.get("pool_details").get("settings").get("ippool")[0].get("IpAddressSpace") == "IPv4":
                    want.get("settings").get("ippool")[0].update({"IpAddressSpace": "IPv4"})
                    log("true")
                elif self.have.get("pool_details").get("settings").get("ippool")[0].get("IpAddressSpace") == "Ipv6":
                    want.get("settings").get("ippool")[0].update({"IpAddressSpace": "IPv6"})
                    log("false")
    ##            want.get("settings").get("ippool")[0].update({"IpAddressSpace": "IPv6"})
                want.get("settings").get("ippool")[0].update({"type": self.have.get("pool_details").get("settings").get("ippool")[0].get("ipPoolType")})
                want.get("settings").get("ippool")[0].update({"ipPoolCidr": self.have.get("pool_details").get("settings").get("ippool")[0].get("ipPoolCidr")})
                
                if want.get("settings").get("ippool")[0].get("dhcpServerIps") == None and self.have.get("pool_details").get("settings").get("ippool")[0].get("dhcpServerIps") != None:
                    want.get("settings").get("ippool")[0].update({"dhcpServerIps": self.have.get("pool_details").get("settings").get("ippool")[0].get("dhcpServerIps")})
                if want.get("settings").get("ippool")[0].get("dnsServerIps") == None and self.have.get("pool_details").get("settings").get("ippool")[0].get("dnsServerIps") != None:
                    want.get("settings").get("ippool")[0].update({"dnsServerIps": self.have.get("pool_details").get("settings").get("ippool")[0].get("dnsServerIps")})
                if want.get("settings").get("ippool")[0].get("gateway") == None and self.have.get("pool_details").get("settings").get("ippool")[0].get("gateway") != None:
                    want.get("settings").get("ippool")[0].update({"gateway": self.have.get("pool_details").get("settings").get("ippool")[0].get("gateway")})
                    
                                                                
            log(str(want))
            self.want = want

        if self.params.get("config")[0].get("ReservePoolDetails") != None:

            want_reserve = dict(
                name = self.params.get("config")[0].get("ReservePoolDetails").get("name"),
                type = self.params.get("config")[0].get("ReservePoolDetails").get("type"),
                ipv6AddressSpace = self.params.get("config")[0].get("ReservePoolDetails").get("ipv6AddressSpace"),
                ipv4GlobalPool = self.params.get("config")[0].get("ReservePoolDetails").get("ipv4GlobalPool"),
                ipv4Prefix = self.params.get("config")[0].get("ReservePoolDetails").get("ipv4Prefix"),
                ipv4PrefixLength = self.params.get("config")[0].get("ReservePoolDetails").get("ipv4PrefixLength"),
                ipv4GateWay = self.params.get("config")[0].get("ReservePoolDetails").get("ipv4GateWay"),
                ipv4DhcpServers = self.params.get("config")[0].get("ReservePoolDetails").get("ipv4DhcpServers"),
                ipv4DnsServers = self.params.get("config")[0].get("ReservePoolDetails").get("ipv4DnsServers"),
                ipv6GlobalPool = self.params.get("config")[0].get("ReservePoolDetails").get("ipv6GlobalPool"),
                ipv6Prefix = self.params.get("config")[0].get("ReservePoolDetails").get("ipv6Prefix"),
                ipv6PrefixLength = self.params.get("config")[0].get("ReservePoolDetails").get("ipv6PrefixLength"),
                ipv6GateWay = self.params.get("config")[0].get("ReservePoolDetails").get("ipv6GateWay"),
                ipv6DhcpServers = self.params.get("config")[0].get("ReservePoolDetails").get("ipv6DhcpServers"),
                ipv6DnsServers = self.params.get("config")[0].get("ReservePoolDetails").get("ipv6DnsServers"),
                ipv4TotalHost = self.params.get("config")[0].get("ReservePoolDetails").get("ipv4TotalHost"),
                ipv6TotalHost = self.params.get("config")[0].get("ReservePoolDetails").get("ipv6TotalHost")
            )

            log(str(self.have_reserve))
            if not self.have_reserve:
                if want_reserve.get("type") == None:
                    want_reserve.update({"type": generic})
                if want_reserve.get("ipv4GateWay") == None:
                    want_reserve.update({"ipv4GateWay": ""})
                if want_reserve.get("ipv4DhcpServers") == None:
                    want_reserve.update({"ipv4DhcpServers": []})
                if want_reserve.get("ipv4DnsServers") == None:
                    want_reserve.update({"ipv4DnsServers": []})
                if want_reserve.get("ipv6AddressSpace") == None:
                    want_reserve.update({"ipv6AddressSpace": False})  
                if want_reserve.get("slaacSupport") == None:
                    want_reserve.update({"slaacSupport": True}) 
                if want_reserve.get("ipv4TotalHost") == None:
                    del want_reserve['ipv4TotalHost']
                if want_reserve.get("ipv6Prefix") == None and want_reserve.get("ipv6AddressSpace") == True:
                    want_reserve.update({"ipv6Prefix": True})
                else:
                    del want_reserve['ipv6Prefix']
                if want_reserve.get("ipv6AddressSpace") == False:   
                    if want_reserve.get("ipv6GlobalPool") == None:
                        del want_reserve['ipv6GlobalPool']
                    if want_reserve.get("ipv6PrefixLength") == None:
                        del want_reserve['ipv6PrefixLength']
                    if want_reserve.get("ipv6GateWay") == None:
                        del want_reserve['ipv6GateWay']
                    if want_reserve.get("ipv6DhcpServers") == None:
                        del want_reserve['ipv6DhcpServers']
                    if want_reserve.get("ipv6DnsServers") == None:
                        del want_reserve['ipv6DnsServers']
                    if want_reserve.get("ipv6TotalHost") == None:
                        del want_reserve['ipv6TotalHost']

            else:
                del want_reserve['type']
                del want_reserve['ipv4GlobalPool']
                del want_reserve['ipv4Prefix']
                del want_reserve['ipv4PrefixLength']
                del want_reserve['ipv4TotalHost']
                # want_reserve.update({"ipv6AddressSpace": "False"})

            self.want_reserve = want_reserve


    def get_execution_details(self, execid):
        response = None
        response = self.dnac._exec(
            family="task",
            function='get_business_api_execution_details',
            params={"execution_id": execid}
        )

        if self.log:
            log(str(response))

        if response and isinstance(response, dict):
            return response        


    def get_diff_merge(self):
        if self.params.get("config")[0].get("GlobalPoolDetails") != None:

            if not self.params.get("config")[0].get("GlobalPoolDetails").get("settings").get("ippool")[0].get("ipPoolName"):
                msg = "Mandatory Parameter ipPoolName required\n"
                self.module.fail_json(msg=msg)
            pool_updated = False
            pool_created = False

            if self.have.get("pool_exists"):
                log("entered")
                obj_params = [
                    ("settings", "settings"),
                ]
                if self.requires_update(self.have.get("pool_details"), self.want, obj_params):
                    log("Pool update requires")
                    #Pool Exists
                    pool_params = copy.deepcopy(self.want)
                    pool_params.get("settings").get("ippool")[0].update({"id": self.have.get("pool_id")})
                    log(str(self.want))
                    log(str(pool_params))
                    del pool_params["settings"]["ippool"][0]["IpAddressSpace"]
                    del pool_params["settings"]["ippool"][0]["ipPoolCidr"]
                    del pool_params["settings"]["ippool"][0]["type"]

                    if pool_params.get("settings").get("ippool")[0].get("dhcpServerIps") == None:
                        pool_params.get("settings").get("ippool")[0].update({"dhcpServerIps" : self.have.get("pool_details").get("settings").get("ippool")[0].get("dhcpServerIps")})
                    if pool_params.get("settings").get("ippool")[0].get("dnsServerIps") == None:
                        pool_params.get("settings").get("ippool")[0].update({"dnsServerIps" : self.have.get("pool_details").get("settings").get("ippool")[0].get("dnsServerIps")})
                    if pool_params.get("settings").get("ippool")[0].get("gateway") == None:
                        pool_params.get("settings").get("ippool")[0].update({"gateway" : self.have.get("pool_details").get("settings").get("ippool")[0].get("gateway")})
                        
                    log(str(pool_params))
                    log(str(self.have))
                    response = self.dnac._exec(
                        family = "network_settings",
                        function = "update_global_pool",
                        params = pool_params,
                        op_modifies = True,
                    )
                    
                    pool_updated = True
                    log(str(pool_updated))

                else:
                    log("Pool doesn't requires an update")
                    self.result["response"] = self.have.get("settings")
                    self.result["msg"] = "Pool doesn't requires an update"
                    self.module.exit_json(**self.result)

            else:
                #creating New Pool
                pool_params = self.want
                log(str(pool_params))
                response = self.dnac._exec(
                    family="network_settings",
                    function="create_global_pool",
                    params = pool_params,
                    op_modifies = True,
                )
                log("PoolCreated") 
                log(str(response))
                pool_created = True
    
            if pool_created or pool_updated:
                if response and isinstance(response, dict):
                    executionid = response.get("executionId")

                    while True:
                        execution_details = self.get_execution_details(executionid)
                        if execution_details.get("status") == "SUCCESS":
                            self.result['changed'] = True
                            self.result['response'] = execution_details
                            break

                        elif execution_details.get("bapiError"):

                            self.module.fail_json(msg=execution_details.get("bapiError"),
                                                response=execution_details)
                            break

                    if pool_updated:
                        log("Pool Updated Successfully")
                        self.result['msg'] = "Pool Updated Successfully"
                        self.result['response'].update({"Id": self.have.get("pool_details").get("id")})
                        
                    elif pool_created:
                        log("Pool Created Successfully")
                        (pool_exists, pool_details, pool_id) = self.pool_exists()
                        self.result['response'].update({"Id": pool_id})
                        self.result['msg'] = "Pool Created Successfully"
                    else:
                        log("Pool doesn't need a update")
                        self.result['msg'] = "Pool doesn't requires an update"
                        self.result['response'].update({"Id": self.have.get("pool_details").get("id")})

        if self.params.get("config")[0].get("ReservePoolDetails") != None:

            res_updated = False
            res_created = False
            log(str(self.have_reserve.get("res_details")))
            log(str(self.want_reserve))
            if self.have_reserve:
                log("entered")
                obj_params = [
                    ("name", "name"),
                    ("type", "type"),
                    ("ipv6AddressSpace", "ipv6AddressSpace"),
                    ("ipv4GlobalPool", "ipv4GlobalPool"),
                    ("ipv4Prefix", "ipv4Prefix"),
                    ("ipv4PrefixLength", "ipv4PrefixLength"),
                    ("ipv4GateWay", "ipv4GateWay"),
                    ("ipv4DhcpServers", "ipv4DhcpServers"),
                    ("ipv4DnsServers", "ipv4DnsServers"),
                    ("ipv6GateWay", "ipv6GateWay"),
                    ("ipv6DhcpServers", "ipv6DhcpServers"),
                    ("ipv6DnsServers", "ipv6DnsServers"),
                    ("ipv4TotalHost", "ipv4TotalHost"),
                    ("slaacSupport", "slaacSupport")
                ]

                if self.requires_update(self.have_reserve.get("res_details"), self.want_reserve, obj_params):
                    log("Pool update requires")
                    #Pool Exists
                    log(str(self.have_reserve))
                    log(str(self.want_reserve))

                    # if not self.site_id:
                    #     self.module.fail_json(msg="Mandatory parameter siteName not present or invalid", response=[])
                    res_params = copy.deepcopy(self.want_reserve)
                    res_params.update({"site_id": self.site_id})
                    res_params.update({"id": self.have_reserve.get("res_id")})
                    response = self.dnac._exec(
                        family="network_settings",
                        function="update_reserve_ip_subpool",
                        params=res_params,
                    )

                    log("Reservation Updated") 
                    log(str(response))
                    res_updated = True
                
                else:
                    log("Reserved ip subpool doesn't requires an update")
                    self.result["response"] = self.have.get("ReservePoolDetails")
                    self.result["msg"] = "Reserved ip subpool doesn't requires an update"
                    self.module.exit_json(**self.result)

            else:
                #creating New Pool
                res_params = self.want_reserve
                log(str(res_params))
                if not self.want_reserve.get("name") or not self.want_reserve.get("ipv4GlobalPool") or not self.want_reserve.get("ipv4PrefixLength") or not self.site_id:
                    self.module.fail_json(msg="missing parameter name or ipv4GlobalPool or ipv4PrefixLength or siteName", response=[])

                res_params.update({"site_id": self.site_id})
                log(str(res_params))
                response = self.dnac._exec(
                    family="network_settings",
                    function="reserve_ip_subpool",
                    params=res_params,
                )
                log("Reservation Created") 
                log(str(response))
                res_created = True

            if res_created or res_updated:
                if response and isinstance(response, dict):
                    executionid = response.get("executionId")

                    while True:
                        execution_details = self.get_execution_details(executionid)
                        if execution_details.get("status") == "SUCCESS":
                            self.result['changed'] = True
                            self.result['response'] = execution_details
                            break

                        elif execution_details.get("bapiError"):

                            self.module.fail_json(msg=execution_details.get("bapiError"),
                                                response=execution_details)
                            break

                    if res_updated:
                        log("Reserved Ip Subpool Updated Successfully")
                        self.result['msg'] = "Reserved Ip Subpool Updated Successfully"
                        self.result['response'].update({"Reservation details": self.have.get("res_details")})
                        
                    elif res_created:
                        log("Ip Subpool Reservation Created Successfully")
                        (res_exists, res_details, res_id) = self.res_exists()
                        self.result['response'].update({"Reservation details": self.have.get("res_details")})
                        self.result['msg'] = "Ip Subpool Reservation Created Successfully"
                    else:
                        log("Ip Subpool Reservation doesn't need a update")
                        self.result['msg'] = "Ip Subpool Reservation doesn't requires an update"
                        self.result['response'].update({"Reservation details": self.have.get("res_details")})


    def get_id_by_name(self, name):
        id = None
        try:
            response = self.dnac._exec(
                family="network_settings",
                function="get_reserve_ip_subpool",
                params={"siteId":self.site_id},
            )

            log(str(response))

            if isinstance(response, dict):
                if "response" in response:
                    response = response.get("response")
            log(str(response))


            current_details = get_dict_result(response, "groupName", name)         
            if current_details:        
                id = current_details.get("id")
        
        except:
            result = None

        return id


    def get_diff_delete(self):
        
        if self.params.get("config")[0].get("ReservePoolDetails") != None:
            res_exists = self.have_reserve.get("res_exists")
            log(str(res_exists))
            id = None
            if self.want_reserve.get("name"):
                log(str(self.want_reserve.get("name")))
                id = self.get_id_by_name(self.want_reserve.get("name"))
            log(str(id))
            if res_exists:
                if not id:
                    self.module.fail_json(msg="missing or incorrect parameter reserved pool name", response=[])
                log(str(self.have_reserve.get("res_id")))
                response = self.dnac._exec(
                    family="network_settings",
                    function="release_reserve_ip_subpool",
                    params={"id": id},
                )

                if response and isinstance(response, dict):
                    executionid = response.get("executionId")
                    while True:
                        execution_details = self.get_execution_details(executionid)
                        if execution_details.get("status") == "SUCCESS":
                            self.result['changed'] = True
                            self.result['response'] = execution_details
                            log(str(response))
                            self.result['msg'] = "Ip subpool reservation released successfully"
                            break

                        elif execution_details.get("bapiError"):
                            self.module.fail_json(msg=execution_details.get("bapiError"),
                                                response=execution_details)
                            break

            else:
                self.module.fail_json(msg="Reserved Ip Subpool Not Found", response=[])

        if self.params.get("config")[0].get("GlobalPoolDetails") != None: 
            pool_exists = self.have.get("pool_exists")

            if pool_exists:
                response = self.dnac._exec(
                    family="network_settings",
                    function="delete_global_ip_pool",
                    params={"id": self.have.get("pool_id")},
                )

                if response and isinstance(response, dict):
                    executionid = response.get("executionId")
                    while True:
                        execution_details = self.get_execution_details(executionid)
                        if execution_details.get("status") == "SUCCESS":
                            self.result['changed'] = True
                            self.result['response'] = execution_details
                            log(str(response))
                            self.result['response'].update({"Id": self.have.get("pool_details").get("id")})
                            self.result['msg'] = "Pool deleted successfully"
                            break

                        elif execution_details.get("bapiError"):
                            self.module.fail_json(msg=execution_details.get("bapiError"),
                                                response=execution_details)
                            break

            else:
                self.module.fail_json(msg="Pool Not Found", response=[])
        
            

def main():
    """main entry point for module execution"""

    element_spec = dict(
        dnac_host=dict(required=True, type="str"),
        dnac_port=dict(type="str", default="443"),
        dnac_username=dict(type="str", default="admin", aliases=["user"]),
        dnac_password=dict(type="str", no_log=True),
        dnac_verify=dict(type="bool", default="True"),
        dnac_version=dict(type="str", default="2.2.3.3"),
        dnac_debug=dict(type="bool", default=False),
        dnac_log=dict(type="bool", default=False),
        validate_response_schema=dict(type="bool", default=True),
        config=dict(required=True, type="list", elements="dict"),
        state=dict(default="merged", choices=["merged", "deleted"]),
    )

    module = AnsibleModule(argument_spec=element_spec, supports_check_mode=False)
    
    dnac_network = DnacNetwork(module)
    
    state = dnac_network.get_state()
    dnac_network.validate_input()
    
    dnac_network.get_have()
    dnac_network.get_want()
    
    if state == "merged":
        dnac_network.get_diff_merge()
        
    elif state == "deleted":
        dnac_network.get_diff_delete()
    log(str(dnac_network.result))
    
    module.exit_json(**dnac_network.result)
    

if __name__ == "__main__":
    main()