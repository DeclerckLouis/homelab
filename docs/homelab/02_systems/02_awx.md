# AWX x Netbox  
## Intro
In a previous project, I used netbox as a source of truth to automate VM deployments in Proxmox using ansible and terraform.  
The goal of that project was to prove proficiency in ansible, terraform, FreeIPA, etc.   
While fun and a great learning experience, it was very fragile and not scalable.  
  
In this project, I want to set up netbox as a scalable source of truth, integrating it with AWX.  
The goal is to see how AWX can be used to automate tasks based on data from netbox, and to explore the capabilities of AWX in a more practical setting.

For this project, I used a free Netbox Cloud instance provided by [netbox.dev

## Local env installation and Configuration
Since AWX doesn't run on ARM, I ditched the raspberry pi's and sacrificed my HP Omen laptop to run RHEL. (developer license)  

### k3s Setup
K3s installed using the quickstart script.  
This is the most basic way to get k3s up and running.  

```bash title="k3s installation command"
sudo dnf install -y kernel-modules-extra (1)!
curl -sfL https://get.k3s.io | sh -
watch sudo kubectl get nodes #(2)!
```
1.  The `kernel-modules-extra` package is required for k3s to function properly.  
    Ref. [k3s requirements](https://docs.k3s.io/installation/requirements?os=rhel)
2.  Wait until the node is in `Ready` state to proceed.  
    The `watch` command can be interrupted with `Ctrl + C` once the node is ready.

Next, the local firewall has to be configured to allow the network used by k3s to communicate properly.  
Ref. [k3s requirements](https://docs.k3s.io/installation/requirements?os=rhel)
```bash title="Commands to configure firewall for k3s"
firewall-cmd --permanent --add-port=6443/tcp #apiserver
firewall-cmd --permanent --zone=trusted --add-source=10.42.0.0/16 #pods
firewall-cmd --permanent --zone=trusted --add-source=10.43.0.0/16 #services
firewall-cmd --reload
```
!!! Note
    If you forget this step, deployment of the awx-web deployment will never succeed and get stuck in `crashloopbackoff` state.

### AWX Setup 
Installation was done following the [AWX-operator](https://docs.ansible.com/projects/awx-operator/en/latest/installation/basic-install.html) docs.  

```bash title="Commands to clone awx-operator repo"
git clone https://github.com/ansible/awx-operator.git
cd awx-operator
git tag
git checkout tags/2.19.1 #(1)!
```

1.    2.19.1 is the latest release as of writing this page.  

Next, the operator is deployed using a kustomization.yaml file with the following contents:
```yaml title="kustomization.yaml for awx-operator deployment"
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  # - awx-demo.yml # This is currently commented out to allow awx-operator to be deployed first. It will be uncommented later to deploy the AWX instance itself.
  - github.com/ansible/awx-operator/config/default?ref=2.19.1

# Set the image tags to match the git version from above
images:
  - name: quay.io/ansible/awx-operator
    newTag: 2.19.1

# Specify a custom namespace in which to install AWX
namespace: awx
```

1.  The `awx-demo.yml` line   

We install the manifests by running
```bash title="Command to deploy awx-operator"
kubectl apply -k .
```