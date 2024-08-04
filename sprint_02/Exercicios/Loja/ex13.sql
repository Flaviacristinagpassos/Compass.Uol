SELECT 
    ven.cdpro,
    ven.nmcanalvendas,
    ven.nmpro,
    SUM(ven.qtd) AS quantidade_vendas
FROM 
    TBVENDAS ven
WHERE 
    ven.status = 'Concluído'
    AND ven.nmcanalvendas IN ('Ecommerce', 'Matriz')
GROUP BY 
    ven.cdpro, ven.nmcanalvendas, ven.nmpro
ORDER BY 
    quantidade_vendas ASC
LIMIT 
    10;