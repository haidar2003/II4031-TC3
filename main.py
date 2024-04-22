import base64
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import os
from rsa_encryption import *
from pydantic import BaseModel

origins = [
    "http://localhost:80",
    "http://localhost:5173",
]

current_user = 0

class Key(BaseModel):
    key_type: str
    exponent: int
    modulus: int

class UserData(BaseModel):
    file_name: str
    file_extension: str
    public_key: Key
    private_key: Key
    partner_key: bool

class FileMetadata(BaseModel):
    output_file_name: str
    output_file_extension: str

class Text(BaseModel):
    input_text: str


users = {
    1: UserData(file_name='user_1', file_extension='txt', public_key=Key(key_type='', exponent=0, modulus=0), private_key=Key(key_type='', exponent=0, modulus=0), partner_key=False),
    2: UserData(file_name='user_2', file_extension='txt', public_key=Key(key_type='', exponent=0, modulus=0), private_key=Key(key_type='', exponent=0, modulus=0), partner_key=False)
}



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
USER_DATA_FILE = os.path.join(BASE_DIR, "users.json")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.delete('/app/reset')
async def reset():
    global current_user
    global users

    current_user = 0

    users = {
    1: UserData(file_name='user_1', file_extension='txt', public_key=Key(key_type='', exponent=0, modulus=0), private_key=Key(key_type='', exponent=0, modulus=0), partner_key=False),
    2: UserData(file_name='user_2', file_extension='txt', public_key=Key(key_type='', exponent=0, modulus=0), private_key=Key(key_type='', exponent=0, modulus=0), partner_key=False)
}


@app.get('/user')
def get_users():
    return users

@app.get('/user/current_user')
def get_current_user():
    return current_user

@app.put('/user/generate_key')
async def generate_user_key(user_id: int):
    global current_user
    global users

    if user_id not in users:
        raise HTTPException(status_code=404, detail=f'User {user_id} tidak ditemukan')

    public_key, private_key = generate_key(10, 10000000)

    public_key_dict = json.loads(public_key)
    private_key_dict = json.loads(private_key)

    user = users[user_id]

    user.public_key.key_type = 'public'
    user.private_key.key_type = 'private'
    user.public_key.exponent = public_key_dict['exponent']
    user.public_key.modulus = public_key_dict['modulus']
    user.private_key.exponent = private_key_dict['exponent']
    user.private_key.modulus = private_key_dict['modulus']

    if user_id == 1:
        users[2].partner_key = False
    elif user_id == 2:
        users[1].partner_key = False

    KEY_PATH = os.path.join(BASE_DIR, "key")

    public_key_file = os.path.join(KEY_PATH, f"user_{user_id}.pub")
    private_key_file = os.path.join(KEY_PATH, f"user_{user_id}.pri")

    with open(public_key_file, 'w') as f:
        json.dump(public_key_dict, f)
    with open(private_key_file, 'w') as f:
        json.dump(private_key_dict, f)

    return {'user': users[user_id]}

@app.get('/user/{user_id}/public_key')
async def download_user_public_key(user_id: int):
    global users

    if user_id not in users:
        raise HTTPException(status_code=404, detail=f'User {user_id} tidak ditemukan')

    user = users[user_id]

    if user.public_key.key_type != 'public':
        raise HTTPException(status_code=404, detail=f'User {user_id} tidak memiliki public key')

    KEY_PATH = os.path.join(BASE_DIR, "key")
    public_key_file = os.path.join(KEY_PATH, f"user_{user_id}.pub")

    if not os.path.exists(public_key_file):
        raise HTTPException(status_code=404, detail=f'File public key user {user_id} tidak ditemukan')

    with open(public_key_file, 'rb') as f: 
        return FileResponse(public_key_file, media_type='application/octet-stream', filename=f"user_{user_id}_public_key.pub")


@app.get('/user/{user_id}/private_key')
async def download_user_private_key(user_id: int):
    global users

    if user_id not in users:
        raise HTTPException(status_code=404, detail=f'User {user_id} tidak ditemukan')

    user = users[user_id]

    if user.private_key.key_type != 'private':
        raise HTTPException(status_code=404, detail=f'User {user_id} tidak memiliki private key')

    KEY_PATH = os.path.join(BASE_DIR, "key")
    private_key_file = os.path.join(KEY_PATH, f"user_{user_id}.pub")

    if not os.path.exists(private_key_file):
        raise HTTPException(status_code=404, detail=f'File private key user {user_id} tidak ditemukan')

    with open(private_key_file, 'rb') as f: 
        return FileResponse(private_key_file, media_type='application/octet-stream', filename=f"user_{user_id}_private_key.pri")

