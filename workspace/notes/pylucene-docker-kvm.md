
INSTALLAZIONE SU UBUNTU



KVM
https://serverfault.com/questions/1043441/how-to-run-kvm-nested-in-wsl2-or-vmware (PRIMI PASSI DA EFFETTUARE)
https://docs.docker.com/desktop/setup/install/linux/#kvm-virtualization-support (MODPROBE)

On WSL2 (Windows 11), nested virtualization is supported but not enabled by default. To enable it, you must:

    Add yourself to the kvm group
    Change the default group of /dev/kvm
    Enable nested virtualization in /etc/wsl.conf
    Restart WSL

1. Adding yourself to the kvm group:

This one is easy:

sudo usermod -a -G kvm ${USER}

2. Change the default group of /dev/kvm

This is also easy, but to make it stick across reboots and upgrades, add this section to your /etc/wsl.conf file:

[boot]
command = /bin/bash -c 'chown -v root:kvm /dev/kvm && chmod 660 /dev/kvm'

3. Enable nested virtualization

You don’t need to recompile your WSL distribution to enable nested virtualization, just add this section to your /etc/wsl.conf:

[wsl2]
nestedVirtualization=true

4. Restart WSL

You can either restart Windows, or close all of your WSL terminal windows and issue this command in Powershell, CMD, or Windows Run menu (Windows+R)

wsl.exe --shutdown

The next time you open a terminal, WSL will start with the new options and nested virtualization will work. 






DOCKER
(https://docs.docker.com/desktop/setup/install/linux/)
[Install Using the Repository](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository) (Questo è quello giusto da seguire)




