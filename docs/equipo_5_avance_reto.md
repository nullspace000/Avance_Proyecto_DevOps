## Objetivo

Diseñar e implementar un flujo de trabajo DevOps escalable y automatizado en Amazon Web Services (AWS), integrando herramientas de control de versiones, contenedores, infraestructura como código, pipelines de CI/CD, monitoreo y seguridad, con el fin de optimizar los tiempos de entrega, mejorar la estabilidad de las aplicaciones y garantizar la seguridad de la infraestructura en la nube.

## Instrucciones

Caso de análisis:  

La empresa Soluciones Tecnológicas del Futuro es una organización de reciente creación y en expansión, dedicada al desarrollo de aplicaciones web para el sector financiero. Actualmente, enfrenta desafíos en la gestión y despliegue de sus soluciones en la nube. Su proceso de entrega de software es manual, lo que genera retrasos en las actualizaciones, errores durante la implementación en producción y dificultades para monitorear el rendimiento de sus aplicaciones.  

Para abordar estos problemas, Soluciones Tecnológicas del Futuro ha decidido implementar una plataforma automatizada de despliegue y monitoreo en AWS, adoptando prácticas de DevOps. El objetivo de este proyecto es optimizar los tiempos de entrega, mejorar la estabilidad de sus aplicaciones y garantizar la seguridad de la infraestructura en la nube para sus clientes.

## Procedimiento:  

### 1. Elaborar una presentación que exponga los principios de DevOps
   - nombre de la presentación: devops_principios.html

### 2. Crear un repositorio en Github
   `https://github.com/nullspace000/Avance_Proyecto_DevOps.git`  
   
   ![screenshot](imgs/repo.png)  

### 3. Configurar un entorno de desarrollo en Linux
   1. Instalar Ubuntu en una máquina virtual local o en una instancia AWS EC2 (solo tamaños nano, micro, small, medium o large).
   2. Configurar paquetes esenciales: git, vim, docker, python3.
   3. Crear y ejecutar scripts Bash para automatizar tareas. 
   ``` sudo apt update && sudo apt upgrade -y
# Herramientas base
sudo apt install -y git vim curl build-essential
# Python 3 y pip
sudo apt install -y python3 python3-pip python3-venv
# Docker Engine (repositorio oficial)
sudo apt install -y ca-certificates gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io
# Añadir tu usuario al grupo docker
sudo usermod -aG docker "$USER"
```
   5. Automatizar la instalación de dependencias.
   Crea un archivo bootstrap_dev.sh:
   ```#!/usr/bin/env bash
   set -euo pipefail
   sudo apt update
   sudo apt install -y git vim python3 python3-pip docker.io
   echo "Instalación completa. 
   ```
   ![screenshot](imgs/3.png)
   1. Programar tareas con cron para limpieza de logs.  
      Crea un script clean_logs.shque elimine o rote logs antiguos
      ``` #!/usr/bin/env bash
      set -euo pipefail
      LOG_DIR="/var/log/myapp"
      DAYS_TO_KEEP=7
      find "$LOG_DIR" -type f -name "*.log" -mtime +"$DAYS_TO_KEEP" -print -delete
      ```
   Programa una tarea cron para ejecutarlo, por ejemplo diariamente a las 03:30:
      ```crontab -e
      30 3 * * * /usr/local/bin/clean_logs.sh >> /var/log/clean_logs.cron.log 2>&1
      ```  
      ![screenshot](imgs/4.png)


### 4. Desarrollar un script en Python para automatizar tareas
   1. Crear las claves de acceso IAM para poder hacer uso de los script
   ![screenshot](imgs/7.png)
   Configurar los datos en el EC2  
   ![screenshot](imgs/8.png)
   3. Crear un script para aprovisionar instancias EC2 (máximo 9 instancias en total, respetando los límites de Learner Lab).
   saber el AMI del EC2 para poder hacer la creacion  
   ![screenshot](imgs/9.png)  
   Correrlo  
   ![screenshot](imgs/10.png)  
   ![screenshot](imgs/11.png)
   4. Generar un reporte automático de uso de recursos.  
   ![alt text](imgs/image-1.png)
   5. Utilizar Boto3 para interactuar con AWS.
   ![screenshot](imgs/5.png)
   6. Listar buckets en S3 y sus objetos.  
   ![screenshot](imgs/6.png)

