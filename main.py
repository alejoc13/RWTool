import helper.loadData as ld







if __name__ =='__main__':
    token =input('Ingrese la Contraseña para acceder a los datos de Smartsheet: ')
    menu = True
    while menu != False:
        try:
            option = input("""
            1. Crear Hoja de trabajo basada en PLC RW
            2. Comparar Documento Cofepris con el Submission Plan
            Ingrese el numero de la opción a utilizar: """)
            option = int(option)
        except:
            if option == '':
                print('Funcion terminada')
                break
            else:
                print('Opción Incorrecta')
                print('#---------------------------------------')
        
            
            
    # ld.ChargeRW(token)