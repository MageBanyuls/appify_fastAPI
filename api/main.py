# main.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from typing import List
from utils import peticion_get, peticion_post, peticion_get_pdf, peticion_get_rifa
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Configuración del CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://appify-fas-api.vercel.app/",

]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Configuración del CORS para permitir todos los orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class IdDoc(BaseModel):
    TipoDTE: int
    FchEmis: str
    Folio: int

class Emisor(BaseModel):
    RUTEmisor: str

class Receptor(BaseModel):
    RUTRecep: str
    RznSocRecep: str
    GiroRecep: str
    Contacto: str
    CorreoRecep: str
    DirRecep: str
    CmnaRecep: str

class DetalleItem(BaseModel):
    NmbItem: str
    QtyItem: int
    PrcItem: int

class ReferenciaItem(BaseModel):
    TpoDocRef: str
    RazonRef: str
    FolioRef: int

class Encabezado(BaseModel):
    IdDoc: IdDoc
    Emisor: Emisor
    Receptor: Receptor

class DteTemporalData(BaseModel):
    Encabezado: Encabezado
    Detalle: List[DetalleItem]
    #Referencia:List[ReferenciaItem]

class DteRealData(BaseModel):
    codigo: str
    dte: int
    emisor: int
    receptor: int


@app.post("/dte-temporal", tags=["Emisión de Documentos"])
async def dte_temporal(request: Request, dte_data: DteTemporalData):
    """
    Emite un documento temporal.

    Parámetros:
    - dte_data: Datos del documento temporal a emitir.
    """
    datos = await request.json()
    url = "https://libredte.cl/api/dte/documentos/emitir?normalizar=1&formato=json&links=0&email=0"
    return peticion_post(datos, url)

@app.post("/dte-real", tags=["Emisión de Documentos"])
async def dte_real(request: Request, dte_data :DteRealData):
    """
    Emite un documento real.

    Parámetros:
    - dte_data: Datos del documento real a emitir.
    """
    datos = await request.json()
    url = "https://libredte.cl/api/dte/documentos/generar?getXML=0&links=0&email=0&retry=1&gzip=0"
    return peticion_post(datos, url)

@app.get("/dte_tmps/info", tags=["Documentos Temporales"])
async def info_tmps(codigo: str, dte: str, emisor: str, receptor: str):
    """
    Obtiene la informacion de un DTE temporal.

    """
    url = f"https://libredte.cl/api/dte/dte_tmps/info/{receptor}/{dte}/{codigo}/{emisor}?getDetalle=0&getDatosDte=0&getEmailEnviados=0&getLinks=0&getReceptor=0&getSucursal=0&getUsuario=0"
    return peticion_get(url)

@app.get("/dte_tmps/pdf", tags=["Documentos Temporales"])
async def pdf_tmps(codigo: str, dte: str, emisor: str, receptor: str):
    """
    
    Obtiene el PDF de un DTE temporal.

    """
    url = f"https://libredte.cl/api/dte/dte_tmps/pdf/{receptor}/{dte}/{codigo}/{emisor}?cotizacion=0&formato=general&papelContinuo=0&compress=0"
    return peticion_get_pdf(url)

@app.get("/dte_tmps/xml", tags=["Documentos Temporales"])
async def xml_tmps(codigo: str, dte: str, emisor: str, receptor: str):
    """
    Obtiene el XML de un DTE temporal.

    """
    url = f"https://libredte.cl/api/dte/dte_tmps/xml/{receptor}/{dte}/{codigo}/{emisor}"
    return peticion_get(url)

@app.get("/dte_tmps/eliminar", tags=["Documentos Temporales"])
async def eliminar_tmps(codigo: str, dte: str, emisor: str, receptor: str):
    """

    Elimina los datos de un DTE temporal
    
    """
    url = f"https://libredte.cl/api/dte/dte_tmps/eliminar/{receptor}/{dte}/{codigo}/{emisor}"
    return peticion_get(url)

@app.get("/dte_emitidos/info", tags=["Documentos Emitidos"])
async def info_emitidos(dte: str, emisor: str, folio: str):
    """
    Obtiene la informacion de un DTE real.

    """
    url = f"https://libredte.cl/api/dte/dte_emitidos/info/{dte}/{folio}/{emisor}"
    return peticion_get(url)

@app.get("/dte_emitidos/pdf", tags=["Documentos Emitidos"])
async def pdf_emitidos(dte: str, emisor: str, folio: str):
    """
    
    Obtiene el PDF de un DTE real.

    """
    url = f"https://libredte.cl/api/dte/dte_emitidos/pdf/{dte}/{folio}/{emisor}"
    return peticion_get_pdf(url)

@app.get("/dte_emitidos/xml", tags=["Documentos Emitidos"])
async def xml_emitidos(dte: str, emisor: str, folio: str):
    """

    Obtiene el XML de un DTE real.

    """
    url = f"https://libredte.cl/api/dte/dte_emitidos/xml/{dte}/{folio}/{emisor}"
    return peticion_get(url)

@app.get("/dte_emitidos/actualizarestado", tags=["Documentos Emitidos"])
async def actualizar_estado(tipo: str, folio: str, emisor: str):
    """

    Actualiza el estado de un DTE real.

    """
    url = f"https://libredte.cl/api/dte/dte_emitidos/actualizar_estado/{tipo}/{folio}/{emisor}?usarWebservice=1"
    return peticion_get(url)

@app.get("/dte_emitidos/eliminar", tags=["Documentos Emitidos"])
async def eliminar_dte_emitido(tipo: str, folio: str, emisor: str):
    """
    
    Recurso que permite eliminar un DTE emitido y enviado al SII que se encuentra en estado rechazado, o bien un DTE que fue emitido pero no se pudo enviar al SII y no se desea enviar.

    """
    url = f"https://libredte.cl/api/dte/dte_emitidos/eliminar/{tipo}/{folio}/{emisor}"
    return peticion_get(url)

@app.get("/")
async def home():

    return {"Estoy": "Desplegado"}



@app.get("/actualizar/rifa/db", tags=["Documentos Emitidos"])
async def eliminar_dte_emitido(offset: int):
    """
    
    Api para interactuar con MP

    """
    url = f"https://api.mercadopago.com/preapproval/search?limit=100&offset={offset}"
    return peticion_get_rifa(url)


























































































































































































@app.get("/dte_folios/info", tags=["Folios"])
async def info_folios(dte: int, emisor: str):
    """

    Obtener informacion de un folio.

    """
    url = f"https://libredte.cl/api/dte/admin/dte_folios/info/{dte}/{emisor}"
    return peticion_get(url)


@app.get("/dte_folios/estado", tags=["Folios"])
async def estado_folios(dte: int, folio :int, emisor: str):
    """

    Obtener el estado de un folio en el SII.

    """
    url = f"https://libredte.cl/api/dte/admin/dte_folios/estado/{dte}/{folio}/{emisor}?formato=json"
    return peticion_get(url)

@app.get("/dte_folios/anular", tags=["Folios"])
async def anular_folio(dte: int, folio :int, emisor: str):
    """

    Obtener el estado de un folio en el SII.

    """
    url = f"https://libredte.cl/api/dte/admin/dte_folios/anular/{dte}/{folio}/{emisor}?formato=json"
    return peticion_get(url)
