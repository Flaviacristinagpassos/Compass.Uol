SELECT 
    ven.cdpro, 
    ven.nmpro
FROM 
    TBVENDAS ven
WHERE 
    ven.dtven BETWEEN '2014-02-03' AND '2018-02-02'
GROUP BY 
    ven.cdpro, 
    ven.nmpro
ORDER BY 
    COUNT(ven.cdven) DESC
LIMIT 1;