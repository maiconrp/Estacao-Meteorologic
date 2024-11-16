###     ESTE ARQUIVO CRIA OS DICIONÁRIOS QUE REPRESENTAM 
###     OS HISTÓRICOS DOS VALORES COLETADOS DE UM DIA ESPECÍFICO   

import numpy as np
import pandas as pd
from Tables.Estacao.historicosEstacao import*


### Caminhos do diretório de cada tipo de arquivo
### Por enquanto, para cada tabela de um dia, de cada estação, é necessário alterar o caminho manualmente aqui no código.
path_json='C:\\Users\\Victor Fonteles\\Documents\\validacao\\Tables\\Estacao\\05-07-2023-temp.json'
path_csv_Dia30='C:\\Users\\Victor Fonteles\\Documents\\validacao\\Tables\\INMET\\30-06-2023-INMET.csv'
path_csv_Dia2='C:\\Users\\Victor Fonteles\\Documents\\validacao\\Tables\\INMET\\02-07-2023-INMET.csv'
path_csv_Dia5='C:\\Users\\Victor Fonteles\\Documents\\validacao\\Tables\\INMET\\05-07-2023-INMET.csv'


# A partir do csv baixado, essa função irá criar um dicionário que relaciona os horários com 
# os valores coletados de um parâmetro climático 
def GerarHistoricoInmet(path, parametro):
    ###     Criando dataframe do arquivo csv, que foi baixado diretamento do site do INMET: https://mapas.inmet.gov.br/, a partir da estação desejada
    df = pd.read_csv(path, encoding='ISO-8859-1')

    #transforma o dataframe 'df' em um dicionario python
    dicionario_clima = df.to_dict()

    #Cria o dict 'horas', onde cada chave recebe o um valor da chave 'Hora (UTC)' do 'dicionario_clima'
    horas =  dicionario_clima['Hora (UTC)']

    # Atualiza os valores deixando o horário no formato HH:MIN
    horas = {key: f"{str(value).zfill(4)[:2]}:{str(value).zfill(4)[2:]}" for key, value in horas.items()}

    #Cria o dict 'valores', onde cada chave recebe um valor das chaves do parametro climatologico do 'dicionario_clima'
    valores = dicionario_clima[parametro]

    #Cria o dicionário que irá de fato contes o históricco dos valores
    dict_historico_INMET = {}

    ###     Preenche o dicionário relacionando as horas com os respectivos valores      ###
    i=0
    for hora in horas.values():
        valor = valores[i]
        dict_historico_INMET[hora] = valor
        i=i+1


    return dict_historico_INMET

# A partir do json baixado, essa função irá criar um dicionário que relaciona os horários com 
# os valores coletados de um parâmetro climático    
def GerarHistóricoEst(path, parametro):
    ###     Cria o dataframe do arquivo json, que foi exportado do firebase
    df = pd.read_json(path, encoding='ISO-8859-1')

    dataframe = pd.DataFrame(df)

    # Converter o índice para datetime
    dataframe.index = pd.to_datetime(df.index)

    # Formatar o índice sem a data
    dataframe.index = df.index.strftime("%H:%M:%S")

    ### Cria um dicionário que contém somente a coluna do parâmetro desejado
    ### Este dicionário já relaciona os valores coletados com sua respectiva hora
    dict_historico_EST = dataframe[parametro]

   
    return dict_historico_EST

# Cria a lista "medicoes", que irá guardar os valores medidos daquele parâmetro climático, 
# convertidos em float
def GerarListaMedicoes(dicio, parametro):
    if parametro == 'Temp. Ins. (C)' or parametro== 'Vel. Vento (m/s)' or parametro =='Radiacao (KJ/m)':
        ###     Percorre cada valor, e substitui a virgula por ponto, transformando em tipo float.
        try:
            medicoes = [float(v.replace(',', '.')) for v in dicio.values() if type(v) != 'NoneType']
        except:
            medicoes = [i for i in range(24)]
    else:
        ###     Se o parâmetro for 'umidade', apenas percorre   os valores, transformando eles em int.         
        try:
            medicoes = [int(v) for v in dicio.values() if type(v) != 'NoneType']
        except:
            medicoes = [i for i in range(24)]

    return medicoes

def filtrar_horas_proximas(dicio):
    novo_dict = {}
    
    for hora, valor in dicio.items():
        hora_proxima = hora[:2] + ":00"  # Extrair apenas a parte da hora e adicionar ":00"
        
        if hora_proxima not in novo_dict:
            novo_dict[hora_proxima] = (hora, valor)  # Armazenar o par (hora, valor)
            
        else:
            hora_atual, valor_atual = novo_dict[hora_proxima]  # Valor já armazenado
            
            diff_proxima = abs(int(hora.split(":")[1]) - int(hora_proxima.split(":")[1]))  # Diferença entre os minutos da hora atual e a próxima
            diff_atual = abs(int(hora_atual.split(":")[1]) - int(hora_proxima.split(":")[1]))  # Diferença entre os minutos da hora já armazenada e a próxima
            
            if diff_proxima < diff_atual:
                novo_dict[hora_proxima] = (hora, valor)  # Substituir o par armazenado pelo par correspondente à hora mais próxima
    
    novo_dict = {hora: valor for hora, valor in novo_dict.values()}  # Remover a hora original e manter apenas a hora mais próxima e o valor associado

    # Adicionar manualmente o índice '14:00' caso não esteja presente no dicionário

    return novo_dict

