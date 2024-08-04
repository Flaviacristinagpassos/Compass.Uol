SELECT 
    A.codAutor, A.nome, A.nascimento, count(L.cod) AS quantidade
FROM 
    autor A
LEFT JOIN 
    livro L ON A.codAutor = L.autor
GROUP BY 
    A.codAutor, A.nome, A.nascimento
ORDER BY 
    A.nome ASC;