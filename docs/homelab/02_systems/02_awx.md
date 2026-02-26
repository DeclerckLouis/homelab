# AWX 
## Installation and Configuration
In this homelab, I installed AWX on a HP laptop running RHEL. (developer license)  
Installation was done following the [AWX-operator](https://docs.ansible.com/projects/awx-operator/en/latest/installation/basic-install.html) docs.  
---  

### Cloning the awx-operator repo  
```bash
git clone https://github.com/ansible/awx-operator.git
cd awx-operator
git tag
git checkout tags/2.9.0 #(1)!
```

1.  **to be updated to 2.19**

!!! Note "Fun Fact"
    While writing this, I found out that i have always used 2.9 thinking this was the latest version since it's the latest one to show up when running `git tag`. i'll delete the entire deployment and try installing 2.19 to see what changes.  

### Deploying AWX Operator
