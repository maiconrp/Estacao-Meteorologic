from Utils.historicos import *

def CalcAssertividade(historico_INMET, historico_EST):
    assertividades = []
    for key in historico_INMET:

        if not isinstance(historico_INMET[key], int):
            valor1 = float(historico_INMET[key].replace(',', '.'))
        else:
            valor1 = historico_INMET[key]

        valor2 = historico_EST[key]

        if valor2 < valor1:
            assertividade = round((valor2 / valor1) * 100, 2)
        else:
            assertividade = round((valor1 / valor2) * 100, 2)

        assertividades.append(assertividade)
    
    media = round(sum(assertividades) / len(assertividades), 2)
    print(assertividades)
    return media 


def CalcMAiorVariancia(historico_INMET, historico_EST):
    variancias = {}
    for key in historico_INMET:

        if not isinstance(historico_INMET[key], int):
            valor1 = float(historico_INMET[key].replace(',', '.'))
        else:
            valor1 = historico_INMET[key]

        valor2 = historico_EST[key]
        variancia = round(valor1 - valor2, 2)
        variancias[key] = variancia

    # Encontrando a chave com a maior diferença
    print(variancias)
    chave_maior_variancia = max(variancias, key=lambda k: abs(variancias[k] - 0))
    maior_diferenca = variancias[chave_maior_variancia]
    if maior_diferenca < 0:
        maior_diferenca = str(maior_diferenca).replace("-", "")
        maior_diferenca = str(maior_diferenca) + "% Acima, às "
    else:
        maior_diferenca = str(maior_diferenca) + "% Abaixo, às "

    return str(maior_diferenca) + str(chave_maior_variancia)


def CalcMediaVariancia(historico_INMET, historico_EST):
    variancias = []
    for key in historico_INMET:

        if not isinstance(historico_INMET[key], int):
            valor1 = float(historico_INMET[key].replace(',', '.'))
        else:
            valor1 = historico_INMET[key]

        valor2 = historico_EST[key]
        variancia = round(valor1 - valor2, 2)
        variancias.append(variancia)

    media = round(sum(variancias) / len(variancias), 2)
    print(variancias)

    if media < 0:
        media = str(media).replace("-", "")
        media = str(media) + "% Acima"
    else:
        media = str(media) + "%  Abaixo"

    return media



media_variancia_temperatura = CalcMediaVariancia(historico_temperatura_INMET_Dia5, dictTempDia5)
media_variancia_umidade = CalcMediaVariancia(historico_umidade_INMET_Dia2, dictUmidadeDia2)
print("Media variancia temp " + str(media_variancia_temperatura))
#print("Media variancia umidade " + str(media_variancia_umidade))

maior_variancia_temperatura = CalcMAiorVariancia(historico_temperatura_INMET_Dia5, dictTempDia5)
maior_variancia_umidade = CalcMAiorVariancia(historico_umidade_INMET_Dia2, dictUmidadeDia2)
print("Maior variancia temp " + str(maior_variancia_temperatura))
#print("Maior variancia umidade " + str(maior_variancia_umidade))


assertividade_temperatura = CalcAssertividade(historico_temperatura_INMET_Dia5, dictTempDia5)
assertividade_umidade = CalcAssertividade(historico_umidade_INMET_Dia2, dictUmidadeDia2)
print("Assertividade Temp " + str(assertividade_temperatura))
#print("Assertividade Umidade " + str(assertividade_umidade))


