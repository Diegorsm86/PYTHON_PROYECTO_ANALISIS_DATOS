#Definir archivo a importar
filename = "Transacción de muestra.txt"
data = open(filename,"r", encoding= "utf-8")
read_data = data.read()
#print(read_data)

import pandas as pd 

def get_transactions_data(strData):
    data_array = []
    insTransaction = False
    for line in strData.split("\n"):
        if "ID_Transaccion" in line or insTransaction == True:
            insTransaction = True   
            data_line = line.split(", ")
            data_array.append(data_line)
       
    df = pd.DataFrame(data_array)
    df.columns = df.iloc[0]
    df = df.drop([0])
    df = df.dropna()
    df = df.reset_index(drop=True)
    return df

trannsaction_data = get_transactions_data(read_data)
#print(trannsaction_data)


#obtener datos del encabezado 
def get_value_by_keyword(strData, strKeyword):
    for line in strData.split("\n"):
        if strKeyword in line:
            data_Value = line.split(": ")
            value = data_Value[1]
            break
    return value
#print(get_value_by_keyword(read_data,"Empresa"))
#print(get_value_by_keyword(read_data,"Fecha del Reporte"))
#print(get_value_by_keyword(read_data,"Número de Sucursal"))


def get_report_data(strData):
    out_dict = {"Empresa": "",
                "Fecha del Reporte":"",
                "Número de Sucursal":"",
                "Transacciones":None    
                }   
    out_dict["Empresa"] =   get_value_by_keyword(strData,"Empresa")
    out_dict["Fecha del Reporte"] =  get_value_by_keyword(read_data,"Fecha del Reporte")
    out_dict["Número de Sucursal"] =  get_value_by_keyword(read_data,"Número de Sucursal")
    out_dict["Transacciones"] = get_transactions_data(strData)
    
    return out_dict

report_data = get_report_data(read_data)
#print(report_data["Transacciones"])


#data_analysis_resume
def get_data_analysis_resume(df_input):
    df = df_input.copy() #se crea una copia del df_input con tal de no modificar datos del data frame inicio.
    
    #Cambiar el nombre precio a precio unitario
    df = df.rename(columns={"Precio":"Precio Unitario"})
    
    # Crear una nueva columna llamada 'Total de venta' que sea la cantidad multiplicada por el precio, le cambio el tipo de dato"Astype float ya que los
    #datos originales venian en tipo "dato" y no numerico. 
    
    df["Cantidad"] = df["Cantidad"].astype(float)
    df["Precio Unitario"] = df["Precio Unitario"].astype(float)
    df["Total de venta"] = df["Cantidad"]* df["Precio Unitario"]
    
    #Obtener el total de ventas por cada categoria
    df_sales_by_category = df[["Categoria","Total de venta"]].groupby("Categoria").sum()
    
    #Crear las columnas Mes, Dia, año
    df["Fecha"] = pd.to_datetime(df["Fecha"], yearfirst=True)
    df["Mes"] = df["Fecha"].dt.month
    df["Dia"] = df["Fecha"].dt.day
    df["Año"] = df["Fecha"].dt.year
    
    #Obtener el producto y fecha con mas venta
    max_sold_index = df["Total de venta"].idxmax()
    most_sold_product = df.iloc[max_sold_index]["Producto"]
    most_sold_date = df.iloc[max_sold_index]["Fecha"]
    
    out_dict = {"data":df,
               "sales_by_category":df_sales_by_category,
               "most_sold_info":{"product": most_sold_product , "date": most_sold_date}}
    
    
    return out_dict
   
data_analysis_resume = get_data_analysis_resume(report_data["Transacciones"])
print(["sales_by_category"])

from matplotlib import pyplot as plt    
#Graficar el historico de ventas por dia

def plot_historycal_sales(dfi):
    df = dfi.copy() 
    df = df[["Fecha","Total de venta"]].groupby('Fecha').sum()
    df = df.reset_index()
    #Crear figura de grafico
    plt.figure(figsize=(20,5)) 
    plt.plot(df["Fecha"], df["Total de venta"], marker = "o", color = "blue")     
    plt.grid(True)
    plt.xlabel("Fecha")
    plt.ylabel("Ventas")
    plt.title("Historico de ventas")
    plt.xticks(df["Fecha"], rotation = 45)
    
    plt.show()
    
   

#output = plot_historycal_sales(data_analysis_resume["data"])


#print(output)

#Graficar el numero de productos vendidos por cada categoria (circular)
def plot_sales_by_category(dfi):
    df = dfi.copy()
    df = df.reset_index()

    plt.title("Ventas por categoria", pad=25)
    plt.pie(df["Total de venta"], labels = df["Categoria"], colors = ["skyblue", "lightgreen","lightcoral"])
    plt.legend(df["Categoria"]) 
    plt.show()

    return
plot_sales_by_category(data_analysis_resume["sales_by_category"])




    











        
    





