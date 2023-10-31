import csv
import html

def read_csv_file(filename, delimitador, codificacao):
    with open(filename, 'r', encoding=codificacao) as f:
        reader = csv.reader(f, delimiter=delimitador)
        rows = []
        for row in reader:
            rows.append(row)
    return rows


def inicia_html_file(filename, familia_fonte, padrao_de_cores):
    with open(filename, 'w', encoding="utf-8") as f:
        f.write("""<!doctype html>
<html lang="pt-br"><head>
<meta charset="UTF-8">
<style>
body {
  -webkit-print-color-adjust: exact !important;
  padding:2em;
  background-color: """)
        f.write(padrao_de_cores[0] + ";\n")
        f.write("""}
* { 
	color-adjust: exact;
	-webkit-print-color-adjust: exact;
	print-color-adjust: exact;\n""")
        f.write("   font-family: " + familia_fonte + ";\n")
        f.write("""}
@media print {
  table tr {
    break-inside: avoid;
  }
}
table.tabela_01 {
  border:1px solid black;
  background-color: """)
        f.write("white;\n")
        f.write("""}
table.tabela_01 th, table.tabela_01 td {
  padding:0.8em;
}\n""")


def escreve_padrao_de_cores_para_linhas_de_tabelas(filename,tupla_de_cores):
	# O primeiro elemento é a cor de fundo para a página
	# O segundo elemento é a cor de destaque para cabecalhos
	# Todos os elementos restantes são cores alternadas, supostamente bem claras, para linhas contrastantes
	# Esta função não implementa a cor de fundo da página, que é tratada em outra função
    with open(filename, 'a', encoding="utf-8") as f:
        if len(tupla_de_cores) > 1:
            f.write("table.tabela_01 tr.cabecalho {\n")
            f.write("  background-color: "+ tupla_de_cores[1] +";\n")
            f.write("}\n")
        if len(tupla_de_cores) == 3:
            # Nesta situação não há cores contrastantes para as linhas de tabelas; o terceiro parâmetro se aplica para todas as linhas
            f.write("tr { background-color: " + tupla_de_cores[2] + "; border: 0; }\n")
        if len(tupla_de_cores) > 3:
            number_of_colors = str(len(tupla_de_cores) - 2) # Número de cores contrastantes para as linhas da tabela (como caracteres)
            contador = 0 # Precisamos contar as linhas de especificacao de cor (começando por zero)
            for cor in tupla_de_cores[2:]:
                f.write("tr:nth-child(" + number_of_colors + "n")
                if contador > 0:
                    f.write("+" + str(contador))
                f.write(") { background-color: " + tupla_de_cores[contador + 2] + "; border: 0; }\n")
                contador += 1
        f.write("th { border: 2px solid black; }\n")
        f.write("td { border: 1px solid black; }\n")

def escreve_codigo_contador_de_linhas(filename):
    with open(filename, 'a', encoding="utf-8") as f:
        f.write("""/*
	Contador de linhas
*/
table tbody {
	counter-reset: cnt;
}
table tbody tr th.cnt::before {
	counter-increment: cnt;
	content: counter(cnt)".";
}
tbody td.cnt::before {
	counter-increment: cnt;
	content: counter(cnt)".";
}
</style>\n""")

def insere_texto_abertura(h1, p, filename):
    html_string = "<h1>" + h1 + "</h1>\n"
    html_string += "<p>" + p + "</p>\n"
    with open(filename, 'a', encoding="utf-8") as f:
        f.write(html_string)


def create_html_table(rows, numeracao):
    html_string = '<table class="tabela_01">\n<thead>\n<tr class="cabecalho">\n'
    if numeracao:
        html_string += '<th>#</th>'
    for header in rows[0]:
        html_string += f'<th>{header}</th>\n'
    html_string += '</tr>\n</thead>\n<tbody>\n'

    for row in rows[1:]:
        html_string += '<tr>'
        if numeracao:
            html_string += '<th class="cnt"></th>'
        for field in row:
            html_string += f'<td>{html.escape(field)}</td>\n'
        html_string += '</tr>\n'

    html_string += '</tbody>\n</table>'
    return html_string


def write_html_file(html_string, filename):
    with open(filename, 'a', encoding="utf-8") as f:
        f.write(html_string)


def pede_codificacao_entrada():
    resposta = '0'
    while (resposta != '1') and (resposta != '2'):
        x = input(
            'Digite "1" para codificação UTF-8, ou "2" para codificação ANSI (Windows-1252): ')
        resposta = x[0]
    if x == "2":
        return "cp1252"
    else:
        return "utf-8"


def fecha_codigo_html(filename, codificacao):
    with open(filename, "a", encoding="utf-8") as f:
        f.write('<p style="font-size:x-small">Tabela criada a partir de arquivo CSV.')
        f.write(' O programa utilizado está disponível e documentado em <a href="https://github.com/epistemologia/csv-to-html/" target="_blank">')
        f.write('https://github.com/epistemologia/csv-to-html/upload/main</a>; o uso é livre, inclusive para fins comerciais.  Não é preciso preservar esta linha de crédito autoral.</p>\n<hr>\n')
        f.write('</body>\n</html>\n''')


def fecha_arquivo_saida(filename):
    with open(filename, "a", encoding="utf-8") as f:
        f.close()


