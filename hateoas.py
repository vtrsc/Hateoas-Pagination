from datetime                         import datetime
from mmap import PAGESIZE
from typing                           import List
from requests import session
from sqlalchemy                       import text
from sqlalchemy.orm                   import Session
from fastapi                          import APIRouter, Query, status, Depends, HTTPException
from sqlalchemy.orm                   import Session
from sqlalchemy.future                import select
from core.deps                        import get_session, get_current_user
from models.processo_model import processoModel
from models.tramitacao_model          import tramitacaoModel
from models.ult_tramitacao_model      import ult_tramitacaoModel
from models.lista_model               import ListaModel
from schemas.dashboard_prateleira import dashboardPrateleiraSchemaBase
from schemas.dashboard_schema import dashboardSchemaBase
from schemas.eliminacao_schema import eliminacaoSchemaBase
from schemas.estante_schema import estanteSchemaBase
from schemas.hateoas_schema import hateoasSchemaBase
from schemas.lista_schema             import ListaSchemaBase
from schemas.localizarprocesso_schema import LocalizarProcessoSchemaBase,ProcessoSchemaUp
from fastapi.encoders import jsonable_encoder
from schemas.pro_arquivo_schema import proarquivoSchemaBase
from schemas.pro_temp_proc_schema import proTempProcSchemaBase
from schemas.processo_schema import processoSchemaBase

from schemas.prateleira_estante_schema import estante_prateleiraSchemaBase
from schemas.prateleira_schema import prateleiraSchemaBase
from schemas.temp_prateleira_schema import tempPrateleiraSchemaBase

router = APIRouter()


#Relatorio de Qtde de Processos no Arquivo Vs Qtde de Processos Arquivados (Num. Prateleira informada)

         

@router.get("/consultarTotal/",response_model=None)
def get_total_items(db: Session = Depends(get_session)) -> int:
    with db as session:
        query = text(f"""SELECT count(*) FROM PRO_RELACAO_A_ELIMINAR E""")
        result = session.execute(query).fetchone()
        return result[0] 



@router.get("/paginaçao")
def generate_pagination_links(page: int, db: Session = Depends(get_session)) -> dict:
    base_url = str('http://127.0.0.1:8000/api/relatorios/hateoas/?skip=1&limit=10')
    total_pages = (get_total_items(db) - 1) 
    links = {
        "self": f"{base_url}?page={page}",
    }
    if page > 1:
        links["prev"] = f"{base_url}?page={page - 1}"
    if page < total_pages:
        links["next"] = f"{base_url}?page={page + 1}"
    return links

@router.get("/hateoas/",response_model=List[processoSchemaBase])
def consultar_dados(skip: int = Query(default=0,description="Número de itens para pular", ge=0),
                    limit: int = Query(default=10,description="Número máximo de itens para retornar", le=100),
                    db: Session = Depends(get_session)):
    with db as session:
       
       '''if  skip == 2:
            skip = 11  # Altere o valor para 11 para pular 10 registros (considerando limit = 10)
       else:
         skip = (skip - 2) * limit + 11  
       
        
    query = text(f"""SELECT linha,processos
                           FROM (SELECT rownum AS linha,trim(E.processos) AS processos
                                 FROM PRO_RELACAO_A_ELIMINAR E) v
                           WHERE linha BETWEEN {skip} AND (({skip}+{limit}-1))
                           ORDER BY linha""")'''
       
    query = text(f"""SELECT * FROM
                     (
                       SELECT  v.*,rownum AS linha
                         FROM 
                         (
                            SELECT E.processos
                              FROM PRO_RELACAO_A_ELIMINAR E
                         ) v
                       WHERE rownum < (({skip} * {limit}) + 1)
                     )
                     WHERE linha >= ((({skip}-1) * {limit}) + 1)""")
        

    result : List[processoSchemaBase] = session.execute(query).fetchall()

    # Retorne os dados com a chave "result"
    return result#{"result": dados_paginados}
"""
SELECT linha,processos
                           FROM (SELECT rownum AS linha,E.processos
                                 FROM PRO_RELACAO_A_ELIMINAR E) v
                           WHERE linha BETWEEN {skip} AND (({skip}+{limit})-1)
                           ORDER BY linha
"""

"""

SELECT * FROM
(
    SELECT a.*, rownum r__
    FROM
    (
        SELECT * FROM ORDERS WHERE CustomerID LIKE 'A%'
        ORDER BY OrderDate DESC, ShippingDate DESC
    ) a
    WHERE rownum < ((pageNumber * pageSize) + 1 )
)
WHERE r__ >= (((pageNumber-1) * pageSize) + 1)
"""
