from typing import Annotated

from fastapi import FastAPI, File, UploadFile ,Request ,Response

from fastapi.encoders import jsonable_encoder


from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
    ORJSONResponse,
    PlainTextResponse,
    RedirectResponse,
    Response,
    StreamingResponse,
    UJSONResponse,
)

import pdf_parsing as pp

from pydantic import BaseModel

import json

import pickle

from zipfile import ZipFile 

fake_db = {}


class Item(BaseModel):
    title: str
    text: str


app = FastAPI()


@app.put("/items/")
def update_item(item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    print(json_compatible_item_data)
    return json_compatible_item_data



##This block will give the size if someone hits url http:127.0.0.1/files/
##app is the name of the application.
@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

##This block will give the filename if someone hits url http:127.0.0.1/get_uploaded_file_name/
##app is the name of the application.
@app.post("/get_uploaded_file_name/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


@app.post("/download/")
async def summmary_type(
    request: Request,
):
    option= await request.body()
    print("JSON REPRESENTING YES OR NO")
    print(str(option))
    
    #return {
    #    "JSON Payload": {"type": option},
    #}
    return Response(content=option)


##This block will receive the pdf file and write its content to a temporary file which will be consumed by downsteam application.
##In our case the downstream apllication id pdf_parding with the name pp.
@app.post("/uploadfile/")
async def create_upload_file(request:Request,file: UploadFile):
    ##Read File content ansynchronous manner else it will fail for large files
    content=await file.read()
    
    ##Read JSON content ansynchronous manner else it will fail for large files
    #option= await request.body()
    
    #print("input mail option type json")
    #print(option)
    
    #print("input mail option type value")
    #print(option['option'])
    
    
    ##Get the filename of the file that will be uploaded by the client
    filename=file.filename
    
    
    
    ##Read the content of PDF and write it back to another PDF file on client side
    ##This received PDF will sent to for parsing.
    with open(filename,'wb') as handle:
        handle.write(content)
        
   
    ##this function immported from pdf_parsing package.
    ##It will parse the pdf and return back the parsed content in form of a dictionary
    parsed_pdf=pp.extract_text_images_tables('./'+filename)
    
    print(type(parsed_pdf))
    
    print("filename")
    print(filename)
    
    with open(filename+'.pickle', 'wb') as f:
        pickle.dump(parsed_pdf, f)
    
    with ZipFile(filename+'.zip', 'w') as myzip:
        myzip.write(filename+'.pickle')
    
    print('Zip complete.')
    
    def generate():
        with open(filename+'.zip', "rb") as fwav:
            data = fwav.read(8192)
            while data:
                yield data
                #print('sending file')
                #print('..')
                data = fwav.read(8192)
                
    print('diarized zip file sent')
    
    #print(type(parsed_pdf.to_json()))
    
    #return val
    #return Response(generate(), mimetype="audio/x-wav")
    return FileResponse(filename+'.pickle')
    
    #return Response(content=filename+'.zip')