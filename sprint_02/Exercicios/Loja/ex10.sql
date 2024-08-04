SELECT 
    v.nmvdd AS vendedor,
    SUM(ven.qtd * ven.vrunt) AS valor_total_vendas,
    ROUND(SUM(ven.qtd * ven.vrunt) * v.perccomissao/100, 2) AS comissao
FROM 
    TBVENDEDOR v
JOIN 
    TBVENDAS ven ON v.cdvdd = ven.cdvdd
WHERE
    ven.status = 'Concluído'
GROUP BY 
    v.nmvdd, v.perccomissao
ORDER BY 
    comissao DESC;