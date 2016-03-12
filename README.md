Install the following if you don't already have them:

To install Selenium:
sudo pip install selenium

To install PhantomJS:

(if you have nodeJS installed already)
sudo npm -g install phantomjs

To install NodeJS (OPTIONAL: only needed to install PhantomJS):
sudo apt-get install nodejs


Alternatively, you can install PhantomJS by downloading the required package from the main site:
http://phantomjs.org/download.html


Add the path of the phantomJS executable to the file 'phantompath.txt'


run the program using:
python find_email_addresses.py <website_name>

for example, to show all emails in jana.com, do:
python find_email_addresses.py jana.com