### 5. Diseñar una plantilla CloudFormation
   1. Definir infraestructura en YAML para instancias EC2 y S3, asegurando que las instancias cumplan los límites del entorno.  
   ![alt text](imgs/image-2.png)
   2. Aplicar políticas de IAM solo con el rol LabRole preexistente, ya que Learner Lab no permite crear nuevos roles o grupos.
   #### No aplica ya que no es learner lab 
   3. Implementar recursos en AWS mediante IaC.
   ```
   aws cloudformation deploy \
  --stack-name devops-stack \
  --template-file stack-dev.yaml \
  --parameter-overrides \
    AmiId=ami-00de3875b03809ec5 \
    InstanceType=t3.micro \
  --region us-east-1
   ```
   4. Desplegar y actualizar infraestructura con AWS CloudFormation deploy.  
   ![alt text](imgs/image.png)  

### 6. Crear una imagen Docker para una aplicación web
   1. Definir un Dockerfile con configuración de nginx o flask.  
   
      Dockerfile: 
      ```
      # Stage 1: Build (dependency instalation)
      FROM python:3.11-slim AS builder

      WORKDIR /app
      COPY requirements.txt .
      # Instalamos dependencias en un directorio local
      RUN pip install --user --no-cache-dir -r requirements.txt

      # Stage 2: Final (light image for exec)
      FROM python:3.11-slim

      WORKDIR /app
      # Copiamos solo las dependencias instaladas y el código
      COPY --from=builder /root/.local /root/.local
      COPY . .

      # Asegurar que el PATH incluya las librerías instaladas
      ENV PATH=/root/.local/bin:$PATH

      EXPOSE 5000
      CMD ["python", "app.py"]
      ```

   2. Optimizar la imagen con multi-stage builds.
      - docker compose up --build
      - tenemos stage 1 y stage 2

   3. Configurar docker-compose.yml para múltiples servicios.  
      docker-compose.yml:
      ```
      version: '3.8'

      services:
      web:
         build: .
         ports:
            - "8080:5000"
         volumes:
            - ./app:/app  # Hot-reloading para desarrollo
         networks:
            - frontend
            - backend
         depends_on:
            - db
         environment:
            - REDIS_HOST=db

      db:
         image: redis:alpine
         networks:
            - backend
         volumes:
            - redis_data:/data

      networks:
      frontend:
         driver: bridge
      backend:
         internal: true  # Red aislada para seguridad

      volumes:
      redis_data:
      ```
   4. Definir volúmenes y redes personalizadas.
      ```
      [null@T480 avance_reto]$ sudo docker network ls
      [sudo] password for null: 
      NETWORK ID     NAME              DRIVER    SCOPE
      08b7811756f4   bridge            bridge    local
      ff7efc952609   docker_backend    bridge    local
      32db7fe7059d   docker_frontend   bridge    local
      0c6fa98669dc   host              host      local
      0e8316485271   none              null      local
      ```
      ![alt text](imgs/12.png)

### 7. Implementar un pipeline CI/CD con AWS CodeCommit
   1. Configurar CodeCommit y CodeBuild para pruebas automatizadas.  
      - CodeCommit y CodeBuild no están accesibles en la capa gratuita de AWS.
      - Al no tener acceso a los learner labs, no podemos continuar con esta parte del reto.
      ![alt text](imgs/13.png)
   2. Integrar CodePipeline para despliegue continuo.
   3. Enviar archivos a EC2 utilizando AWS Systems Manager Session Manager.
   4. Usar AWS Lambda para automatizar rollback ante fallos.
   
### 8. Prepara y revisa cuenta de acceso y recursos en AWS
   1. Regresa al inicio de tu cuenta en AWS a través del Learner Lab.
   ![alt text](image.png)
   2. Explora la consola de AWS y familiarízate con los servicios principales.
   7
   3. Configura AWS CLI en Cloud9 y autentica el acceso.
   ![alt text](image-1.png)
   4. Lista recursos activos en AWS mediante comandos CLI dentro de Learner Lab.
   ![alt text](image-7.png)
   5. Utiliza LabRole en vez de crear nuevos usuarios IAM para CI/CD.
   ![alt text](image-2.png)
   6. Revisa y define permisos utilizando el rol preexistente (LabRole).
   ![alt text](image-8.png)
   7. Aplica restricciones de seguridad en IAM sin crear nuevos usuarios ni grupos.
   ![alt text](image-9.png)
   8. Valida el acceso a los servicios con AWS Policy Simulator.![alt text](image-10.png)
