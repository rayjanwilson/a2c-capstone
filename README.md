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
    - `cd a2c-capstone/webapp-api`
    - `python3 -m venv venv`
    - activate this python. you'll have to do this whenever you have a new terminal
    - `source venv/bin/activate`
    - `which python3`
        - `/Users/rayjwil/dev/git/a2c-capstone/webapp-api/venv/bin/python3`

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
