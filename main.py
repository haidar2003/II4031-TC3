import base64
from http.client import HTTPException
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import uvicorn
import json
import os
from rsa_encryption import *
from pydantic import BaseModel

class Key(BaseModel):
    key_type: str
    exponent: int
    modulus: int

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

@app.get('/rsa/keygen')
async def keygen():
    public_key, private_key = generate_key(10, 10000000)
    return {'public_key': public_key, 'private_key': private_key}

@app.post('/rsa/file/encrypt')
async def encrypt_file(key: Key, output_file_name: str, output_file_extension: str, file: UploadFile = File(...)):
    
    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(400,detail='File bermasalah')
    
    key_json = json.dumps({'key_type': key.key_type, 'exponent': key.exponent, 'modulus': key.modulus})
    
    file_decoded = file_bytes.decode('latin1')

    file_decoded_encrypted = rsa_string_encrypt(file_decoded, key_json, 4) # string

    new_output_file_name = f'{output_file_name}.{output_file_extension}'

    SAVE_FILE_PATH = os.path.join(UPLOAD_DIR, new_output_file_name)

    with open(SAVE_FILE_PATH, "wb") as f:
        f.write(file_decoded_encrypted.encode('latin-1'))

    return FileResponse(path=SAVE_FILE_PATH, media_type="application/octet-stream", filename=new_output_file_name)

@app.post('/rsa/file/decrypt')
async def encrypt_file(file: UploadFile, key: Key, output_file_name: str, output_file_extension: str):
    
    file_bytes = await file.read()

    return{{'output': file_bytes}}

    # if not file_bytes:
    #     raise HTTPException(400,detail='File bermasalah')
    
    # key_json = json.dumps({'key_type': key.key_type, 'exponent': key.exponent, 'modulus': key.modulus})
    
    # file_decoded = file_bytes.decode('latin1')

    # file_decoded_encrypted = rsa_string_decrypt(file_decoded, key_json, 4) # string

    # new_output_file_name = f'{output_file_name}.{output_file_extension}'

    # SAVE_FILE_PATH = os.path.join(UPLOAD_DIR, new_output_file_name)

    # with open(SAVE_FILE_PATH, "wb") as f:
    #     f.write(file_decoded_encrypted.encode('latin-1'))

    # return FileResponse(path=SAVE_FILE_PATH, media_type="application/octet-stream", filename=new_output_file_name)


@app.post('/rsa/string/encrypt')
async def encrypt_file(string: str, key: Key, output_file_name: str, output_file_extension: str):

    if not str:
        raise HTTPException(400,detail='String bermasalah')
    
    key_json = json.dumps({'key_type': key.key_type, 'exponent': key.exponent, 'modulus': key.modulus})

    string_encrypted = rsa_string_encrypt(string, key_json, 4) # string

    new_output_file_name = f'{output_file_name}.{output_file_extension}'

    SAVE_FILE_PATH = os.path.join(UPLOAD_DIR, new_output_file_name)

    with open(SAVE_FILE_PATH, "wb") as f:
        f.write(string_encrypted.encode('latin-1'))

    return FileResponse(path=SAVE_FILE_PATH, media_type="application/octet-stream", filename=new_output_file_name)
    

@app.post('/rsa/string/decrypt')
async def encrypt_file(string: str, key: Key, output_file_name: str, output_file_extension: str):
    
    if not str:
        raise HTTPException(400,detail='String bermasalah')
    
    key_json = json.dumps({'key_type': key.key_type, 'exponent': key.exponent, 'modulus': key.modulus})

    string_decrypted = rsa_string_decrypt(string, key_json, 4) # string

    new_output_file_name = f'{output_file_name}.{output_file_extension}'

    SAVE_FILE_PATH = os.path.join(UPLOAD_DIR, new_output_file_name)

    with open(SAVE_FILE_PATH, "wb") as f:
        f.write(string_decrypted.encode('latin-1'))

    return FileResponse(path=SAVE_FILE_PATH, media_type="application/octet-stream", filename=new_output_file_name)
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)






