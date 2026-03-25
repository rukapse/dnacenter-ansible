# SDA Host Port Onboarding — Device Refresh Migration

## Purpose

Automates replication of SDA host port onboarding configurations from a source device (e.g., Catalyst 9000 being decommissioned) to a destination device (e.g., Catalyst 9350 replacement) within the same fabric site on Cisco Catalyst Center.

This POC package provides a single, self-contained playbook that performs the full extract → transform → apply workflow for device refresh/migration scenarios.

## Prerequisites

- **Ansible** 2.14+
- **cisco.dnac** collection installed (`ansible-galaxy collection install cisco.dnac`)
- **dnacentersdk** >= 2.3.7.9 (`pip install dnacentersdk`)
- **PyYAML** >= 5.1
- **Python** >= 3.9
- Network access to Cisco Catalyst Center
- Both source and destination devices must be **provisioned** and added to the **fabric site** in Catalyst Center

## Quick Start

1. **Edit** `vars_device_refresh.yml` with your environment details (Catalyst Center credentials, fabric site, source/destination device IPs).
2. **Run** the playbook:
   ```bash
   ansible-playbook -i inventory.yml playbook_device_refresh.yml
   ```
3. **Verify** in Catalyst Center UI that the destination device has the replicated host port onboarding configuration.

## Running Individual Phases

You can run specific phases using Ansible tags:

```bash
# Extract config from source device only
ansible-playbook -i inventory.yml playbook_device_refresh.yml --tags extract

# Transform + Apply together (REQUIRED — apply depends on transform)
ansible-playbook -i inventory.yml playbook_device_refresh.yml --tags transform,apply
```

> **⚠️ Important:** The `transform` and `apply` phases must be run together (`--tags transform,apply`).
> The apply phase depends on the `destination_config` variable which is set during transform.
> Running `--tags apply` alone will fail with an undefined variable error.
> The `extract` phase can be run independently since it writes to a file.

## What the Playbook Does

The playbook executes three phases:

### Phase 1: Extract (`--tags extract`)
Extracts the current SDA host port onboarding configuration from the source device using the `cisco.dnac.sda_host_port_onboarding_playbook_config_generator` module. The extracted config is saved to a YAML file (default: `extracted_source_config.yml`).

### Phase 2: Transform (`--tags transform`)
Loads the extracted YAML file, filters entries for the source device, and swaps the source device IP address with the destination device IP address. This retargets the configuration for the replacement device.

### Phase 3: Apply (`--tags apply`)
Pushes the transformed configuration to the destination device using the `cisco.dnac.sda_host_port_onboarding_workflow_manager` module with `state: merged`. Each config entry (port assignments, port channels, wireless SSIDs) is applied individually.

### Cleanup: Delete Port Assignments (`--tags transform,cleanup`)

Deletes the migrated port assignments from the destination device. **This is a destructive operation** and is intentionally excluded from the main flow — it only runs when explicitly called with the `cleanup` tag.

```bash
# Delete migrated port assignments from destination device
ansible-playbook -i inventory.yml playbook_device_refresh.yml --tags transform,cleanup
```

> **⚠️ Warning:** This will delete the port assignments on the destination device. This cannot be undone.
> The `cleanup` tag uses Ansible's `never` tag, so it will never run unless you explicitly include it.
> It requires `transform` to run alongside it (`--tags transform,cleanup`) to build the `destination_config`.

## APIs Called Internally

The following Catalyst Center APIs are called during execution:

| # | SDK Method | API Endpoint | Purpose |
|---|-----------|-------------|---------|
| 1 | `sda.get_fabric_sites` | `GET /dna/intent/api/v1/sda/fabricSites` | Resolves fabric site names to IDs |
| 2 | `sda.get_port_assignments` | `GET /dna/intent/api/v1/sda/portAssignments` | Gets port assignment configs per fabric site |
| 3 | `sda.get_port_channels` | `GET /dna/intent/api/v1/sda/portChannels` | Gets port channel configs per fabric site |
| 4 | `fabric_wireless.retrieve_the_vlans_and_ssids_mapped_to_the_vlan_within_a_fabric_site` | `GET /dna/intent/api/v1/sda/fabrics/{fabricId}/vlanToSsids` | Gets wireless SSID-to-VLAN mappings |
| 5 | `devices.get_device_by_id` | `GET /dna/intent/api/v1/network-device/{id}` | Resolves device UUIDs to management IPs |

## Troubleshooting

- **Check `dnac.log`** for detailed debug output (generated in the playbook directory when `dnac_log: true`).
- **Verify both devices are provisioned** and present in the fabric site within Catalyst Center.
- **Verify `fabric_site_hierarchy`** matches exactly (case-sensitive) the hierarchy shown in Catalyst Center.
- **Increase `catalyst_center_api_task_timeout`** in `vars_device_refresh.yml` for large configurations (default: 1200 seconds).
- **Empty destination config error**: If Phase 2 fails with "no config entries found," confirm the `source_device_ip` matches a device in the extracted config file.
- **Connectivity issues**: Ensure the Ansible control node can reach Catalyst Center on the configured port (default: 443).

## Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `catalyst_center_host` | Catalyst Center IP or hostname | `10.195.120.197` |
| `catalyst_center_username` | Login username | `admin` |
| `catalyst_center_password` | Login password | `C1sc0dna` |
| `catalyst_center_verify` | Verify SSL certificate | `false` |
| `catalyst_center_port` | HTTPS port | `443` |
| `catalyst_center_version` | API version | `2.3.7.9` |
| `catalyst_center_debug` | Enable SDK debug logging | `false` |
| `catalyst_center_api_task_timeout` | API task timeout in seconds | `1200` |
| `fabric_site_hierarchy` | Full fabric site path (case-sensitive) | `Global/USA/SAN-FRANCISCO/SF_BLD2/FLOOR2` |
| `source_device_ip` | Management IP of device being replaced | `10.195.120.219` |
| `destination_device_ip` | Management IP of replacement device | `10.195.120.173` |
| `components_to_migrate` | List of components to migrate | `[port_assignments, port_channels, wireless_ssids]` |
| `extracted_config_file` | Path for intermediate extracted config | `{{ playbook_dir }}/extracted_source_config.yml` |
