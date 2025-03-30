from domain.repositories.i_bovespa_data_repository import ISegmentoRepository
from infrastructure.database.db_connection import get_db_connection
from typing import List

class PyODBCSegmentoRepository(ISegmentoRepository):
    def create_segmentos_economicos(self, segmentos: List[any]):
            conn = get_db_connection()
            cursor = conn.cursor()            
            try:
                # Desativar fast_executemany para OUTPUT funcionar
                cursor.fast_executemany = False
                
                # Lista para armazenar os IDs inseridos
                inserted_ids = []
                
                for segmento in segmentos:
                    cursor.execute(
                        """
                        INSERT INTO dbo.SegmentoClassificacao (Sigla, Descritivo)
                        OUTPUT INSERTED.ID
                        VALUES (?, ?)
                        """,
                        segmento['sigla'], segmento['descritivo']
                    )
                    row = cursor.fetchone()
                    inserted_ids.append(row.ID)
                
                conn.commit()
                
                # Atualizar os dicionários com os IDs
                for i, segmento in enumerate(segmentos):
                    segmento['id'] = inserted_ids[i]
                
                return segmentos
                
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
                conn.close()
    
    def get_segmentos_economicos(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT ID, Sigla, Descritivo FROM dbo.SegmentoClassificacao")
            segmentos = []
            
            for row in cursor.fetchall():
                segmento = {
                    "id": row.ID,
                    "sigla": row.Sigla,
                    "descritivo": row.Descritivo
                }                
                segmentos.append(segmento)
            
            return segmentos
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def create_sub_setor(self, sub_setores: List[any]):
        conn = get_db_connection()
        cursor = conn.cursor()            
        try:
            # Desativar fast_executemany para OUTPUT funcionar
            cursor.fast_executemany = False
            
            # Lista para armazenar os IDs inseridos
            inserted_ids = []
            
            for sub_setor in sub_setores:
                cursor.execute(
                    """
                    INSERT INTO dbo.Subsetor (Descritivo)
                    OUTPUT INSERTED.ID
                    VALUES (?)
                    """,
                    sub_setor['descritivo']
                )
                row = cursor.fetchone()
                inserted_ids.append(row.ID)
            
            conn.commit()
            
            # Atualizar os dicionários com os IDs
            for i, sub_setor in enumerate(sub_setores):
                sub_setor['id'] = inserted_ids[i]
            
            return sub_setor
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_subsetores(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT ID, Descritivo FROM dbo.Subsetor")
            subsetores = []
            
            for row in cursor.fetchall():
                subsetor = {
                    "id": row.ID,                    
                    "descritivo": row.Descritivo
                }                
                subsetores.append(subsetor)
            
            return subsetores
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def create_setor_economico(self, setor_economico: List[any]):
        conn = get_db_connection()
        cursor = conn.cursor()            
        try:
            # Desativar fast_executemany para OUTPUT funcionar
            cursor.fast_executemany = False
            
            # Lista para armazenar os IDs inseridos
            inserted_ids = []
            
            for setor in setor_economico:
                cursor.execute(
                    """
                    INSERT INTO dbo.SetorEconomico (Descritivo)
                    OUTPUT INSERTED.ID
                    VALUES (?)
                    """,
                    setor['descritivo']
                )
                row = cursor.fetchone()
                inserted_ids.append(row.ID)
            
            conn.commit()
            
            # Atualizar os dicionários com os IDs
            for i, setor in enumerate(setor_economico):
                setor['id'] = inserted_ids[i]
            
            return setor
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_setores(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT ID, Descritivo FROM dbo.SetorEconomico")
            setores = []
            
            for row in cursor.fetchall():
                subsetor = {
                    "id": row.ID,                    
                    "descritivo": row.Descritivo
                }                
                setores.append(subsetor)
            
            return setores
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def create_segmentos(self, segmentos: List[any]):
        conn = get_db_connection()
        cursor = conn.cursor()            
        try:
            # Desativar fast_executemany para OUTPUT funcionar
            cursor.fast_executemany = False
            
            # Lista para armazenar os IDs inseridos
            inserted_ids = []
            
            for segmento in segmentos:
                cursor.execute(
                    """
                    INSERT INTO dbo.Segmento (Descritivo)
                    OUTPUT INSERTED.ID
                    VALUES (?)
                    """,
                    segmento['descritivo']
                )
                row = cursor.fetchone()
                inserted_ids.append(row.ID)
            
            conn.commit()
            
            # Atualizar os dicionários com os IDs
            for i, segmento in enumerate(segmentos):
                segmento['id'] = inserted_ids[i]
            
            return segmentos
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_segmentos(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT ID, Descritivo FROM dbo.Segmento")
            setores = []
            
            for row in cursor.fetchall():
                subsetor = {
                    "id": row.ID,                    
                    "descritivo": row.Descritivo
                }                
                setores.append(subsetor)
            
            return setores
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_segmento_classificacao_id_by_sigla(self, sigla: str):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT ID FROM dbo.SegmentoClassificacao WHERE Sigla = ?",
                sigla
            )
            row = cursor.fetchone()
            return row[0] if row else None
        finally:
            cursor.close()
            conn.close()

    def get_setor_economico_id_by_descritivo(self, descritivo: str):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT ID FROM dbo.SetorEconomico WHERE Descritivo = ?",
                descritivo
            )
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Setor Econômico não encontrado: {descritivo}")
            return row[0]
        finally:
            cursor.close()
            conn.close()

    def get_subsetor_id_by_descritivo(self, descritivo: str):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT ID FROM dbo.Subsetor WHERE Descritivo = ?",
                descritivo
            )
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Subsetor não encontrado: {descritivo}")
            return row[0]
        finally:
            cursor.close()
            conn.close()

    def get_segmento_id_by_descritivo(self, descritivo: str):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT ID FROM dbo.Segmento WHERE Descritivo = ?",
                descritivo
            )
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Segmento não encontrado: {descritivo}")
            return row[0]
        finally:
            cursor.close()
            conn.close()

    def create_empresas(self, empresas: List[any]):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Inserir empresas e obter IDs
            inserted_empresas = []
            for empresa in empresas:                
                cursor.execute(
                    """
                    INSERT INTO dbo.Empresa 
                    (Nome, Codigo, SegmentoClassificacaoID, SetorEconomicoID, SubsetorID, SegmentoID)
                    OUTPUT INSERTED.ID, INSERTED.Nome, INSERTED.Codigo, 
                           INSERTED.SegmentoClassificacaoID, INSERTED.SetorEconomicoID, 
                           INSERTED.SubsetorID, INSERTED.SegmentoID
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    empresa['nome'], empresa['codigo'], empresa['segmento_classificacao_id'],
                    empresa['setor_economico_id'], empresa['subsetor_id'], empresa['segmento_id']
                )                
                row = cursor.fetchone()                
                empresa_inserida = {
                    "id":row.ID,
                    "nome":row.Nome,
                    "codigo":row.Codigo,
                    "segmento_classificacao_id":row.SegmentoClassificacaoID,
                    "setor_economico_id":row.SetorEconomicoID,
                    "subsetor_id":row.SubsetorID,
                    "segmento_id":row.SegmentoID
                }                
                inserted_empresas.append(empresa_inserida)                
            conn.commit()
            return inserted_empresas
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_empresa_by_codigo(self, codigo: str):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = """
            SELECT 
                e.ID, e.Nome, e.Codigo,
                sc.ID as SegmentoClassificacaoID, sc.Sigla as SegmentoClassificacaoSigla, sc.Descritivo as SegmentoClassificacaoDesc,
                se.ID as SetorEconomicoID, se.Descritivo as SetorEconomicoDesc,
                ss.ID as SubsetorID, ss.Descritivo as SubsetorDesc,
                s.ID as SegmentoID, s.Descritivo as SegmentoDesc
            FROM dbo.Empresa e
            LEFT JOIN dbo.SegmentoClassificacao sc ON e.SegmentoClassificacaoID = sc.ID
            INNER JOIN dbo.SetorEconomico se ON e.SetorEconomicoID = se.ID
            INNER JOIN dbo.Subsetor ss ON e.SubsetorID = ss.ID
            INNER JOIN dbo.Segmento s ON e.SegmentoID = s.ID
            WHERE e.Codigo = ?
            """
            
            cursor.execute(query, codigo)
            row = cursor.fetchone()
            
            if not row:
                return None
                
            empresa = {
                "id": row.ID,
                "nome": row.Nome,
                "codigo": row.Codigo,
                "segmento_classificacao": {
                    "id": row.SegmentoClassificacaoID,
                    "sigla": row.SegmentoClassificacaoSigla,
                    "descritivo": row.SegmentoClassificacaoDesc
                } if row.SegmentoClassificacaoID else None,
                "setor_economico": {
                    "id": row.SetorEconomicoID,
                    "descritivo": row.SetorEconomicoDesc
                },
                "subsetor": {
                    "id": row.SubsetorID,
                    "descritivo": row.SubsetorDesc
                },
                "segmento": {
                    "id": row.SegmentoID,
                    "descritivo": row.SegmentoDesc
                }
            }
            
            return empresa
        finally:
            cursor.close()
            conn.close()