import os, sys, pathlib
import time
from pathlib import Path
import asyncio
import aiohttp
import zipfile
from tqdm.asyncio import tqdm



async def download_file(url, save_path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            total_size = int(response.headers.get('Content-Length', 0))
            with open(save_path, 'wb') as f:
                with tqdm(total=total_size, desc=str(save_path), unit='B', unit_scale=True) as pbar:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                        pbar.update(len(chunk))
    return save_path

async def download_emqx_server(root_path):
    print(f'system is {sys.platform}')
    if sys.platform == 'win32':
        pass
    else:
        raise NotImplementedError('only support windows now')

    download_url = r'https://packages.emqx.io/emqx-ce/v5.3.1/emqx-5.3.1-windows-amd64.zip'
    # download emqx server to root_path/emqx.zip
    emqx_zip_path = root_path.joinpath(Path(r'emqx.zip'))
    print(f'emqx zip path is {emqx_zip_path}')
    await download_file(download_url, emqx_zip_path)
    print('download emqx server success')
    # unzip emqx.zip to root_path/emqx
    emqx_path = root_path.joinpath(Path(r'emqx'))
    print(f'emqx path is {emqx_path}')
    with zipfile.ZipFile('emqx.zip', 'r') as zip_ref:
        zip_ref.extractall(emqx_path)


async def start_emqx_server(root_path):
    print(f'system is {sys.platform}')
    if sys.platform == 'win32':
        pass
    else:
        raise NotImplementedError('only support windows now')

    # download emqx server if not exists
    emqx_path = root_path.joinpath(Path(r'emqx\bin\emqx_ctl'))
    if os.path.exists(emqx_path):
        print(f'emqx path is {emqx_path}')
    else:
        await download_emqx_server(root_path)

    while not await check_emqx_server(root_path):
        print(f'starting emqx server')
        # if path not exists, create it
        emqx_path = root_path.joinpath(Path(r'emqx\bin\emqx'))
        if os.path.exists(emqx_path):
            print(f'emqx path is {emqx_path}')
        else:
            raise FileNotFoundError(f'emqx path {emqx_path} not exists')
        # start emqx by run "emqx\bin\emqx start"
        os.system(f"{emqx_path} start")
        print('emqx server started')
        await asyncio.sleep(3)


async def check_emqx_server(root_path):
    print(f'check emqx server')
    # if path not exists, create it
    emqx_path = root_path.joinpath(Path(r'emqx\bin\emqx_ctl'))
    if os.path.exists(emqx_path):
        print(f'emqx path is {emqx_path}')
    else:
        raise FileNotFoundError(f'emqx path {emqx_path} not exists')
    # 检测emqx是否正在运行
    # run "emqx\bin\emqx status" and get the result
    result = os.popen(f"{emqx_path} status").read()
    print(f'emqx status is {result}')
    if 'is starting' in result:
        await asyncio.sleep(3)
        return await check_emqx_server(root_path)
    if 'is started' in result:
        print('emqx server is running')
        return True
    else:
        print('emqx server is not running')
        return False

