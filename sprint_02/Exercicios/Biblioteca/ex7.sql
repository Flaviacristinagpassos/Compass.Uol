SELECT 
    A.nome
FROM 
    AUTOR A
LEFT JOIN 
    LIVRO L ON A.codAutor = L.autor
WHERE 
    L.cod is NULL
ORDER BY 
    A.nome ASC;