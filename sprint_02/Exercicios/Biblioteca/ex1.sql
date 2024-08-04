SELECT
    L.cod, L.titulo, L.autor, L.editora, L.valor, L.publicacao, L.edicao, L.idioma
FROM
    livro L
WHERE 
    L.publicacao > '2014-12-31'
ORDER BY
    L.cod asc;

