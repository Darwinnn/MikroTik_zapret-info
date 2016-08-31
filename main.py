import sys
import logging

import config
import zapret.api
import zapret.mikrotik

from lxml import etree
from time import sleep

def main(check_urgent=False):
    """ Main routine """
    api = zapret.api.API()
    lasturgentdate = api.getLastDumpDateEx().lastDumpDateUrgently
    logging.basicConfig(format='%(asctime)s %(message)s', filename=config.LOG_FILENAME, level=logging.WARNING)
    
    if check_urgent:
        with open(config.LASTDATEURGENT, "r") as f:
            if f.read() != str(lasturgentdate):
                logging.warning("New urgent update, lastDumpDateUrgently: %s" % lasturgentdate)
            else:
                return

    with open(config.LASTDATEURGENT, "w+") as f:
        f.write(str(lasturgentdate))
 
    code = api.get_code(config.REQUEST_FILENAME, config.SIGNATURE_FILENAME)
    logging.warning("Got request code: %s" % code)

    counter = 0
    while True:
        try:
            xml = api.get_xml(code)
            tree = etree.fromstring(xml)
            ips = list(set([i.text for i in tree.xpath('//ip')]))
            subnets = list(set([i.text for i in tree.xpath('//ipSubnet')]))
            logging.warning("Parsed %s uniq IPs and %s subnets from the XML" % (len(ips), len(subnets)))
            # ToDo: mail notification
            zapret.mikrotik.add_addresslist(config.SERVERS, ips+subnets)
            logging.warning("Successfully added to MikroTik")
            break

        except zapret.api.NoResult as e:
            counter += 1
            if counter >= config.ATTEMPTS:
                logging.warning("Stopped after %d failed attempts to request the xml" % counter)
                break
            logging.warning("Caught NoResult error with: %s" % e.value)
            sleep(config.ATTEMPT_TIME)

if __name__ == "__main__":
     if "--check-urgent" in sys.argv:
         main(check_urgent=True)
     else: 
         main()
