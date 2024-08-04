WITH Vendedor_Menor_Venda AS (
    SELECT 
        v.cdvdd
    FROM 
        TBVENDEDOR v
    JOIN 
        TBVENDAS ven ON v.cdvdd = ven.cdvdd
    WHERE 
        ven.status = 'Concluído'
    GROUP BY 
        v.cdvdd
    HAVING 
        SUM(ven.qtd * ven.vrunt) > 0
    ORDER BY 
        SUM(ven.qtd * ven.vrunt) ASC
    LIMIT 
        1
),
-- dependentes do vendedor identificado
Dependentes_Vendedor AS (
    SELECT 
        d.cddep,
        d.nmdep,
        d.dtnasc,
        SUM(ven.qtd * ven.vrunt) AS valor_total_vendas
    FROM 
        TBDEPENDENTE d
    JOIN 
        TBVENDEDOR v ON d.cdvdd = v.cdvdd
    JOIN 
        TBVENDAS ven ON v.cdvdd = ven.cdvdd
    WHERE 
        v.cdvdd IN (SELECT cdvdd FROM Vendedor_Menor_Venda)
        AND ven.status = 'Concluído'
    GROUP BY 
        d.cddep, d.nmdep, d.dtnasc
)
-- dados dos dependentes
SELECT 
    cddep,
    nmdep,
    dtnasc,
    valor_total_vendas
FROM 
    Dependentes_Vendedor;
