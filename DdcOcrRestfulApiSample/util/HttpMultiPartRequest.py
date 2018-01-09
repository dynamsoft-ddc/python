import uuid
import http.client
import sys 
import os

from builtins import str

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Comm import *
from FormData import FormData

class HttpMultiPartRequest:
    @staticmethod
    # post multi-part form data
    def post(strHost, strUrl, dicHeader, formData):
        if((not isinstance(strHost, str)) or len(strHost) == 0 or
           (not isinstance(strUrl, str)) or len(strUrl) == 0):
            raise Exception('Url is invalid.')
        
        strBoundary = 'DdcOrcRestfulApiSample' + uuid.uuid4().hex
        
        bytesBodyData = HttpMultiPartRequest.constructRequestBodyData(formData, strBoundary)
        
        if(bytesBodyData is None):
            raise Exception('Reqeust body invalid.')
        
        conn = http.client.HTTPConnection(strHost)
        # Please use below statement if HTTPS support is available
        # HTTPS support is only available if Python was compiled with SSL support (through the ssl module).
        # conn = http.client.HTTPSConnection(strHost)
        
        conn.putrequest('POST', strUrl)
        
        conn.putheader('content-type', 'multipart/form-data; boundary=' + strBoundary)
        conn.putheader('content-length', str(len(bytesBodyData)))        
        for key, value in dicHeader.items():
            conn.putheader(key, value)            
        conn.endheaders()       
        
        conn.send(bytesBodyData) 
        
        return conn.getresponse()
    
    @staticmethod
    # construct request body data
    def constructRequestBodyData(formData, strBoundary):        
        if((not isinstance(formData, FormData)) or (not formData.isValid())):
            return None       
        
        listBodyData = []
        
        bHasItemAdded = False        
        strNewLine = '\r\n'
        strBoundarySeparator = '--'
        strEncoding = 'utf-8'
        
        for (strKey, value, strFileName) in formData.getAll():            
            if(bHasItemAdded): 
                listBodyData.append(bytes(strNewLine, strEncoding))
            
            if(strFileName is None):
                listBodyData.append(bytes(strBoundarySeparator + strBoundary + strNewLine + 
                                    'Content-Disposition: form-data; name="' + strKey + '"' +
                                    strNewLine + strNewLine +
                                    value, strEncoding))
            else:
                listBodyData.append(bytes(strBoundarySeparator + strBoundary + strNewLine + 
                                    'Content-Disposition: form-data; name="' + strKey + '"; ' + 
                                    'filename="' + strFileName + '"' + strNewLine +
                                    'Content-Type: ' + ('text/plain' if isinstance(value, str) else 'application/octet-stream') +
                                    strNewLine + strNewLine, strEncoding))
                
                listBodyData.append(bytes(value, strEncoding) if isinstance(value, str) else value)
                
            bHasItemAdded = True
            
        if(bHasItemAdded):
            listBodyData.append(bytes(strNewLine + strBoundarySeparator + strBoundary + strBoundarySeparator + strNewLine, strEncoding))
            
        return b''.join(listBodyData)

    