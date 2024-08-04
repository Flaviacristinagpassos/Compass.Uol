SELECT DISTINCT 
    A.nome
FROM 
    AUTOR A
JOIN 
    LIVRO L ON A.codAutor = L.autor
JOIN 
    EDITORA E ON L.editora = E.codEditora
JOIN 
    ENDERECO EN ON E.endereco = EN.codEndereco
WHERE 
    EN.estado NOT IN ('PARANÁ', 'SANTA CATARINA', 'RIO GRANDE DO SUL')
ORDER BY 
    A.nome;