### 9. Infraestructura y redes en AWS
   
   1. Crea una instancia EC2 dentro de los límites de Learner Lab (máximo 9 instancias simultáneas).
      ![alt text](image-3.png)
   2. Configura reglas de Security Groups para acceso restringido.
      ![alt text](image-4.png)
   3. Implementa una política en EC2 utilizando LabRole.
      ![alt text](image-5.png)
      
   4. Conéctate a la instancia EC2 usando AWS Systems Manager en vez de SSH.
![alt text](image-11.png)
   5. Asigna permisos a la instancia mediante el perfil LabInstanceProfile.
      ![alt text](image-6.png)
   6. Diseña una VPC con subredes públicas y privadas dentro de us-east-1 o us-west-2.
![alt text](image-12.png)
   7. Configura una tabla de enrutamiento y gateway de internet. 
   ![*alt text*](image-13.png)
   8. Documenta la arquitectura de red mediante un diagrama. 
![alt text](image-14.png)
### 10. Almacenamiento y bases de datos AWS
   
   1. Crea un bucket en S3 y configura permisos de acceso con LabRole.
![alt text](image-17.png)
   2. Implementa políticas de versión en objetos S3.
   ![alt text](image-16.png)
   3. Automatiza la carga de archivos a S3 mediante boto3 en Cloud9.
   ![alt text](image-19.png)![alt text](image-22.png)
   4. Habilita el cifrado de datos en reposo, verificando disponibilidad.
   ![alt text](image-18.png)![alt text](image-21.png)
   5. Implementa reglas de ciclo de vida para la eliminación automática de objetos.
   ![alt text](image-20.png)
   6. Crea una tabla DynamoDB con una clave primaria definida.
   ![alt text](image-23.png)
   7. Inserta, modifica y elimina registros utilizando AWS SDK para Python (boto3).
   ![alt text](image-24.png)
   8. Aplica restricciones de acceso a DynamoDB mediante LabRole.
   ![alt text](image-25.png)
   9.  Documenta las operaciones realizadas con capturas de pantalla.
   
   Implicito que ya esta 

### 11. Monitoreo y registro de eventos 

   1. Configura AWS CloudWatch para visualizar métricas de EC2 y S3.
   ![alt text](image-26.png)![alt text](image-27.png)
   2. Crea una alarma en CloudWatch para detectar alto consumo de CPU en EC2.![alt text](image-33.png)
![alt text](image-28.png)![alt text](image-30.png)
   3. Genera dashboards personalizados en CloudWatch.
![alt text](image-32.png)
   4. Audita acciones en la cuenta AWS mediante AWS Config, evitando CloudTrail.

   5. Configura AWS Config para supervisar cambios en los recursos.
![alt text](image-29.png)
   6. Almacena logs generados en un bucket S3 dedicado.
![alt text](image-31.png)
   7. Envía logs de una instancia EC2 a CloudWatch Logs utilizando agente de logs.
![alt text](image-34.png)
![alt text](image-35.png)![alt text](image-36.png)
### 12. Seguridad en AWS

   1. Implementa roles de IAM utilizando exclusivamente LabRole.
![alt text](image-37.png)
   2. Aplica configuraciones de seguridad dentro de las restricciones de IAM.
![alt text](image-38.png)
   3. Configura acceso temporal mediante LabRole.
![alt text](image-39.png)
   4. Crea políticas de seguridad en Security Groups en lugar de roles IAM.
![alt text](image-40.png)
   5. Configura acceso restringido a AWS Lambda dentro del límite de 10 ejecuciones concurrentes.
![alt text](image-41.png)![alt text](image-42.png)![alt text](image-43.png)
   6. Aplica restricciones de acceso condicional basado en IP dentro de Security Groups.
![alt text](image-44.png)
### 13. Arquitectura de microservicios.

   1. Diseñar una función dentro de una arquitectura de microservicios para la aplicación.
   
   2. Desplegar un servicio independiente en AWS Lambda respetando el límite de 10 ejecuciones concurrentes.
   ![alt text](image-46.png)
   No tengo disponibles por que es una cuenta empresarial :(
   3. Crear una función que devuelva un mensaje JSON de manera aleatoria usando Node.js o Python.
   ![alt text](image-45.png)
   4. Configurar una API con API Gateway como disparador de la función Lambda.
   ![alt text](image-47.png)
   5. Registrar logs de ejecución utilizando CloudWatch Logs.![alt text](image-48.png)![alt text](image-49.png)![alt text](image-50.png)![alt text](image-51.png)