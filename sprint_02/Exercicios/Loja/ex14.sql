SELECT 
    estado,
    CAST(ROUND(SUM(qtd * vrunt) * 1.0 / COUNT(*), 2) AS DECIMAL(10, 2)) AS gastomedio
FROM 
    TBVENDAS
WHERE 
    status = 'Concluído'
GROUP BY 
    estado
ORDER BY 
    gastomedio DESC;
