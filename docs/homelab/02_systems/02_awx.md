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

### K3s setup

Install k3s using the quickstart script.  
This is the most basic way to get k3s up and running.  

```bash title="k3s installation command"
sudo dnf install -y kernel-modules-extra (1)!
curl -sfL https://get.k3s.io | sh -
watch sudo kubectl get nodes #(2)!
```
1.  The `kernel-modules-extra` package is required for k3s to function properly.  
    Ref. [k3s requirements](https://docs.k3s.io/installation/requirements?os=rhel)
2.  The `watch` command can be interrupted with `Ctrl + C` once the node is ready.  

Next, configure the local firewall to allow the network used by k3s to communicate properly.  
See [k3s requirements](https://docs.k3s.io/installation/requirements?os=rhel).
```bash title="Commands to configure firewall for k3s"
firewall-cmd --permanent --add-port=6443/tcp #apiserver
firewall-cmd --permanent --zone=trusted --add-source=10.42.0.0/16 #pods
firewall-cmd --permanent --zone=trusted --add-source=10.43.0.0/16 #services
firewall-cmd --reload
```
!!! Note
    If you skip this step, the deployment of the awx-web deployment will fail and get stuck in `crashloopbackoff` state.

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
```yaml title="kustomization.yaml for awx-operator deployment"
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
```yaml title="awx-demo.yml for AWX instance deployment"
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

```yaml title="Example hosts file entry for AWX access"
127.0.0.1   awx.internal.packetflow.be #(1)!
```

1.  This needs to be the same hostname as specified in the `awx-demo.yml` file.  
   
Finally, deploy the AWX instance by uncommenting the `awx-demo.yml` line in the `kustomization.yaml` file and running the same command as before:
```yaml title="kustomization.yaml with awx-demo.yml uncommented"
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
