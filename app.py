#!/usr/bin/env python3

from __future__ import annotations

import asyncio
from io import BytesIO
from typing import Literal

from fastapi import FastAPI, Response, UploadFile, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image, ImageFilter, ImageOps

app = FastAPI()
# this serves the HTML and JS from the frontend directory
# styling is almost non-existent
# this UX is awful
# i spent zero time on it
# make changes as needed.
static = StaticFiles(directory='frontend')


def scramble(io: BytesIO) -> bytes:
    ret = BytesIO()
    with Image.open(io) as im:
        im = im.filter(ImageFilter.GaussianBlur(5))
        im = ImageOps.invert(im)
        im.save(ret, format='png')
    ret.seek(0)
    return ret.read()


@app.post('/upload')
async def upload_file(file: UploadFile, proto: Literal['http', 'https']) -> JSONResponse:
    """handles a file upload.

    whether or not the file is an image is not checked.
    couldn't be bothered. if this is needed, i'll do it later.

    all this does is store, *globally*, the protocol and the file contents.
    """
    if not file.filename:
        return JSONResponse({'error': 'No filename found'}, status_code=status.HTTP_400_BAD_REQUEST)
    app.state.plaintext = await file.read()
    app.state.content_type = file.content_type
    app.state.proto = proto
    return JSONResponse({'filename': file.filename})


@app.get('/attack')
async def try_get_data() -> Response:
    """The hack thing.

    If the saved proto is http, return the plaintext.
    If it's https, return a random string.
    """
    if not hasattr(app.state, 'plaintext') or not hasattr(app.state, 'proto'):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    if app.state.proto == 'http':
        return Response(status_code=status.HTTP_200_OK, content=app.state.plaintext, media_type=app.state.content_type)
    else:
        return Response(
            status_code=status.HTTP_201_CREATED,
            content=await asyncio.to_thread(scramble, BytesIO(app.state.plaintext)),
            media_type='image/png',
        )


@app.get('/')
async def redir_to_index() -> Response:
    """Redirects / to /index.html"""
    return Response(status_code=status.HTTP_302_FOUND, headers={'Location': '/index.html'})


# i'm not sure if order matters here, but anyway, keep this at the bottom.

app.mount('/', static, name='static')

# this makes it so `python app.py` works.
if __name__ == '__main__':
    import uvicorn

    try:
        uvicorn.run(app, host='0.0.0.0', port=3000)
    except KeyboardInterrupt:
        pass
