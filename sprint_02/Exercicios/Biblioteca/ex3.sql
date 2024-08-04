SELECT
    count(l.cod) AS quantidade,
    E.nome,
    EN.estado,
    EN.cidade
FROM
    livro L
JOIN
    editora E ON L.editora = E.codEditora
JOIN
    endereco EN ON E.endereco = EN.codEndereco
GROUP BY
    E.nome, EN.estado, EN.cidade
ORDER BY
     quantidade DESC
LIMIT
    5;