def main():
    csv_file = 'entrada.csv'
    html_file = 'saida.htm'
    numera_linhas = True

    print("""Olá! Este é o programa de conversão de arquivo CSV para HTML, versão 2023-Out-27.03
          
Conferido e expandido por L.O.D. a partir de sugestão do Google Bard.

Por padrão, este programa lê um arquivo entrada.csv, cria um saida.htm com linhas numeradas,
e usa ponto-e-vírgula como separador.\n\n""")

    entrada = "*"
    while (entrada != "S") and (entrada != "s") and (entrada != "") and (entrada != ","):
        print('Entre com "S" se prefere outros parâmetros, ')
        entrada = input('ou tecle <enter> para prosseguir. ')
        print("\n\n")

    padrao_de_cores = '0'
    while padrao_de_cores < "1" or padrao_de_cores > "5":
        x = input("Digite o número do padrão de cores desejado (1-5): ")
        padrao_de_cores = x[0]
    if padrao_de_cores == '1':
        cor = ('ivory', 'lightblue', 'lightgray', 'silver')
    if padrao_de_cores == '2':
        cor = ('white', 'orange', '#F5FFFA', '#D7E9EC')
    if padrao_de_cores == '3':
        cor = ('lightgray', 'aqua', '#FFFFCC', '#A6845D')
    if padrao_de_cores == '4':
        cor = ('ivory', 'lightblue', 'azure', 'ivory', 'mintcream', 'snow')
    if padrao_de_cores == '5':
        cor = ('silver', 'lightblue', 'hwb(72 95% 0%)', 'hwb(216 95% 0%)', 'hwb(0 97% 0%)', 'hwb(144 94% 0%)', 'hwb(288 96% 0%)')

    separador = ";"
    if entrada == ",":
        separador = ","
    if (entrada == "S") or (entrada == 's'):
        arq_entrada = input("Digite o nome do arquivo de entrada conforme o padrão <entrada.csv>: ")
        arq_saida = input("Digite o nome do arquivo de saída conforme o padrão <saida.htm>: ")
        if arq_entrada == "":
            arq_entrada = "entrada.csv"
        if arq_saida == "":
            arq_saida = "saida.htm"
        if arq_entrada.find(".", -5, -1) < 0:
            arq_entrada += ".csv"
        if arq_saida.find(".", -5, -1) < 0:
            arq_saida += ".htm"
        csv_file = arq_entrada
        html_file = arq_saida
        stringSeparador = input("Digite o caractere separador: ")
        separador = stringSeparador[0]  # Só o primeiro caractere conta
        temp = input("Quer numerar as linhas da tabela (S/n)? ")
        if (temp[0] == 'N') or (temp[0] == 'n'):
            numera_linhas = False
    #
    # codificacao_entrada deve ter o valor utf-8 ou cp1252 (para ANSI)
    #
    codificacao_entrada = pede_codificacao_entrada()
    rows = read_csv_file(csv_file, separador, codificacao_entrada)

    estilo_fonte = 'sans-serif'  # Valor default
    quer_estilo_fonte = "*"
    while (quer_estilo_fonte != '1') and (quer_estilo_fonte != '2') and (quer_estilo_fonte != '3'):
        quer_estilo_fonte = input(
            "Escolha o estilo de fonte (1=Sans Serif; 2=Monospace; 3=Serif)? ")
        quer_estilo_fonte = quer_estilo_fonte[0]
    if quer_estilo_fonte == '1':
        estilo_fonte = 'sans-serif'
    if quer_estilo_fonte == '2':
        estilo_fonte = 'monospace'
    if quer_estilo_fonte == '3':
        estilo_fonte = 'serif'

    cabecalho = ''
    texto_inicial = ''
    inclui_texto = '*'
    while (inclui_texto != 'S') and (inclui_texto != 'N'):
        inclui_texto = input(
            "Quer incluir cabeçalho e/ou texto de apresentação antes da tabela (S/N)? ")
        inclui_texto = inclui_texto[0].upper()

    inicia_html_file(html_file, estilo_fonte, cor)  # Cabecalhos HTML e CSS
    escreve_padrao_de_cores_para_linhas_de_tabelas(html_file, cor)
    escreve_codigo_contador_de_linhas(html_file)
    if inclui_texto == 'S':
        cabecalho = input(
            "Qual deve ser o texto do cabeçalho antes da tabela? ")
        texto_inicial = input(
            "Qual deve ser o texto corrido antes da tabela? ")
        # Etiquetas H1 e P antes da tabela
        insere_texto_abertura(cabecalho, texto_inicial, html_file)

    # Conteúdo da tabela (código HTML completo)
    html_string = create_html_table(rows, numera_linhas)
    write_html_file(html_string, html_file)

    fecha_codigo_html(html_file, codificacao_entrada)

    fecha_arquivo_saida(html_file)

    x = input("Tecle <enter> para encerrar.")


if __name__ == '__main__':
    main()

"""
Próximos recursos a implementar:

1. Perguntar se é desejado numerar as linhas (27.02)
2. Criar a opção de adicionar um título (H1) e um texto introdutório (P) no início do HTML (27.02)
3. Detectar automaticamente a codificação do arquivo de entrada (ANSI ou UTF-8)
   e ajustar de acordo.  Para ANSI, usar "encoding='cp1252' (27.02 permite seleção manual)
4. Facultar outros estilos de fonte (27.02)
5. Oferecer suporte para parâmetros opcionais de tamanhos de fonte
6. Oferecer suporte para outras combinações de cores. (feito em 27.03 e melhorado em 29.03)
7. Encerrar devidamente (e com rodapé) o código HTML (feito em 27.01)
8. Suporte para outros separadores além de "," e ";" (feito em 27.01)
9. Opções para tratar a primeira linha como dados normais (tabela sem linha de cabeçalhos)
   e de inserir manualmente seus próprios cabeçalhos. 
"""
