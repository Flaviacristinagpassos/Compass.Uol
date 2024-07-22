#!/bin/bash
# Caminho absoluto para o diretório de backup
base_dir="/home/nave/Área de Trabalho/ecommerce"
backup_dir="$base_dir/vendas/backup"
dados_file="$base_dir/vendas/dados_de_vendas.csv"

mkdir -p "$backup_dir"

data_atual=$(date +%Y%m%d)

cp "$dados_file" "$backup_dir/dados-${data_atual}.csv"
if [ $? -ne 0 ]; then
    echo "Erro ao copiar o arquivo de dados..."
    exit 1
fi

mv "$backup_dir/dados-${data_atual}.csv" "$backup_dir/backup-dados-${data_atual}.csv"
if [ $? -ne 0 ]; then
    echo "Erro ao mover o arquivo de dados..."
    exit 1
fi

atual_data=$(date +"%Y/%m/%d %H:%M")

primeira_data=$(head -n 2 "$dados_file" | tail -n 1 | cut -d ',' -f 5)
ultima_data=$(tail -n 1 "$dados_file" | cut -d ',' -f 5)

itens_total=$(cut -d ',' -f 3 "$dados_file" | tail -n +2 | awk '{sum += $1} END {print sum}')

relatorio="$backup_dir/relatorio.txt"

# Gera o relatório
echo "Data do sistema operacional: $atual_data" > "$relatorio"
echo "Data do primeiro registro de venda: $primeira_data" >> "$relatorio"
echo "Data do último registro de venda: $ultima_data" >> "$relatorio"
echo "Quantidade total de itens diferentes vendidos: $itens_total" >> "$relatorio"
echo -e "\nPrimeiras 10 linhas do arquivo 'backup-dados-${data_atual}.csv':" >> "$relatorio"
head -n 10 "$backup_dir/backup-dados-${data_atual}.csv" >> "$relatorio"

gzip "$backup_dir/backup-dados-${data_atual}.csv"
gzip "$dados_file"

echo "Relatório gerado em $relatorio"
