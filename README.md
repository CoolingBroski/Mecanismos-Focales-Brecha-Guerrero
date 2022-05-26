# Mecanismos Focales Brecha Guerrero
Repositorio para el cálculo de mecanismos focales de sismos de baja magnitud en la brecha de Guerrero por medio del método de Nawa Dahal y John Ebel

Para la ejecución del flujo de trabajo, es necesario lo siguiente:

Configurar un entorno estrictamente de Python 3.8, preferiblemente de Anaconda, con las siguientes versiones de liberías. Es importante verificar las versiones para evitar incompatibilidades:

obspy==1.2.2
pandas==1.1.0
numpy==1.20.3
mttime==1.0.0 -> La cual tiene como dependencia a la librería cartopy en su versión 0.17.0, que a su vez requiere dentro de un sistema Debian la instalación de los paquetes libproj-dev, proj-data, proj-bin y libgeos-dev.

Tener instalados los programas incluídos en Computer Programs in Seismology de Saint Louis University para la generación de sismogramas sintéticos. Para la compilación de estos programas, se requiere gcc y gfortran. Además, la instalación de estos programas también requiere de los paquetes make, xorg-dev y libncurses5-dev en un sistema Debian.

Finalmente, para la descarga automática de datos del SSN de México con el script de Bash download_data.sh, es necesario colocar el programa SSNstp en ~ y otorgarle permiso de ejecución. Además, debe ejecutarse dicho script en el directorio del repositorio, el cual debe tener contener un directorio con nombre "Datos". Esto para la compatibilidad con el flujo de trabajo. Si esta descarga de datos será ejecutada en un sistema Debian de 64 bits, es necesario tener instalado el paquete libc6-i386 para obtener soporte para programas de 32 bits, como es el caso de SSNstp.

Posterior a ejecutar download_data.sh, se debe ejecutar el script de Python org_data.py

Orden de ejecución de las libretas de Python (Mientras no se hayan eliminado los datos obtenidos por procesos anteriores, no es necesario ejecutarlos nuevamente si solo se requieren los resultados de cierto proceso intermedio):

Download_Org.ipynb -> Se colocan los sismogramas en Datos_Trim.

Preprocessing.ipynb -> Se elimina la respuesta del instrumento, se rota a RT. Además, se calculan las distancias y azimut para guardar esta información en los archivos SAC y en tablas ev_st. Finalmente, se mantienen únicamente las estaciones dentro del rango de distancias designado.

Synthetics.ipynb -> Se filtran y recortan los sismogramas rotados, se calculan los sismogramas sintéticos y se genera el archivo de configuración inicial de la inversión.

Inversion.ipynb -> Se busca la mejor combinación de estaciones mediante un proceso iterativo de eliminación de estaciones que incremente lo más posible el VR y el porcentaje DC.

El archivo catalogSSN.dat debe contener todos los datos necesarios para cada evento. Este archivo controla aquellos eventos que serán procesados en cada paso del flujo de trabajo.
