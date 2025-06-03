# Tópicos especiales en Telemática, período 2025-1

### Profesor:
 * Edwin Nelson Montoya
 
     * Correo: emontoya@eafit.brightspace.com

### Estudiantes:

 * Juan Diego Llorente Ortega

     * Correo: jdllorento@eafit.edu.co

 * Samuel Daza Carvajal

     * Correo: sdazac@eafit.edu.co

 * Santiago Gómez Rueda

     * Correo: sgomezr13@eafit.edu.co

# 1. Breve descripción de la actividad

El objetivo de este proyecto es el desarrollo de un prototipo más cercano a un caso real de ingeniería de datos y Big Data, que tiene las características de:

 * Ser fundamentado en una arquitectura batch o por lotes, completamente automatizada y que no requiera interacción del usuario.

 * Usar un bucket S3 de AWS dividido en secciones para las etapas de los datos (raw/trusted/refined)

 * Tener automatizadas las etapas del ciclo de vida (ingesta, dataprep, procesamiento, display)

 * Nuestro grupo usará la fuente de datos de Open-Meteo a través de su API abierta, extraemos variables del clima de la ciudad de Medellín.

 * El procesamiento y gran parte de la automatización se implementa sobre clusters EMR con procesamiento Spark

## 1.1. ¿Qué aspectos se cumplieron?

 * Ingesta de datos y almacenamiento en zona raw automática usando crontab

 * Dataprep automático tomando el archivo más reciente de la zona raw y subiendo el resultado a la zona trusted usando steps en el cluster

 * Pruebas exitosas de la etapa de dataprep con archivos reales descargados automáticamente.

 * Validación de limpieza y transformación de datos con Spark DataFrame.

 * Implementación de validación de archivos duplicados por fecha.

 * Aplicación de buenas prácticas como eliminación de archivos temporales tras el uso.

## 1.2. ¿Qué aspectos NO se cumplieron?

 * No se logró una automatización al 100% del pipeline debido a limitaciones de AWS, explicado más adelante

# 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

 * Arquitectura de procesamiento por lotes

 * Uso de crontab en una VM para la ingesta automática

 * Uso de bucket S3 para el almacenamiento de los datos y scripts

 * Uso de clusters EMR con Spark a través de steps para la ejecución de scripts de dataprep y procesamiento

 * Uso de bootstrap para la instalación de dependencias en las instancias del cluster

 * Descarga inicial de archivos .json y transformación a .csv

# 3. Descripción del ambiente de desarrollo y técnico:

 * Lenguaje principal: Python 3.12

 * Librerías: boto3, pyspark, os

 * Configuración de Java en la instancia (JAVA_HOME, versión 11).

 * Entorno virtual: venv

 * Herramientas: pip, Git, VSCode

 * Despliegue en entorno AWS

## Paquetes y requerimientos

 * boto3

 * pyspark

## ¿Cómo ejecutar?

1. Con el inicio del laboratorio de AWS academy automáticamente se inicia la VM encargada de la ingesta y se ejecuta el Script correspondiente, guardando el archivo con la fecha.

2. Manualmente hay que clonar el cluster EMR con la configuración ya existente.

3. Ejecución de bootsrap para la instalación de dependencias.

4. Ejecución de step de dataprep y subida a la zona trusted del bucket.

## Capturas de funcionamiento
![image](https://github.com/user-attachments/assets/493148a7-fa06-438c-a04d-f26cf71a706d)
![image](https://github.com/user-attachments/assets/db269e0f-6cdd-4d52-b1fa-d2a5b2db8477)
![image](https://github.com/user-attachments/assets/cb32f8e0-3e8c-493f-8b37-28d059001761)
![image](https://github.com/user-attachments/assets/2a602307-a818-4201-9f05-ba6b6a66e863)


## Parámetros configurables

 * Bucket S3

 * Fuente de datos

 * start_date en el script de ingesta.

 * Variables a descargar

 * Detalles para la limpieza de datos

# 4. Ambiente de ejecución

 * Lenguaje: Python 3.12

 * Crontab en la VM de la ingesta

 * Despliegue en la nube: AWS EC2

 * Instancias m5.xlarge en el cluster EMR

 * Almacenamiento en bucket S3

# 5. Otra información relevante

Abordando el por qué no se logró la automatización en su totalidad y en general el proceso de razonamiento.

 * Para la ingesta, es prácticamente imposible hacerla 100% automático, ya que depende de cuánto tiempo esté iniciado el lab de AWS, se planteó que el script se ejecutara cada 24 horas a las 7 am UTC, pero ahora funciona ejecutándose automáticamente cuando se inicia la instancia.

 * Para el manejo del cluster EMR, se escribió un script que crea el cluster con la configuración y los steps necesarios, pero al ejecutarlo ocurre un error:

```console
An error occurred (AccessDeniedException) when calling the RunJobFlow operation: User: arn:aws:sts::490487474837:assumed-role/EMR_EC2_DefaultRole/i-01c830791698eadd2 is not authorized to perform: elasticmapreduce:RunJobFlow on resource: arn:aws:elasticmapreduce:us-east-1:490487474837:cluster/* because no identity-based policy allows the elasticmapreduce:RunJobFlow action
```

Resulta que esto también es por limitaciones de AWS academy, puesto que la instancia EC2 se ejecuta con el rol IAM EMR_EC2_DefaultRole, y este rol no tiene permisos para crear clusters EMR, por lo que únicamente se pueden crear manualmente en la consola.

Naturalmente, también se intentó crear políticas con permisos de creación de cluster y agregarlas al rol de IAM, o crear otro rol, pero no hay permisos en la cuenta AWS academy para crear políticas o roles.

```console
Access denied to iam:CreateUser

You don't have permission to iam:CreateUser
```

 * Se tenía planeado usar un único script maestro que se ejecutara cuando se iniciara la instancia EC2, este script iniciaría el de ingesta y el de creación del cluster, pero por las limitaciones mencionadas se deja que únicamente se ejecute el script de ingesta al iniciar la instancia, luego de esto habría que manualmente clonar el cluster, haciendo que el proceso sea semiautomático, teniendo que intervenir en esta parte.

 * También con respecto a la automatización, en la etapa inicial del desarrollo del script de ingesta, primero se barajó la posibilidad de usar GitHub actions, que fue descartado por necesitar credenciales permanentes en forma de **secrets** en el repo, pero no fue posible ya que en AWS academy las credenciales son temporales, se generan cada vez que se inicia el laboratorio, al final se tuvo que recurrir a usar un rol IAM con la VM que tuviera permisos para subir contenido a buckets de la cuenta.

 * Todos los scripts, incluso los que no se utilizaron por las limitaciones se encuentran en la rama master del repositorio.

# 6. Video Sustentacion

https://www.youtube.com/watch?v=eX3oMZ7-7Js&feature=youtu.be