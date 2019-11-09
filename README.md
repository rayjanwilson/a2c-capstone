# a2c-capstone

## Engagement Manager Info
- [Internal weekly status report format](https://confluence.aws-proserve.org/confluence/display/EDF/How+to+produce+a+weekly+status+-+Internal) provided by Dave Sumner
    - not everyone will have access to it, but that's ok
- This [wiki link](https://w.amazon.com/index.php/Technical%20Program%20Manager/Reporting%20Status) describes the status reporting

## Git Branching Strategy
- We will use the [Gitflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) branching strategy
- This strategy uses two branches to record the history of the project: **master** and **dev**
- Each new feature should have its own branch, working off of dev (instead of branching off of master).
- Naming convention for feature branches: issueNumber-issueDescription. Do not use spaces. For example: *32-update-readme-git-branching-strategy*
- When a feature is developed, it should be merged into dev through a pull request.
- Dev will occasionally be merged into master through a pull request.

## Project Components and ownership
- Greengrass infrastructure (Ray)
- Greengrass lambdas (all)
- Data ingestion through IoT stuff (Tim)
- Data processing with IoT Analytics + storage (Phanee)
- Web App - react app setup (Ray)
- Web App - dashboards, cleanup UI, cognito (Sumeet)

## Link to Proserve Templates
- [Weekly Status Reports](https://confluence.aws-proserve.org/confluence/pages/viewpage.action?spaceKey=EDF&title=How+to+produce+a+weekly+status+-+Internal)
- [Migration Readiness (MRA)](https://confluence.aws-proserve.org/confluence/display/STAGE/Readiness+Assessment)
- [General migration execution links](https://confluence.aws-proserve.org/confluence/display/STAGE/Execution%3A+Deliverables)
- [Landing Zone](https://confluence.aws-proserve.org/confluence/display/STAGE/AWS+Landing+Zone)
- [Security for MRA](https://confluence.aws-proserve.org/confluence/display/STAGE/Security%3A+Deliverables)
- [Delivery Quality Program](https://drive.corp.amazon.com/folders/AWS%20ProServe%20Ops/Tools/Deal%20Quality/DQ%20Templates)
- [Customer Satisfaction Survey](https://w.amazon.com/bin/view/AWS/Teams/Proserve/Customer_Satisfaction_V2/)

## setting up dev environment

### docker

- Linux
    - [link](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html#install_docker)
- OS X
    - [link](https://docs.docker.com/docker-for-mac/install/)

### python3

- ensure homebrew is installed (OS X only)
    - `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
    - restart terminal
- install python3
    - OS X
        - `brew install python3`
    - Linux
        - `sudo apt-get install python3`
    - `which python3`
        - `/usr/local/bin/python3`
- setup virtualenvironment
    - this will be the python you'll be using for development
        - it makes a copy so you don't pollute your global python installation
    - `cd a2c-capstone`
    - OS X
        - `brew install pipenv`
    - Linux
        - `sudo apt-get install pipenv`
    - create the virtualenv
        - `pipenv --python 3.7`
    - activate this python. you'll have to do this whenever you have a new terminal
        - `pipenv shell`
    - verify it's setup correctly
        - `pipenv --venv`
        - `/Users/rayjwil/.local/share/virtualenvs/a2c-capstone`

### node and serverless.js

- ensure homebrew is installed (OS X only)
    - `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
    - restart terminal
- install git
    - OS X
        - `brew install git`
    - Linux
        - `sudo apt-get install git`
    - `which git`
        - `/usr/local/bin/git`
- install node version manager
    - [link](https://github.com/nvm-sh/nvm)
    - `wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash`
        - you may have to fiddle with your bash or zsh profile files
        - details are in the link provided above
    - `nvm install v12`
    - `node --version`
        - `v12.3.1`
- install serverless.js
    - `npm install -g serverless`
        - `1.43.0`

## Setting up GreenGrass on RasPi3

### Create new sdcard

#### Backup SD Card image (OS X)

- insert sd card
- `diskutil list`
- note the location (ie `/dev/disk3`)
- `sudo dd if=/dev/disk3 of=/Users/rayjwil/Desktop/phi-prototype.img`
  - note: `of=` must be absolute path, not relative path
  - this will take many minutes and will sieze control of your terminal

#### Etch new SD Card

Download latest Raspbian OS Image
- https://downloads.raspberrypi.org/raspbian_lite_latest

- use [etcher.io](https://etcher.io/) to etch the sdcard with the image you downloaded
- when finished etching, etcher will unmount the sdcard
- reinsert sd card

_NOTE: many of the config files are in `a2c-capstone/raspi3/configs`_
- edit files in boot folder

  - `cd /Volumes/boot`
  - Enable wifi at boot

    - create the wpa_supplicant.conf file

      ```bash
      #wpa_supplicant.conf
      ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
      update_config=1
      country=US

      network={
          ssid="myssid"
          scan_ssid=1
          psk="mypass"
          key_mgmt=WPA-PSK
      }
      ```

    - sometimes this is what you need (WPA-1 type routers)

      ```bash
      #wpa_supplicant.conf
      ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
      update_config=1
      country=US

      network={
          ssid="myssid"
          scan_ssid=1
          psk="mypass"
          pairwise=CCMP
          auth_alg=OPEN
          key_mgmt=WPA-PSK
      }
      ```

  - Enable ssh at boot
    - create an empty file named `ssh`
  - edit `config.txt`

    - uncomment

      ```bash
      # Uncomment some or all of these to enable the optional hardware interfaces
      dtparam=i2c_arm=on
      #dtparam=i2s=on
      dtparam=spi=on
      ```

    - add to bottom

      ```bash
      start_x=1
      gpu_mem=128
      ```

  - edit `cmdline.txt`
    - add `cgroup_enable=cpuset cgroup_enable=memory` to end of line

#### Boot Raspberry Pi and configure

_NOTE: many of the config files are in `a2c-capstone/raspi3/configs`_

- insert sdcard into raspi
- boot / power up
- from your laptop
  - `ping raspberrypi.local`
  - `ssh pi@raspberrypi.local`
    - you may have to delete an entry in `~/.ssh/known_hosts`
    - pw is `raspberry`
  - `sudo apt-get update`
- follow instructions outlined in greengrass documentation
  - [Module 1 - Environment Setup](https://docs.aws.amazon.com/greengrass/latest/developerguide/module1.html)
  - [Module 2 - Installing the Greengrass Core Software](https://docs.aws.amazon.com/greengrass/latest/developerguide/module2.html)
- add the greengrass user to groups
  - `sudo usermod -a -G spi,i2c,gpio ggc_user`

- enable greengrass as a service

  - make `/etc/init.d/greengrass`
    ```bash
    #!/bin/sh
    ### BEGIN INIT INFO
    # Provides:          greengrass
    # Required-Start:    $all
    # Required-Stop:
    # Default-Start:     2 3 4 5
    # Default-Stop:
    # Short-Description: Starts greengrass...
    ### END INIT INFO
    mkdir -p /tmp/images
    chmod 777 /tmp/images
    mkdir -p /greengrass/certs
    mkdir -p /greengrass/config
    cp /boot/certs/* /greengrass/certs/
    cp /boot/config/* /greengrass/config/
    /greengrass/ggc/core/greengrassd start
    ```
  - `sudo chmod 755 /etc/init.d/greengrass`
  - make `/etc/systemd/system/greengrass.service`

    ```bash
    [Unit]
    Description=AWS Greengrass Service
    After=network.target

    [Service]
    Type=simple
    ExecStart=/etc/init.d/greengrass
    RestartSec=2
    Restart=always
    User=root
    PIDFile=/var/run/greengrassd.pid

    [Install]
    WantedBy=multi-user.target
    ```

  - `sudo systemctl enable greengrass.service`
    - makes sure the service is started at every boot

- enable i2c-dev on boot
  - add `i2c-dev` on it's own line to `/etc/modules`

#### Configure GreenGrass

- IoT console
  - [Module 3 (part 1) - Lambda Functions on AWS Greengrass](https://docs.aws.amazon.com/greengrass/latest/developerguide/module3-I.html)
  - [Module 3 (part 2) - Lambda Functions on AWS Greengrass](https://docs.aws.amazon.com/greengrass/latest/developerguide/module3-II.html)
- `aws greengrass get-service-role-for-account`
  - get the arn
- `aws greengrass associate-service-role-to-account --role-arn <ROLE_ARN>`