@app.put('/user/{sender_user_id}/send_key')
async def send_user_public_key(sender_user_id: int):
    global current_user
    global users

    if sender_user_id not in users:
        raise HTTPException(status_code=404, detail=f'User {sender_user_id} tidak ditemukan')

    user = users[sender_user_id]

    if user.public_key.key_type == '':
        raise HTTPException(status_code=400, detail=f'User {sender_user_id} belum memiliki kunci')

    if sender_user_id == 1:
        users[2].partner_key = True
    elif sender_user_id == 2:
        users[1].partner_key = True

    return {'user': users[(sender_user_id % 2) + 1]}

@app.put('/user/{user_id}/file/metadata')
async def change_user_file_metadata(user_id: int, metadata: FileMetadata):
    global current_user
    global users

    if user_id not in users:
        raise HTTPException(status_code=404, detail=f'User {user_id} tidak ditemukan')
    
    user = users[user_id]

    user.file_name = metadata.output_file_name
    user.file_extension = metadata.output_file_extension

    return {'user': users[user_id]}

@app.put('/user/change_user')
async def change_user(target_user: int):
    global current_user
    global users

    if target_user not in users:
        raise HTTPException(status_code=404, detail=f'User {target_user} tidak ditemukan')

    current_user = target_user

    return current_user

@app.post('/rsa/file/encrypt')
async def encrypt_file(file: UploadFile = File(...)):
    global current_user
    global users
    
    if current_user == 0:
        raise HTTPException(status_code=400, detail='Current User belum diatur')
    
    file_bytes = await file.read()

    user = users[current_user]

    output_file_name = user.file_name

    output_file_extension = user.file_extension


    if not file_bytes:
        raise HTTPException(status_code=400, detail='File bermasalah')
    
    if not user.partner_key:
        raise HTTPException(status_code=400, detail=f'User {(current_user % 2) + 1} (partner) belum mengirim kunci')
    
    if output_file_name == '' or output_file_extension == '':
        raise HTTPException(status_code=400, detail=f'User {current_user} belum memasukkan metadata file output')
    

    public_key = users[(current_user % 2) + 1].public_key

    # Public key merupakan public key partner, bukan current user
    

    key_json = json.dumps({'key_type': public_key.key_type, 'exponent': public_key.exponent, 'modulus': public_key.modulus})
    
    file_decoded = file_bytes.decode('latin1')

    file_decoded_encrypted = rsa_string_encrypt(file_decoded, key_json, 1) # string

    new_output_file_name = f'{output_file_name}.{output_file_extension}'

    SAVE_FILE_PATH = os.path.join(UPLOAD_DIR, new_output_file_name)

    with open(SAVE_FILE_PATH, "wb") as f:
        f.write(file_decoded_encrypted.encode('latin1'))

    return FileResponse(path=SAVE_FILE_PATH, media_type="application/octet-stream", filename=new_output_file_name)


@app.post('/rsa/file/decrypt')
async def decrypt_file(file: UploadFile = File(...)):
    global current_user
    global users
    
    if current_user == 0:
        raise HTTPException(status_code=400, detail='Current User belum diatur')
    
    file_bytes = await file.read()

    user = users[current_user]

    private_key = user.private_key

    output_file_name = user.file_name

    output_file_extension = user.file_extension

    # Private key merupakan private key current user

    if not file_bytes:
        raise HTTPException(status_code=400, detail='File bermasalah')
    
    if private_key.key_type == '':
        raise HTTPException(status_code=400, detail=f'User {current_user} belum memiliki kuci')
    
    if output_file_name == '' or output_file_extension == '':
        raise HTTPException(status_code=400, detail=f'User {current_user} belum memasukkan metadata file output')

    
    key_json = json.dumps({'key_type': private_key.key_type, 'exponent': private_key.exponent, 'modulus': private_key.modulus})
    
    file_decoded = file_bytes.decode('latin1')

    file_decoded_decrypted = rsa_string_decrypt(file_decoded, key_json, 1) # string

    new_output_file_name = f'{output_file_name}.{output_file_extension}'

    SAVE_FILE_PATH = os.path.join(UPLOAD_DIR, new_output_file_name)

    with open(SAVE_FILE_PATH, "wb") as f:
        f.write(file_decoded_decrypted.encode('latin1'))

    return FileResponse(path=SAVE_FILE_PATH, media_type="application/octet-stream", filename=new_output_file_name)


