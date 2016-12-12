#!/usr/bin/env python

import MySQLdb
import sys
import threading
import time
import subprocess
import os
import signal
from os import walk

# Simple database layer over MySQL.
# Move this to its own file and import.
class DBLayer:
    def __init__(self):
        pass

    def open(self):
        try:
            self._connection = MySQLdb.connect('localhost', 'receiptify', 'GZuzJh842yVXwwhB', 'receiptify')
            self._cursor = self._connection.cursor()
        except MySQLdb.Error, e:
            print str(e)
            sys.exit(1)

    def close(self):
        if self._connection:
            self._connection.close()

    def add_unprocessed_receipt(self, filename, data):
        self._cursor.execute("INSERT INTO receipts(filename, data) VALUES(%s,%s)", (filename, data))
        self._connection.commit()

    def unprocessed_receipt_exists(self, filename):
        self._cursor.execute("SELECT id FROM receipts WHERE filename=%s", (filename,))
        row = self._cursor.fetchone()
        if row is None:
            return False
        else:
            return True

# Main daemon class
# Move this to its own file and import
class ReceiptifyDirectoryWatcher(threading.Thread):
    def __init__(self, watch_dir, database):
        super(ReceiptifyDirectoryWatcher, self).__init__()
        self._watch_dir = watch_dir
        self._database = database
        self._running = False

    def run(self):
        self._running = True
        counter = 60
        while(self._running):
            counter += 1
            if counter > 60:
                counter = 0
                print "Scanning directory: %s" % (self._watch_dir)
                scanned_files = []
                for (dirpath, dirnames, filenames) in walk(self._watch_dir):
                    for filename in filenames:
                        self._parse_and_add(os.path.join(dirpath, filename))

            time.sleep(1)

    def stop(self):
        self._running = False

    def _is_scanned_receipt(self, filename):
        return filename.endswith(".tif") or filename.endswith(".jpg")

    def _parse_and_add(self, filepath):
        filename = os.path.basename(filepath)

        if not self._is_scanned_receipt(filename):
            print "Not a scanned receipt: %s" % (filename)
            return False
        if self._database.unprocessed_receipt_exists(filename):
            print "Already added: %s" % (filename)
            return False

        # OCR using tesseract to tempfile
        print "Analyzing image: %s" % (filename)
        data = subprocess.check_output("tesseract %s stdout -l swe" % (filepath), shell = True)

        # Add to database
        self._database.add_unprocessed_receipt(filename, data)

        print "Added image: %s" % (filename)

def main(directory):
    print "Starting database layer..."
    database = DBLayer()
    database.open()
    print "Starting directory watcher [%s]..." % (directory)

    try:
        instance = ReceiptifyDirectoryWatcher(directory, database)
        instance.start()
        while instance.is_alive():
            instance.join(1)
    except (KeyboardInterrupt, SystemExit):
        print "Exiting..."
        instance.stop()
        sys.exit()

if __name__ == "__main__":
    main(sys.argv[1])
