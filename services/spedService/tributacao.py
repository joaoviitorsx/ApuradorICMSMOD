import time
from db.conexao import conectar_banco, fechar_banco

async def criar_e_preencher_c170nova(empresa_id):
    print(f"[INÍCIO] Preenchendo c170nova para empresa_id={empresa_id}...")
    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        tempo_inicio = time.time()

        cursor.execute("""
            INSERT IGNORE INTO c170nova (
                cod_item, periodo, reg, num_item, descr_compl, qtd, unid, 
                vl_item, vl_desc, cfop, cst, id_c100, filial, ind_oper, 
                cod_part, num_doc, chv_nfe, empresa_id, cod_ncm
            )
            SELECT DISTINCT
                c.cod_item, 
                c.periodo, 
                c.reg, 
                c.num_item, 
                COALESCE(o.descr_item, c.descr_compl), 
                c.qtd, 
                c.unid, 
                c.vl_item, 
                c.vl_desc, 
                c.cfop, 
                c.cst_icms, 
                c.id_c100, 
                c.filial, 
                c.ind_oper, 
                cc.cod_part, 
                cc.num_doc, 
                cc.chv_nfe, 
                c.empresa_id,
                o.cod_ncm
            FROM c170 c
            JOIN c100 cc 
                ON cc.id = c.id_c100
            JOIN cadastro_fornecedores f
                ON cc.cod_part = f.cod_part
                AND f.decreto = 'Não' AND f.uf = 'CE' AND f.empresa_id = %s
            LEFT JOIN `0200` o
                ON c.cod_item = o.cod_item
                AND o.empresa_id = c.empresa_id
            LEFT JOIN c170nova n 
                ON n.cod_item = c.cod_item 
                AND n.id_c100 = c.id_c100 
                AND n.empresa_id = c.empresa_id
            WHERE c.empresa_id = %s
            AND c.cfop IN ('1101', '1401', '1102', '1403', '1910', '1116')
            AND n.cod_item IS NULL
        """, (empresa_id, empresa_id))

        total = cursor.rowcount
        conexao.commit()
        print(f"[OK] {total} registros inseridos em c170nova.")
        print(f"[TEMPO] Inserção concluída em {time.time() - tempo_inicio:.2f}s")

    except Exception as e:
        print(f"[ERRO] Falha em criar_e_preencher_c170nova: {e}")
        conexao.rollback()

    finally:
        cursor.close()
        fechar_banco(conexao)
        print("[FIM] Finalização de c170nova.")


