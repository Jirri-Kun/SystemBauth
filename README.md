<h1 align="center"> SystemBauth </h1> <br>

<p align="center">[  !  ] El script requiere la instalación de paquetes, estos pueden encontrarse desde el archivo requirements.txt </p>

<hr/> <br>

<picture> <img align="right" src="https://i.pinimg.com/originals/6c/2b/b8/6c2bb8b7405d465a581a957944dbb8a3.gif?raw=true" width = 250px> </picture> <br> 

**Algunas de sus funcionalidades:**

1 - Verificación de un dominio y servidor al ingresar las credenciales. <br>
2 - Conexión por selección de recursos en una mini interfaz, entablando una mini shell. <br>
3 - Conexión por terminal mediante argumentos, entablando una mini shell. <br>
4 - Visualización de recursos en un servidor. <br> 

<br> <br> <hr/>

<br>

<h2 align="center"> Parametro: -t (credenciales) </h2> <br>

Primeramente, ejecutamos el script con el parametro -t, ingresando las credenciales donde se requiere: <br> <br> 
 
**1. Dominio** <br>
**2. Nombre del Servidor** <br>
**3. Usuario** <br>
**4. Contraseña** <br> <br>

A continuación, se mostrará un ejemplo, pero se debe tomar en cuenta que se deben eliminar los signos de mayor que (<) y menor que (>) junto con el contenido que se encuentra dentro de ellos dejando tal cual los signos que sean indiferentes a estos: 

<br>

```bash
python3 SMBauth.py -t <Dominio>/<Usuario>:<Contraseña>@<host, subdominio o IP>
```

<br>

Aquí un ejemplo más detallado, supongamos que tenemos las siguientes credenciales: 

<br>

**1. Dominio** --> windcorp.thm <br>
**2. Usuario** --> lilyle <br>
**3. Contraseña** --> ChangeMe#1234 <br>
**4. Nombre de servidor** --> fire.windcorp.thm <br>

<br>

```bash
python3 SMBauth.py -t windcorp.thm/lilyle:ChangeMe#1234@fire.windcorp.thm
```

<br>

<h2 align="center"> Parametro: -sr (Visualización de recursos compartidos) </h2> <br>

El parámetro -sr nos muestra los recursos que se alojan en el servidor, estos se clasifican en tres columnas:

<br>

**1. Sharename** --> Nombre del recurso compartido. <br>
**2. Comment** --> Una breve descripción del recurso compartido. <br>
**3. Type** --> El tipo de recurso compartido. <br>

<br>

<p align="center"> <img src="https://github.com/user-attachments/assets/467a780e-50bc-4d8a-9b5d-f2b4903620b1" width = 600px> </p>

<br>

<h2 align="center"> Parametro: -ct (conexión a un recurso compartido) </h2> <br>

Existen dos variantes en el script para entablar una conexión en mini shell:

<br>

**por mini interfaz:**

```bash
python3 SMBauth.py -t <Dominio>/<Usuario>:<Contraseña>@<host, subdominio o IP> -ct
```

Por interfaz, únicamente se escribe el parámetro -ct, en donde se muestran los recursos del servidor y tú puedes elegir entre uno de ellos. Si se escribe incorrectamente, retornará un error.

<p align="center"> <img src="https://github.com/user-attachments/assets/1c16c28d-4431-483e-be63-6f7d02155b57" width = 600px> </p>

<br>

**por terminal:**

Por terminal, solamente se debe escribir el nombre del recurso compartido después de escribir el parámetro -ct, con el cual tenemos permiso de entablar una conexión. Esto te retornara una mini shell.

```bash
python3 SMBauth.py -t <Dominio>/<Usuario>:<Contraseña>@<host, subdominio o IP> -ct <recurso compartido>
```
