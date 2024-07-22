#!/bin/bash

# Caminho absoluto para o diretório de backup
base_dir="/home/nave/Área de Trabalho/ecommerce"
backup_dir="$base_dir/vendas/backup"

# Se o diretório de backup nao existir, ele cria
if [ ! -d "$backup_dir" ]; then
    echo "Diretório $backup_dir não encontrado... Criando o diretório."
    mkdir -p "$backup_dir"
else
    echo "Diretório $backup_dir encontrado."
fi

arquivo_saida="$backup_dir/relatorio_final.txt"

: > "$arquivo_saida"

for file in "$backup_dir"/relatorio*.txt; do
    if [ -f "$file" ]; then
        echo "Processando $file" >> "$arquivo_saida"
        cat "$file" >> "$arquivo_saida"
        echo -e "\n\n" >> "$arquivo_saida"
    else
        echo "Arquivo $file não encontrado..." >> "$arquivo_saida"
    fi
done

echo "Consolidação completa. Verifique o arquivo $arquivo_saida"
