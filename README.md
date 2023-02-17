This code can be used to monitor websites. The code can be used to display information about the status of a website, indicating whether it is up or down.

Requirements

The following modules need to be installed via pip3 before running the program:

fake_useragent
requests
colorama

Usage

The following steps must be taken before the program can be used:

* Install the required modules (see requirements)
* Add URLs for websites to be monitored in lankar.py
* Start the program with $python3 siteup2.py


The program prints a status report for each monitored website. If a website is unresponsive, the program will display a warning with information on the status code and any error messages that may have occurred.

The program also uses colors to make the status reports easier to read:

Red: if the website is down or unresponsive.

Green: if the website is up and available.

Yellow: when the website is returning statuscode 200 again, it will notify you about the downtime.

Developer
This code is written by a person named schakalen12 and is available on Github under schakalen12/Scripts. The purpose of the code is to create a simple monitoring solution for websites, in my case swedish government agency websites, but it is also a good starting point for creating more advanced tools for website monitoring.
