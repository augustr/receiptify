#!/usr/bin/env python

import MySQLdb
import sys
import threading
import time
import subprocess
from os import walk

# Simple database layer over MySQL.
# Move this to its own file and import.
class DBLayer:
    self._connection = None
    self._cursor = None

    def __init__(self):
        pass

    def open(self):
        try:
            self._connection = MySQLdb.connect('localhost', 'receiptify', 'GZuzJh842yVXwwhB', 'receiptify')
            self._cursor = self._connection.cursor()
        except MySQLdb.Error, e:
            print str(e)
            sys.exit(1)

    def close(self)
        if self._connection:
            self._connection.close()

    def add_unprocessed_receipt(self, filename, data):
        self._cursor.execute("INSERT INTO receipts_unprocessed('filename', 'data') VALUES(%s,%s)", (filename, data))

    def unprocessed_receipt_exists(self, filename):
        self._cursor.execute("SELECT id FROM receipts_unprocessed WHERE filename=%s", (filename))
        row = cursor.fetchone()
        if row:
            return True
        else:
            return False

# Main daemon class
# Move this to its own file and import
class ReceiptifyDirectoryWatcher(threading.Thread):
    self._watch_dir = None
    self._database = None

    def __init__(self, watch_dir, database):
        self._watch_dir = watch_dir
        self._database = database

    def run(self):
        while(True):
            scanned_files = []
            for (dirpath, dirnames, filenames) in walk(self._watch_dir):
                for filename in filenames:
                    self._parse_and_add(os.path.join(dirpath, filename)

            time.sleep(60) 
        pass

    def _is_scanned_receipt(self, filename):
        return filename.endswith(".tif") or filename.endswith(".jpg")

    def _parse_and_add(self, filepath):
        filename = os.basename(filepath)

        if (_is_scanned_receipt(filename)):
            print "Not a scanned receipt: %s" % (filename)
            return False
        if not self._database.unprocessed_receipt_exists(filename)):
            return False

        # OCR using tesseract to tempfile
        data = subprocess.check_output("tesseract %s stdout -l swe" % (filepath), shell = True)

        # Add to database
        self._database.add_unprocessed_receipt(filename, data)

def main():
    instance = Receiptify()
    instance.start()

if __name__ == "__main__":
    main()
