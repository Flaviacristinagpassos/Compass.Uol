SELECT 
    v.cdvdd, 
    v.nmvdd
FROM 
    TBVENDEDOR v
JOIN 
    TBVENDAS ven ON v.cdvdd = ven.cdvdd
GROUP BY 
    v.cdvdd, 
    v.nmvdd
ORDER BY 
    COUNT(ven.cdven) DESC  
LIMIT 1;
