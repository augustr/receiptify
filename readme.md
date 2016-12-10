# Receiptify

## Overview

This project aims to automate the process of registering, analyzing and
presenting data from physical receipts, from OCR to web based statistics.

## Installation

You need to install tesseract, python and python-mysqldb. Then it should
only be a matter of running the receiptify.py script. Note that this is
a work in progress. At the time of writing this, no code has been tested
at all.

## How it works

It is to be implemented as a python daemon that watches a directory in
which scanned images can be transfered to by a scanner. The daemon then
checks for new images, OCR's them using open source project tesseract,
stores them in a database.

A web based system is then to be built (using python flask or similar?)
that reads the OCR'd data and finds out the individual items and prices,
allowing the user to fix OCR errors before the data is stored in a
structured way in the database, available later for statistics pages.

## Contributors

Feel free to give feedback or merge requests!

## License

Code relased under [the MIT license](https://github.com/twbs/bootstrap/blob/master/LICENSE)
