SELECT 
    A.codAutor, A.nome, COUNT(L.cod) AS quantidade_publicacoes
FROM 
    AUTOR A
JOIN 
    LIVRO L ON A.codAutor = L.autor
GROUP BY 
    A.codAutor, A.nome
ORDER BY 
    quantidade_publicacoes DESC
LIMIT 1;