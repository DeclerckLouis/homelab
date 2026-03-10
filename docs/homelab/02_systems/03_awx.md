# AWX x Netbox

## Intro

In a previous project, Netbox was used as a source of truth to automate VM deployments in Proxmox using Ansible and Terraform.  
The goal of that project was to prove proficiency in Ansible, Terraform, FreeIPA, and similar tools.   
While fun and a great learning experience, it was very fragile and not scalable.  
  
In this project, Netbox serves as a scalable source of truth, integrated with AWX.  
The goal is to see how AWX can be used to automate tasks based on data from Netbox, and to explore the capabilities of AWX in a more practical setting.

For this project, a free Netbox Cloud instance was used, provided by [netbox.dev](https://netbox.dev).

## Local environment installation and configuration

AWX does not run on ARM platforms, so this setup uses RHEL on a dedicated machine.
For the installation of k3s, see the [k3s installation page](./02_k3s.md).  

### AWX setup

#### Clone repository

Follow the [AWX-operator](https://docs.ansible.com/projects/awx-operator/en/latest/installation/basic-install.html) documentation.  

```bash title="Commands to clone awx-operator repo"
git clone https://github.com/ansible/awx-operator.git
cd awx-operator
git tag
git checkout tags/2.19.1 #(1)!
```

1.  2.19.1 is the latest release as of writing this page.

#### Deploy AWX operator

Deploy the operator using a kustomization.yaml file with the following contents:
```yaml title="kustomization.yaml"
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  # Uncomment after awx-operator is deployed to deploy the AWX instance
  # - awx-demo.yml
  - github.com/ansible/awx-operator/config/default?ref=2.19.1

# Set the image tags to match the git version from above
images:
  - name: quay.io/ansible/awx-operator
    newTag: 2.19.1

# Specify a custom namespace in which to install AWX
namespace: awx
```

1.  The `awx-demo.yml` line   

Deploy the manifests by running:
```bash title="Command to deploy awx-operator"
kubectl apply -k .
```
```console title="Output"
namespace/awx created
customresourcedefinition.apiextensions.k8s.io/awxbackups.awx.ansible.com created
customresourcedefinition.apiextensions.k8s.io/awxrestores.awx.ansible.com created
customresourcedefinition.apiextensions.k8s.io/awxs.awx.ansible.com created
serviceaccount/awx-operator-controller-manager created
role.rbac.authorization.k8s.io/awx-operator-awx-manager-role created
role.rbac.authorization.k8s.io/awx-operator-leader-election-role created
clusterrole.rbac.authorization.k8s.io/awx-operator-metrics-reader created
clusterrole.rbac.authorization.k8s.io/awx-operator-proxy-role created
rolebinding.rbac.authorization.k8s.io/awx-operator-awx-manager-rolebinding created
rolebinding.rbac.authorization.k8s.io/awx-operator-leader-election-rolebinding created
clusterrolebinding.rbac.authorization.k8s.io/awx-operator-proxy-rolebinding created
configmap/awx-operator-awx-manager-config created
service/awx-operator-controller-manager-metrics-service created
deployment.apps/awx-operator-controller-manager created
```  

Wait a moment and verify that all pods are in the `Running` state before proceeding.  
This can be verified by running: 
```bash title="Command to check awx-operator deployment status"
kubectl get pods -n awx
```
```console title="Output"
NAME                                               READY   STATUS      RESTARTS      AGE
awx-operator-controller-manager-6686bb5899-glmf4   2/2     Running     9 (27h ago)   5d15h
```

#### Deploy AWX instance

Modify the `awx-demo.yml` file in the repository as follows:
```yaml title="awx-demo.yml"
---
apiVersion: awx.ansible.com/v1beta1
kind: AWX
metadata:
  name: awx-declercklouis #(1)!
spec:
  service_type: ClusterIP #(2)!
  ingress_type: ingress
  hostname: awx.internal.packetflow.be
```

1.  Change this to your preferred name. Keep it simple for easy debugging.
2.  Use service type `ClusterIP` with an ingress controller instead of the default `NodePort` to avoid dealing with changing port numbers.  

Set up a DNS record for `awx.internal.packetflow.be` pointing to the machine IP, or add an entry in the local hosts file pointing to localhost.

```yaml title="/etc/hosts"
127.0.0.1   awx.internal.packetflow.be #(1)!
```

1.  This needs to be the same hostname as specified in the `awx-demo.yml` file.  
   
Finally, deploy the AWX instance by uncommenting the `awx-demo.yml` line in the `kustomization.yaml` file and running the same command as before:
```yaml title="kustomization.yaml"
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  # Find the latest tag at https://github.com/ansible/awx-operator/releases
  - github.com/ansible/awx-operator/config/default?ref=2.19.1
  - awx-demo.yml

# Set the image tags to match the git version from above
images:
  - name: quay.io/ansible/awx-operator
    newTag: 2.19.1

# Specify a custom namespace in which to install AWX
namespace: awx
```
```bash title="Command to deploy AWX instance"
kubectl apply -k .
```

The AWX instance deploys, typically taking around 5-10 minutes.  
Follow the progress by checking the logs of the deployment:
```bash title="Command to check AWX instance deployment status"
kubectl logs -f deployments/awx-operator-controller-manager -c awx-manager -n awx
```

```console title="Output"
TASK [installer : Start installation if auto_upgrade is false and deployment is missing] ***
task path: /opt/ansible/roles/installer/tasks/main.yml:31

-------------------------------------------------------------------------------
{"level":"info","ts":"2026-03-03T06:50:49Z","logger":"runner","msg":"Ansible-runner exited successfully","job":"9081341982685646779","name":"awx-declercklouis","namespace":"awx"}

----- Ansible Task Status Event StdOut (awx.ansible.com/v1beta1, Kind=AWX, awx-declercklouis/awx) -----


PLAY RECAP *********************************************************************
localhost                  : ok=89   changed=0    unreachable=0    failed=0    skipped=84   rescued=0    ignored=1  
```

### NetBox setup

### Installation

You can install NetBox locally or use a free instance from [NetBoxLabs](https://netboxlabs.com/).  
For the local install, follow the [NetBox installation guide](https://netboxlabs.com/docs/netbox/installation/).  

??? note "NetBoxLabs"
    NetBoxLabs, the company behind the NetBox Cloud offering, provides a free tier.  
    This tier includes the following, and is also used for this project:
    - Private instance
    - 100 devices
    - 500 IP addresses
    - 10k API requests per month
    - Automatic upgrades and backups
    - 2 Operational branches

#### Structure

Not all features are required for this project, but they help supplement your documentation.  

!!! info "Demo data"
    When using NetBox Cloud, start with demo data enabled and then delete the unnecessary data.
    This helps you understand the structure of NetBox and how to use it.

##### Organization

Regions, Sites, Locations, and Racks model the physical location of devices.  
Use these to filter devices based on location in your Ansible inventory.  

```bash title="Localization used in the PacketFlow NetBox instance"
Region: Europe
  Region: Belgium
    Site: Snellegem office
      Location: Office
      Location: Server Room
  Region: France
....
```

##### Devices preparation

This is the most important part of the setup.  
Create manufacturers, device types, and platforms before adding devices.  
**Manufacturers**:

Create a manufacturer for each brand of device you have (for example, Fortinet, MikroTik).  
If using the device type library, ensure the names match the manufacturer names used in the library.

**Device types**:

Create a device type for each device model you have.

!!! tip "Device type library"
    The NetBox community maintains a [device type library](https://github.com/netbox-community/devicetype-library) with pre-made device types.   
    Import them into your instance manually or using the [device type library import](https://github.com/netbox-community/Device-Type-Library-Import) tool.  
    This saves time but uses many API calls. Be mindful of API limits if using NetBox Cloud.  

**Platforms**:
When paired with config contexts, platforms give Ansible the necessary information to connect to devices.  
The platform name should match the `ansible_network_os` variable you use in the Ansible inventory.  
Link them to the correct manufacturer.  

```bash title="Platforms for the PacketFlow NetBox instance"
Platform: fortinet.fortios.fortios #(1)! 
  Manufacturer: Fortinet
Platform: mikrotik.routeros.routeros
    Manufacturer: MikroTik
```

1.  The value must be the actual plugin name, in this case `fortinet.fortios.fortios`, not just `fortinet.fortios`.  
    This is required for the ansible inventory to work properly. 

??? note
    You can optionally link the platform to a device type, though this is not required.

##### Devices

Create the devices themselves.

| Name         | Status | Tenant | Site      | Location    | Rack | Role                 | Manufacturer | Type                   | IP Address     |
| ------------ | ------ | ------ | --------- | ----------- | ---- | -------------------- | ------------ | ---------------------- | -------------- |
| als01        | Active | —      | Snellegem | Server Room | —    | Access Layer Switch  | Ubiquiti     | EdgeSwitch 8 150W      | 10.10.99.13/24 |
| ap01         | Active | —      | Snellegem | Server Room | —    | Wireless AP          | MikroTik     | hAP ac lite TC         | 10.10.99.10/24 |
| Blueberrypi  | Active | —      | Snellegem | Server Room | —    | Generic Linux Server | Raspberry Pi | Raspberry Pi 5         | 10.10.30.5/24  |
| fw01         | Active | —      | Snellegem | Server Room | —    | Firewall             | Fortinet     | FortiGate 40F          | 10.10.99.1/24  |
| Strawberrypi | Failed | —      | Snellegem | Server Room | —    | Generic Linux Server | Raspberry Pi | Raspberry Pi 4 Model B | 10.10.30.6/24  |

!!! note "IP addressing"
    Configure IP addressing later in this project.

## Netbox as Ansible inventory 
### Example inventory file

Test the NetBox inventory by creating a simple playbook with an inventory.yml file that uses the `netbox` plugin to pull devices from NetBox.
```yaml title="Example inventory.yml file"
plugin: netbox.netbox.nb_inventory
api_endpoint: "https://svur9623.cloud.netboxapp.com" #(1)!
token: "Your NetBox API token here" #(2)!
validate_certs: false # (3)! 
config_context: true
flatten_config_context: true #(4)! 
interfaces: true
group_names_raw: true
group_by:
  - device_roles
  - platforms
  - device_types
  - tenants
  - sites
  - racks
  - tags
query_filters: [] # (5)! 
device_query_filters:
  - has_primary_ip: "true" #(6)!
  - status: "active" #(7)!
flatten_custom_fields: true
compose:
  ansible_network_os: platform.name # Very important!
```

1.  The `api_endpoint` is the URL of your NetBox instance.
2.  The `token` is the API token that you can generate in the NetBox UI under the user profile.  
    Use this token to authenticate with the NetBox API and pull the inventory data.
3.  Set to false if using self-signed certificates
4.  Needed to access config context values directly in hostvars (ansible_connection)
5.  Optional: Add filters to limit the devices included in the inventory
6.  Optional: Only include devices with a primary IP address
7.  Optional: Only include active devices

