S = "modo=registro&login=coe&password=potroso&nombre=Victorino&apellidos=Villa+Echeverri&email=gabold%40cartasdeajuste.yu&dni=92540376Z&direccion=Pl.+Lugo+187%2C+&ciudad=Beas+de+Segura&cp=33317&provincia=%C1vila&ntc=8703807831121479&B1=Registrar"

arr = S.split('&')

print(arr[2].lstrip("password="))