@app.post('/rsa/encrypt')
async def encrypt_string(string: Text):
    global current_user
    global users

    if current_user == 0:
        raise HTTPException(status_code=400, detail='Current User belum diatur')
    

    user = users[current_user]

    output_file_name = user.file_name

    output_file_extension = user.file_extension

    # Private key merupakan private key current user

    if not string or string == '':
        raise HTTPException(status_code=400, detail='String bermasalah')
    
    if not user.partner_key:
        raise HTTPException(status_code=400, detail=f'User {(current_user % 2) + 1} (partner) belum mengirim kunci')
    
    if output_file_name == '' or output_file_extension == '':
        raise HTTPException(status_code=400, detail=f'User {current_user} belum memasukkan metadata file output')

    public_key = users[(current_user % 2) + 1].public_key
    
    key_json = json.dumps({'key_type': public_key.key_type, 'exponent': public_key.exponent, 'modulus': public_key.modulus})

    string_encrypted = rsa_string_encrypt(string.input_text, key_json, 1) # string

    new_output_file_name = f'{output_file_name}.txt'

    SAVE_FILE_PATH = os.path.join(UPLOAD_DIR, new_output_file_name)

    with open(SAVE_FILE_PATH, "wb") as f:
        f.write(string_encrypted.encode('latin1'))

    return FileResponse(path=SAVE_FILE_PATH, media_type="application/octet-stream", filename=new_output_file_name)


@app.post('/rsa/decrypt')
async def decrypt_string(string: Text):
    global current_user
    global users
    
    if current_user == 0:
        raise HTTPException(status_code=400, detail='Current User belum diatur')

    user = users[current_user]

    private_key = user.private_key

    output_file_name = user.file_name

    output_file_extension = user.file_extension

    # Private key merupakan private key current user

    if not string or string == '':
        raise HTTPException(status_code=400, detail='String bermasalah')
    
    if private_key.key_type == '':
        raise HTTPException(status_code=400, detail=f'User {current_user} belum memiliki kuci')
    
    if output_file_name == '' or output_file_extension == '':
        raise HTTPException(status_code=400, detail=f'User {current_user} belum memasukkan metadata file output')

    
    key_json = json.dumps({'key_type': private_key.key_type, 'exponent': private_key.exponent, 'modulus': private_key.modulus})

    string_decrypted = rsa_string_decrypt(string.input_text, key_json, 1) # string

    new_output_file_name = f'{output_file_name}.txt'

    SAVE_FILE_PATH = os.path.join(UPLOAD_DIR, new_output_file_name)

    with open(SAVE_FILE_PATH, "wb") as f:
        f.write(string_decrypted.encode('latin1'))

    return FileResponse(path=SAVE_FILE_PATH, media_type="application/octet-stream", filename=new_output_file_name)


@app.post('/rsa/file/encryptB64')
async def encrypt_file(file: UploadFile = File(...)):
    global current_user
    global users
    
    if current_user == 0:
        raise HTTPException(status_code=400, detail='Current User belum diatur')
    
    file_bytes = await file.read()

    user = users[current_user]

    output_file_name = user.file_name

    output_file_extension = user.file_extension


    if not file_bytes:
        raise HTTPException(status_code=400, detail='File bermasalah')
    
    if not user.partner_key:
        raise HTTPException(status_code=400, detail=f'User {(current_user % 2) + 1} (partner) belum mengirim kunci')
    
    if output_file_name == '' or output_file_extension == '':
        raise HTTPException(status_code=400, detail=f'User {current_user} belum memasukkan metadata file output')
    

    public_key = users[(current_user % 2) + 1].public_key

    # Public key merupakan public key partner, bukan current user
    

    key_json = json.dumps({'key_type': public_key.key_type, 'exponent': public_key.exponent, 'modulus': public_key.modulus})
    
    file_decoded = file_bytes.decode('latin1')

    file_decoded_encrypted = rsa_string_encrypt(file_decoded, key_json, 1) # string

    base64_encoded_data = base64.b64encode(file_decoded_encrypted.encode('latin1')).decode('latin1')

    return JSONResponse(
        content={
            'filename': f'{output_file_name}.{output_file_extension}',
            'base64_data': base64_encoded_data
        }
    )


@app.post('/rsa/file/decryptB64')
async def decrypt_file(file: UploadFile = File(...)):
    global current_user
    global users
    
    if current_user == 0:
        raise HTTPException(status_code=400, detail='Current User belum diatur')
    
    file_bytes = await file.read()

    user = users[current_user]

    private_key = user.private_key

    output_file_name = user.file_name

    output_file_extension = user.file_extension

    # Private key merupakan private key current user

    if not file_bytes:
        raise HTTPException(status_code=400, detail='File bermasalah')
    
    if private_key.key_type == '':
        raise HTTPException(status_code=400, detail=f'User {current_user} belum memiliki kuci')
    
    if output_file_name == '' or output_file_extension == '':
        raise HTTPException(status_code=400, detail=f'User {current_user} belum memasukkan metadata file output')

    
    key_json = json.dumps({'key_type': private_key.key_type, 'exponent': private_key.exponent, 'modulus': private_key.modulus})
    
    file_decoded = file_bytes.decode('latin1')

    file_decoded_decrypted = rsa_string_decrypt(file_decoded, key_json, 1) # string

    base64_encoded_data = base64.b64encode(file_decoded_decrypted.encode('latin1')).decode('latin1')

    return JSONResponse(
        content={
            'filename': f'{output_file_name}.{output_file_extension}',
            'base64_data': base64_encoded_data
        }
    )


