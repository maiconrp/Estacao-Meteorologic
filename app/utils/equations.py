from database import Am, esp_linhas, esp_plantas, vazao, TR, Ai, Rn, vv, ur, Temp, data_plantio, setIdade, tempo_ant
from datetime import date, datetime

################################ ETo

## Cálculo da Evapotranspiração de Referência (ETo)
## https://ainfo.cnptia.embrapa.br/digital/bitstream/CNPUV/8815/1/cir065.pdf

# Definição das variáveis

Rn = 12.3
G = 0 # Fluxo total diário de calor do solo em MJ/m2.dia 
z = 530     # Altitude do local em m'''

# Cálculo da declividade da curva de pressão de vapor em relação à temperatura (kPa/oC)
delta = 4098*(0.6108*2.71828**((17.27*Temp)/(Temp+237.3)))/(Temp+237.3)**2


# Cálculo do coeficiente psicométrico (kPa/oC)
gama = 0.665*(0.001)*(101.3*((293-0.0065*z)/293)**5.26)


# Cálculo do déficit de saturação 
# (Diferença entre Pressão de saturação de vapor - es e Pressão atual de vapor - ea) (kPa)
es = 0.6108*2.71828**((17.27*Temp)/(Temp+237.3))

ea = (es*ur)/100

# Cálculo da Evapotranspiração de Referência em mm
EToPMF = (0.408*delta*(Rn-G)+((gama*900*vv*(es-ea))/(Temp+273)))/(delta+gama*(1+0.34*vv))


##################### ETc


Kc= 1.2
Etc= (EToPMF*Kc)
Etc = float(Etc)


############################# Volume
Cu = 0.85

print(Etc)

#Vt = volume total de água a ser aplicado por irrigação, m3;
#Ai = 0.5
Vt = 1000*((float(Etc)*float(TR)*float(Ai))/(Cu))

Vt = (int(Vt/100))

print(Vt)

esp_plantas = esp_plantas/100
esp_linhas = esp_linhas/100

####################################### Tempo de irrigação
Ti = 6*((float(Vt)*float(esp_linhas)*float(esp_plantas))/(float(Ai)*float(vazao)))

Ti = round(Ti)

print(Ti)

#Tempo de funcionamento por posição(Setor) para Irrigação em faixa contínua



Area = Ai*10000

################# idade da cultura
data1 = date.today()
data2 = datetime.strptime(data_plantio, "%d/%m/%Y").date()

idade = data1 - data2

idade = idade.days

setIdade(idade)
print(idade)


#################### Economia

economia = 100 - (((Ti/60)*vazao)/((tempo_ant/60)*vazao)*100)
print(tempo_ant)

quant_gotej = ((Ai*10000)/((esp_linhas/100)*(esp_plantas/100)))

litros_economizados = (quant_gotej*(tempo_ant/60)*vazao)-(Vt*1000)

litros_economizados = round(litros_economizados)
print(litros_economizados)