def ajustar_horarios(dicio, val):
    novo_dict = {}
    
    for hora, valor in dicio.items():
        hora_dt = pd.to_datetime(hora)  # Converter para objeto datetime
        hora_arredondada = hora_dt.round('H')  # Arredondar para a hora mais próxima
        nova_hora = hora_arredondada + pd.DateOffset(hours=3)  # Adicionar 3 horas
        nova_hora_str = nova_hora.strftime('%H:%M')  # Converter de volta para string HH:MM
        novo_dict[nova_hora_str] = valor

    return novo_dict

##################### - - - FILTRAR HORAS PRÓXIMAS - - - - #########################

dictTempDia30 = filtrar_horas_proximas(temperatura_dia30)    
dictTempDia1 = filtrar_horas_proximas(temperatura_dia1)
dictTempDia2 = filtrar_horas_proximas(temperatura_dia2)
dictTempDia5 = filtrar_horas_proximas(temperatura_dia5)


dictUmidadeDia30 = filtrar_horas_proximas(umidade_dia30)
dictUmidadeDia1 = filtrar_horas_proximas(umidade_dia1)
dictUmidadeDia2 = filtrar_horas_proximas(umidade_dia2)
dictUmidadeDia5 = filtrar_horas_proximas(umidade_dia5)


dictVentoDia30 = vento_dia30
dictVentoDia1 = filtrar_horas_proximas(vento_dia1)
dictVentoDia2 = filtrar_horas_proximas(vento_dia2)
dictVentoDia5 = filtrar_horas_proximas(vento_dia5)


dictRadiacaoDia1 = radiacao_dia1


######################### - - - AJUSTAR HORÁRIOS - - - #################################

dictTempDia30 = ajustar_horarios(dictTempDia30, 'temp')
dictTempDia1 = ajustar_horarios(dictTempDia1, 'temp')
dictTempDia2 = ajustar_horarios(dictTempDia2, 'temp')
dictTempDia5 = ajustar_horarios(dictTempDia5, 'temp')


dictUmidadeDia30 = ajustar_horarios(dictUmidadeDia30, 'umi')
dictUmidadeDia1 = ajustar_horarios(dictUmidadeDia1, 'umi')
dictUmidadeDia2 = ajustar_horarios(dictUmidadeDia2, 'umi')
dictUmidadeDia5 = ajustar_horarios(dictUmidadeDia5, 'umi')


#dictVentoDia30 = ajustar_horarios(dictVentoDia30, 'vento')
dictVentoDia1 = ajustar_horarios(dictVentoDia1, 'vento')
dictVentoDia2 = ajustar_horarios(dictVentoDia2, 'vento')
dictVentoDia5 = ajustar_horarios(dictVentoDia5, 'vento')


print(dictRadiacaoDia1)



##################### - - - INMET - - - #######################
historico_temperatura_INMET_Dia30 = GerarHistoricoInmet(path_csv_Dia30, "Temp. Ins. (C)")
historico_temperatura_INMET_Dia2 = GerarHistoricoInmet(path_csv_Dia2, "Temp. Ins. (C)")
historico_temperatura_INMET_Dia5 = GerarHistoricoInmet(path_csv_Dia5, "Temp. Ins. (C)")


historico_umidade_INMET_Dia30 = GerarHistoricoInmet(path_csv_Dia30, "Umi. Ins. (%)")
historico_umidade_INMET_Dia2 = GerarHistoricoInmet(path_csv_Dia2, "Umi. Ins. (%)")
historico_umidade_INMET_Dia5 = GerarHistoricoInmet(path_csv_Dia5, "Umi. Ins. (%)")

historico_vento_INMET_Dia30 = GerarHistoricoInmet(path_csv_Dia30, "Vel. Vento (m/s)")
historico_vento_INMET_Dia2 = GerarHistoricoInmet(path_csv_Dia2, "Vel. Vento (m/s)")
historico_vento_INMET_Dia5 = GerarHistoricoInmet(path_csv_Dia5, "Vel. Vento (m/s)")





################ - - - Mediçoes - - - #########################
medicoes_temperatura_Dia30 = GerarListaMedicoes(historico_temperatura_INMET_Dia30, 'Temp. Ins. (C)')
medicoes_temperatura_Dia2 = GerarListaMedicoes(historico_temperatura_INMET_Dia2, 'Temp. Ins. (C)')
medicoes_temperatura_Dia5 = GerarListaMedicoes(historico_temperatura_INMET_Dia5, 'Temp. Ins. (C)')

medicoes_umidade_Dia30 = GerarListaMedicoes(historico_umidade_INMET_Dia30, 'Umi. Ins. (%)')
medicoes_umidade_Dia2 = GerarListaMedicoes(historico_umidade_INMET_Dia2, 'Umi. Ins. (%)')
medicoes_umidade_Dia5 = GerarListaMedicoes(historico_umidade_INMET_Dia5, 'Umi. Ins. (%)')