@app.post('/rsa/encryptB64')
async def encrypt_string(string: Text):
    global current_user
    global users

    if current_user == 0:
        raise HTTPException(status_code=400, detail='Current User belum diatur')
    

    user = users[current_user]

    output_file_name = user.file_name

    output_file_extension = user.file_extension

    # Private key merupakan private key current user

    if not string or string == '':
        raise HTTPException(status_code=400, detail='String bermasalah')
    
    if not user.partner_key:
        raise HTTPException(status_code=400, detail=f'User {(current_user % 2) + 1} (partner) belum mengirim kunci')
    
    if output_file_name == '' or output_file_extension == '':
        raise HTTPException(status_code=400, detail=f'User {current_user} belum memasukkan metadata file output')

    public_key = users[(current_user % 2) + 1].public_key
    
    key_json = json.dumps({'key_type': public_key.key_type, 'exponent': public_key.exponent, 'modulus': public_key.modulus})

    string_encrypted = rsa_string_encrypt(string.input_text, key_json, 1) # string

    base64_encoded_data = base64.b64encode(string_encrypted.encode('latin1')).decode('latin1')

    return JSONResponse(
        content={
            'encrypted_string': base64_encoded_data
        }
    )


@app.post('/rsa/decryptB64')
async def decrypt_string(string: Text):
    global current_user
    global users
    
    if current_user == 0:
        raise HTTPException(status_code=400, detail='Current User belum diatur')

    user = users[current_user]

    private_key = user.private_key

    output_file_name = user.file_name

    output_file_extension = user.file_extension

    # Private key merupakan private key current user

    if not string or string == '':
        raise HTTPException(status_code=400, detail='String bermasalah')
    
    if private_key.key_type == '':
        raise HTTPException(status_code=400, detail=f'User {current_user} belum memiliki kuci')
    
    if output_file_name == '' or output_file_extension == '':
        raise HTTPException(status_code=400, detail=f'User {current_user} belum memasukkan metadata file output')

    
    key_json = json.dumps({'key_type': private_key.key_type, 'exponent': private_key.exponent, 'modulus': private_key.modulus})

    string_decrypted = rsa_string_decrypt(string.input_text, key_json, 1) # string

    base64_encoded_data = base64.b64encode(string_decrypted.encode('latin1')).decode('latin1')

    return JSONResponse(
        content={
            'encrypted_string': base64_encoded_data
        }
    )

# @app.post('/rsa/string/encrypt')
# async def encrypt_file(string: str, key: Key, output_file_name: str, output_file_extension: str):

#     if not str or str == '':
#         raise HTTPException(400,detail='String bermasalah')
    
#     key_json = json.dumps({'key_type': key.key_type, 'exponent': key.exponent, 'modulus': key.modulus})

#     string_encrypted = rsa_string_encrypt(string, key_json, 4) # string

#     new_output_file_name = f'{output_file_name}.{output_file_extension}'

#     SAVE_FILE_PATH = os.path.join(UPLOAD_DIR, new_output_file_name)

#     with open(SAVE_FILE_PATH, "wb") as f:
#         f.write(string_encrypted.encode('latin1'))

#     return FileResponse(path=SAVE_FILE_PATH, media_type="application/octet-stream", filename=new_output_file_name)
    

# @app.post('/rsa/string/decrypt')
# async def encrypt_file(string: str, key: Key, output_file_name: str, output_file_extension: str):
    
#     if not str:
#         raise HTTPException(400,detail='String bermasalah')
    
#     key_json = json.dumps({'key_type': key.key_type, 'exponent': key.exponent, 'modulus': key.modulus})

#     string_decrypted = rsa_string_decrypt(string, key_json, 4) # string

#     new_output_file_name = f'{output_file_name}.{output_file_extension}'

#     SAVE_FILE_PATH = os.path.join(UPLOAD_DIR, new_output_file_name)

#     with open(SAVE_FILE_PATH, "wb") as f:
#         f.write(string_decrypted.encode('latin1'))

#     return FileResponse(path=SAVE_FILE_PATH, media_type="application/octet-stream", filename=new_output_file_name)
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=80)





