# Documentação do Desafio de Processamento de Vendas

## Preparação
1. **Download e preparação do arquivo `dados_de_vendas.csv`:**
	- Fazer o download do arquivo que contém informações sobre  as vendas; 
	- No Linux, criar um diretório chamado `ecommerce` e inserir o arquivo `dados_de_vendas.csv` nele.

    ```bash
    # Criar o diretório ecommerce
    mkdir -p ecommerce

    # Colocar o arquivo dados_de_vendas.csv no diretório ecommerce
    mv dados_de_vendas.csv ecommerce/
    ```
	- Criar o diretório 'vendas' dentro de 'ecommerce';
	- Navegar até o diretório 'ecommerce' e criar o diretório 'vendas'.

    ```bash
    cd ecommerce
    mkdir -p vendas
    ```

## Script `processamento_de_vendas.sh`
2. **Script**
	- O script `processamento_de_vendas.sh` realiza as seguintes tarefas:
	- Cria o diretório `vendas`.
	- Copia o arquivo `dados_de_vendas.csv` para o diretório `vendas`.
	- Cria um subdiretório `backup` dentro de `vendas`.
	- Faz uma cópia do arquivo `dados_de_vendas.csv` para o diretório `backup` com a data de execução no nome do arquivo.
	- Renomeia o arquivo no diretório `backup`.
	- Cria um arquivo `relatorio.txt` no diretório `backup` com informações sobre a execução e os dados de venda.
	- Comprime os arquivos `backup-dados-<yyyymmdd>.csv` e `dados_de_vendas.csv`.

## Conteúdo do script `processamento_de_vendas.sh`
3. **Conteúdo do Script**
    ```bash
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
    echo "Data do sistema operacional: $atual_data" > $relatorio
    echo "Data do primeiro registro de venda: $primeira_data" >> "$relatorio"
    echo "Data do último registro de venda: $ultima_data" >> "$relatorio"
    echo "Quantidade total de itens diferentes vendidos: $itens_total" >> "$relatorio"
    echo -e "\nPrimeiras 10 linhas do arquivo 'backup-dados-${data_atual}.csv':" >> "$relatorio"
    head -n 10 "$backup_dir/backup-dados-${data_atual}.csv" >> "$relatorio"

    gzip "$backup_dir/backup-dados-${data_atual}.csv"
    gzip "$dados_file"

    echo "Relatório gerado em $relatorio"
    '''

### Script `consolidador_de_processamento_de_vendas.sh`
4. **O Script tem a finalidade de consolidar todos os relatórios gerados pelo script `processamento_de_vendas.sh` em um único arquivo chamado `relatorio_final.txt`**
    '''bash                                          
    #!/bin/bash
    # Define o caminho para o diretorio de backups;

    base_dir=""/home/nave/Área de Trabalho/ecommerce"
    backup_dir="backup_dir="$base_dir/vendas/backup"

    # Se o diretório de backup nao existir, ele cria
    if [ ! -d "$backup_dir" ]; then
        echo "Diretório $backup_dir não encontrado... Criando o diretório."
	mkdir -p "$backup_dir"
    else
    	echo "Diretório $backup_dir encontrado."
    fi

    # Define o caminho para o arquivo de saída
    arquivo_saida="$backup_dir/relatorio_final.txt"

    # Cria ou limpa o arquivo de saída
    : > "$arquivo_saida"

    # Processa todos os arquivos de relatórios
    # faz um loop por todos os arq no diretório de backup que começam por 'relatorio' e t^rm a eextensão '.txt'
    for file in "$backup_dir"/relatorio*.txt; do
	if [ -f "$file" ]; then
	        echo "Processando $file" >> "$arquivo_saida"
		cat "$file" >> "$arquivo_saida"

    # Pra cada arquivo encontrado, o script adiciona uma linha indicando qual arquivo está sendo processado
    # Segue com o conteúdo do arquivo e adiciona duas quebras de linhas para separar o conteúdo dos relatorios
        	echo -e "\n\n" >> "$arquivo_saida"
    	else
        	echo "Arquivo $file não encontrado..." >> "$arquivo_saida"
	fi
    done
    # Após processar tudo o script exibe uma mensagem indicando que a consolidação foi concluída 
    # E informa onde o arquivo pode ser encontrado
    echo "Consolidação completa. Verifique o arquivo $arquivo_saida"
    '''
 
### Agendamento da Execução   
5. **Agendamento do script `processamento_de_vendas.sh`**
    - Para agendar a execução do script `processamento_de_vendas.sh` todos os dias de segunda a quinta às 15:27, siga os passos abaixo:

    ```bash
    crontab -e
    ```
    - Adicione a seguinte linha ao final do arquivo:

    ```bash
    27 15 * * 1-4 /home/nave/Área\ de\ Trabalho/ecommerce/processamento_de_vendas.sh
    ```

### Modificação dos Dados e Geração de Relatórios
6. **Modificação dos dados**
    - Manualmente, modifique os dados no arquivo `dados_de_vendas.csv` no diretório `ecommerce` uma vez por dia.
    - Certifique-se de que o script `processamento_de_vendas.sh` esteja corretamente agendado.

7. **Executar o script `consolidador_de_processamento_de_vendas.sh`**
    - Após pelo menos 3 execuções do script `processamento_de_vendas.sh`, execute manualmente o script `consolidador_de_processamento_de_vendas.sh`.

    ```bash
    ./consolidador_de_processamento_de_vendas.sh
    ```

### Entregáveis
8. **Entregáveis**
    - Todos os arquivos de `dados_de_vendas.csv` gerados (pode-se renomeá-los para commitar).
    - Todos os arquivos de scripts gerados.
    - Arquivo de evidências da execução contendo imagens/prints das execuções.
    - Arquivo escrito no formato markdown, contendo todos os passos para reexecução do desafio.
