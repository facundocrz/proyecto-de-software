# Proyecto de Software

## Introducción

CIDEPINT es el centro de investigación y desarrollo en pinturas de la Facultad de Ingeniería de la Universidad Nacional de La Plata. Su objetivo es promover la competitividad de los productos de pintura argentinos a través de la investigaciones y desarrollos en tecnología de recubrimientos. Además, se dedica a la formación de profesionales especializados y la reación de normas en la industria, abarcando áreas como el tratamiento de aceros, la protección contra la corrosión y soluciones ecológicas.

CIDEPINT plantea la necesidad de una plataforma para mostrar y ofrecer servicios prestados por diferentes instituciones.

## Descripción del proyecto

El proyecto consiste en el desarrollo de una plataforma web que permita a los usuarios visualizar y solicitar servicios ofrecidos por diferentes instituciones. La plataforma se divide en dos partes: una parte pública, donde los usuarios pueden visualizar los servicios ofrecidos y solicitarlos, y una parte privada, donde las instituciones pueden gestionar los servicios ofrecidos y las solicitudes realizadas por los usuarios.

## Estructura del proyecto

- **admin/**: Contiene el código del backend, desarrollado con Python y Flask
- **portal/**: Contiene el código del frontend, desarrollado con Vue.js

## Tecnologías utilizadas

- Python
- Flask
- Jinja
- HTML
- CSS
- JavaScript
- Vue

## Enlaces

- [Frontend Web](https://grupo12.proyecto2023.linti.unlp.edu.ar/)
- [Backend Web](https://admin-grupo12.proyecto2023.linti.unlp.edu.ar/)

## Configuración y uso

### Prerequisitos

- Python
- Node.js
- npm

### Instalación

1. Clonar el repositorio

```bash
git clone https://github.com/facundocrz/proyecto-de-software.git
cd proyecto-de-software
```

2. Instalar las dependencias del backend

```bash
cd admin
pip install -r requirements.txt
```

3. Instalar las dependencias del frontend

```bash
cd ../portal
npm install
```

### Uso

1. Iniciar el backend

```bash
cd admin
flask run
```

2. Iniciar el frontend

```bash
cd portal
npm run serve
```

## Autores

- Facundo Cruz
- Pedro Garofalo
- Marcelo Molina
- Mariano Moreira
