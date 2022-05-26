Sumo Logic SQS  Importer
========================

sqsimport is a generic SQS queue reader, and can be used to read  events off of a SQS  queue and write the output to a file.

Installing the Scripts
=======================

This script is designed to be run from a local machine, either as a sttanding environment or a lambda.
It is a python3 script, and the list of the python modules is provided to aid people using a pip install.

You will need to use Python 3.6 or higher and the modules listed in the dependency section.  

The steps are as follows: 

    1. Download and install python 3.6 or higher from python.org. Append python3 to the LIB and PATH env.

    2. Download and install git for your platform if you don't already have it installed.
       It can be downloaded from https://git-scm.com/downloads
    
    3. Open a new shell/command prompt. It must be new since only a new shell will include the new python 
       path that was created in step 1. Cd to the folder where you want to install the scripts.
    
    4. Execute the following command to install pipenv, which will manage all of the library dependencies:
    
        sudo -H pip3 install pipenv 
 
    5. Clone this repo using git clone
    
    6. Change into the folder. Type the following to install all the package dependencies 
       (this may take a while as this will download all of the libraries that it uses):

        pipenv install
        
Dependencies
============
See the contents of "pipfile"

Caveats
=======
This script consumes data from an AWS SQS queue. If implemented from your AWS environment
it may result in extra charges. Please set up billing alerts and baseline use carefully!

Example Use
===========

    1. Show a help message
       ./sqsimport.py -h

    2. Use a specific configuration file
       ./sqsimport.py -c <configfile>

To Do List
==========

* make the logic asyncrhonous via yield
* implement a count for sampling 
* implement cutoff after N messages

License
=======

Copyright 2019 Wayne Kirk Schmidt
https://www.linkedin.com/in/waynekirkschmidt

Licensed under the Apache 2.0 License (the "License");

You may not use this file except in compliance with the License.
You may obtain a copy of the License at

    license-name   APACHE 2.0
    license-url    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Support
=======

Feel free to e-mail me with issues to: 

*    wschmidt@sumologic.com

*    wayne.kirk.schmidt@gmail.com

I will provide "best effort" fixes and extend the scripts.
