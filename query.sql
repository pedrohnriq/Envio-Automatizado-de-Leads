SELECT
        R.NOME AS [REGIONAL],
        FR.NOME_FANTASIA AS [FRANQUIA],
        P.CPF,
        F.MATRICULA,
        P.NOME,
        CONVERT(VARCHAR, F.DT_FILIACAO, 103) AS [DT FILIACAO],
        F.CEP,
        UPPER(F.CIDADE) AS [CIDADE],
        UPPER(F.BAIRRO) AS [BAIRRO],
        F.ENDERECO,
        F.COMPLEMENTO,
        F.NUMERO,
        UPPER(F.UF) AS [UF],
        (SELECT TOP 1 G.NUMERO 
         FROM PESSOA_TELEFONE (NOLOCK) G 
         WHERE ID_TIPO_TELEFONE = 1 AND ID_PESSOA = P.ID_PESSOA 
         ORDER BY ID_PESSOA_TELEFONE DESC) AS [TELEFONE],
        (SELECT TOP 1 G.NUMERO 
         FROM PESSOA_TELEFONE (NOLOCK) G 
         WHERE ID_TIPO_TELEFONE = 2 AND ID_PESSOA = P.ID_PESSOA 
         ORDER BY ID_PESSOA_TELEFONE DESC) AS [CELULAR]
    FROM FILIADO_CASHBACK_ENERGIA FCE
    JOIN FILIADO F ON F.ID_FILIADO = FCE.ID_FILIADO
    JOIN PESSOA P ON P.ID_PESSOA = F.ID_PESSOA
    JOIN FRANQUIA FR ON FR.ID_FRANQUIA = F.ID_FRANQUIA
    JOIN REGIONAL R ON FR.ID_REGIONAL = R.ID_REGIONAL
    WHERE F.ID_FILIADO_PAI IS NULL
      AND FCE.DATA_CRIACAO BETWEEN '{data_inicio_str}' AND '{data_fim_str}'
      AND NOT EXISTS(
            SELECT 1
            FROM ASSINATURA_CONTRATO A
            left join DADOS_EDT d on a.ID_FILIADO = d.ID_FILIADO
            join filiado f on f.id_filiado = A.id_filiado
            join franquia fr on fr.id_franquia = f.ID_FRANQUIA
            WHERE a.DT_CRIACAO >= '2025-07-29 20:01:00'
            and a.ID_FILIADO = fce.id_filiado
            AND a.Status_EDT IN (4, 5, 6, 7, 8, 10, 98, 99)
            and fr.ID_FRANQUIA not in (426)    
        )
    ORDER BY 2