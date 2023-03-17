import math

# Definição das variáveis
Rn = 12.3   # Saldo de radiação em MJ/m2.dia
G = 0.6     # Fluxo total diário de calor do solo em MJ/m2.dia 
Temp = 25.6 # Temperatura em graus Celsius
ur = 81.6   # Umidade Relativa em porcentagem
vv = 2.0    # Velocidade do vento à 2m de altura em m/s
z = 335     # Altitude do local em m
 
# Cálculo da declividade da curva de pressão de vapor em relação à temperatura (kPa/oC)
delta = 4098*(0.6108*math.exp((17.27*Temp)/(Temp+237.3)))/(Temp+237.3)**2
 
# Cálculo do coeficiente psicométrico (kPa/oC)
gama = 0.665*(10**-3)*(101.3*((293-0.0065*z)/293)**5.26)
 
# Cálculo do déficit de saturação 
# (Diferença entre Pressão de saturação de vapor - es e Pressão atual de vapor - ea) (kPa)
es = 0.6108*math.exp((17.27*Temp)/(Temp+237.2))
ea = (es*ur)/100
 
# Cálculo da Evapotranspiração de Referência em mm
EToPMF = (0.408*delta*(Rn-G)+((gama*900*vv*(es-ea))/(Temp+273)))/(delta+gama*(1+0.34*vv))

# Imprimir o valor calculado da Evapotranspiração de Referência em mm
print("O valor da Evapotranspiração de Referência é: ", EToPMF, "mm")
