import configparser
import sys 
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + 'util')
from HttpMultiPartRequest import *

# sample entry
def main():
    # region setup ocr url and api key
    config = configparser.ConfigParser()
    config.readfp(open(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + 'util' + os.path.sep + 'config.properties'))
    strOcrHostUri = config.get('AppConfig', 'strOcrHostUri')
    strOcrFileUri = config.get('AppConfig', 'strOcrFileUri')
    strApiKey = config.get('AppConfig', 'strApiKey')
    
    dicHeader = {'x-api-key': strApiKey}
    
    # region 1. upload file
    print('-----------------------------------------------------------------------')
    print('1. Upload file...')
    
    formData = FormData()
    formData.append('method', EnumOcrFileMethod['upload'])
    formData.append('file', Comm.getFileData('example.jpg'), 'example.jpg')
    
    try:
        httpWebResponse = HttpMultiPartRequest.post(strOcrHostUri, strOcrFileUri, dicHeader, formData)
        restfulApiResponse = Comm.parseHttpWebResponseToRestfulApiResult(httpWebResponse, EnumOcrFileMethod['upload'])
        strFileName = Comm.handleRestfulApiResponse(restfulApiResponse, EnumOcrFileMethod['upload'])
        if(strFileName is None):
            return
    except Exception as ex:
        print(str(ex))
        return
    
    # region 2. recognize the uploaded file
    print(os.linesep + '-----------------------------------------------------------------------')
    print('2. Recognize the uploaded file...')
    
    formData.clear()
    formData.append('method', EnumOcrFileMethod['recognize'])
    formData.append('file_name', strFileName)
    formData.append('language', 'eng')
    formData.append('output_format', 'UFormattedTxt')
    formData.append('page_range', '1-10')
    
    try:
        httpWebResponse = HttpMultiPartRequest.post(strOcrHostUri, strOcrFileUri, dicHeader, formData)
        restfulApiResponse = Comm.parseHttpWebResponseToRestfulApiResult(httpWebResponse, EnumOcrFileMethod['recognize'])
        strFileName = Comm.handleRestfulApiResponse(restfulApiResponse, EnumOcrFileMethod['recognize'])
        
        if(strFileName is None):
            return
    except Exception as ex:
        print(str(ex))
        return
    
    # region 3. download the recognized file
    print(os.linesep + '-----------------------------------------------------------------------')
    print('3. Download the recognized file...')    
    
    formData.clear();
    formData.append("method", EnumOcrFileMethod['download']);
    formData.append("file_name", strFileName);    
    
    try:
        httpWebResponse = HttpMultiPartRequest.post(strOcrHostUri, strOcrFileUri, dicHeader, formData)
        restfulApiResponse = Comm.parseHttpWebResponseToRestfulApiResult(httpWebResponse, EnumOcrFileMethod['download'])
        Comm.handleRestfulApiResponse(restfulApiResponse, EnumOcrFileMethod['download'])
    except Exception as ex:
        print(str(ex))
        return
    

main()    
    
    