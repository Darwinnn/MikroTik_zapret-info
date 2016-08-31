import StringIO
import zipfile
import base64

import suds

class NoResult(Exception):

    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value.encode("utf-8"))

class API(object):
    def __init__(self):
        self.cl = suds.client.Client("http://vigruzki.rkn.gov.ru/services/OperatorRequest/?wsdl")

    def getLastDumpDate(self):
        return self.cl.service.getLastDumpDate()
    
    def getLastDumpDateEx(self):
        return self.cl.service.getLastDumpDateEx()

    def getResult(self, code):
        return self.cl.service.getResult(code)
    
    def sendRequest(self, request, signature):
        return self.cl.service.sendRequest(request, signature, "2.0")

    def get_code(self, request, signature):
        """ request and signature should be file paths """
        with open(request, "r") as req, open(signature, "r") as sign:
            b64_request = base64.b64encode(req.read())
            b64_signature = base64.b64encode(sign.read())
        
        result = self.sendRequest(b64_request, b64_signature)

        if not result.result:
            raise NoResult(result.resultComment)

        return result.code

    def get_xml(self, code):
        result = self.getResult(code)
        if not result.result:
            raise NoResult(result.resultComment)

        zip_io = StringIO.StringIO()
        zip_io.write(base64.b64decode(result.registerZipArchive))

        zip_file = zipfile.ZipFile(zip_io)
        xml = zip_file.read("dump.xml")
        zip_file.close()

        return xml
