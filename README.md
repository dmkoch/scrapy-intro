scrapy-intro
============

Introduction to Scrapy presentation for CharPy meetup Sep. 25, 2013

### To run the demo:

#### 1. Download and install these packages

* Virtual Box, http://www.virtualbox.org/
* Vagrant, http://www.vagrantup.com/

#### 2. Fire up the virtual machine and log in

    git clone https://github.com/dmkoch/scrapy-intro
    cd scrapy-intro
    vagrant up
    vagrant ssh

#### 3. Install PyPI requirements

    pip install -r /vagrant/requirements.txt

#### 4. Run the spider

    cd /vagrant/newsbot
    scrapy crawl cnn -o articles.json

### To build the presentation:

    cd /vagrant
    make
    # presentation is created here: build/presentation.html
