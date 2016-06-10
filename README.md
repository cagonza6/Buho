# Buho (see "dev" branch)

Buho is a basic library manager for schools. It allowed to control a small size library and meant to be the replacement of the old card records system. It is tested just under Linux.

## Considerations?

* It still is in development phase, so there is not guaranty that it will work

## Features

* ID cards: It allows you to create a batch of ID cards with an unique user ID that can be scanned with a barcode reader.
* Book Code: It allows the creation of books sticker that contains the unique ID with its barcode.
* Loan/Return tracking: it allows you to have a control of what books are loaned and what is currently in the inventory, also you can have the statistics and logs of every book. * Reports: it has implemented the repots module with what you will be able to obtain some valuable information of the most loaned books, popular topics, etc. This reports, can be printed in PDF.

### Missing features?

* More reports options
* More statistics
* Mysql support
* Web version???
* Server functions?
     * Permissions system for server client<->comunication

## Requirements

* Linux Based System
* PyQt
* labreport (python library)



## Installation

Basically run the run.sh file and let the system complain and tell you what you need to install. Since it still is a quick an dirty solution it has not an installer... sorry about that...
