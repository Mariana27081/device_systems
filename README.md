# 🚀 EVOLUCIÓN DE DEVICE_SYSTEMS: API REST AVANZADA PARA LA GESTIÓN DE USUARIOS

Bienvenidos a la documentación oficial de **device_systems**, una solución backend intermedia construida sobre el framework de alto rendimiento **FastAPI**. Este proyecto representa la evolución técnica de un servicio inicial de gestión hacia una arquitectura empresarial modular, robusta, testeable y autodocumentada.

El propósito principal de esta aplicación es gestionar de manera eficiente el recurso de usuarios (`/users`), aplicando una separación estricta de responsabilidades, inyección de dependencias y un control profesional de flujos de error y códigos de estado HTTP.

---

## 📋 ÍNDICE
1. [Descripción General y Arquitectura](#-descripción-general-y-arquitectura)
2. [Estructura del Proyecto (Separación de Responsabilidades)](#-estructura-del-proyecto-separación-de-responsabilidades)
3. [Tecnologías Utilizadas](#-tecnologías-utilizadas)
4. [Instalación, Configuración y Despliegue](#-instalación-configuración-y-despliegue)
5. [Matriz Completa de Endpoints (CRUD)](#-matriz-completa-de-endpoints-crud)
6. [Diseño y Ejemplos de Peticiones / Respuestas](#-diseño-y-ejemplos-de-peticiones--respuestas)
7. [Inyección de Dependencias (`Depends()`)](#-inyección-de-dependencias-depends)
8. [Estrategia de Manejo de Errores y Excepciones (`HTTPException`)](#-estrategia-de-manejo-de-errores-y-excepciones-httpexception)
9. [Evidencias de Aprendizaje y Pruebas (Capturas)](#-evidencias-de-aprendizaje-y-pruebas-capturas)
10. [Reflexión Final sobre la Evolución](#-reflexión-final-sobre-la-evolución)

---

## 🏛️ DESCRIPCIÓN GENERAL Y ARQUITECTURA

La API `device_systems` está diseñada bajo los principios de la **Arquitectura Limpia (Clean Architecture)** y **RESTful API Best Practices**. El sistema divide las tareas en capas lógicas independientes. 

Esto garantiza que la lógica de negocio (cómo se procesa un usuario) esté completamente aislada de la capa de transporte (cómo se reciben las peticiones HTTP), lo que facilita enormemente la migración futura a bases de datos reales o la implementación de pruebas unitarias automatizadas.

---

## 📂 ESTRUCTURA DEL PROYECTO (SEPARACIÓN DE RESPONSABILIDADES)

El árbol de directorios del proyecto se organiza de forma vertical y limpia de la siguiente manera:

```text
device_systems/
│── app/
│   │── __init__.py                # Inicializador del paquete Python
│   │── main.py                    # Punto de entrada de la aplicación y metadatos globales
│   │
│   │── data/
│   │   │── __init__.py
│   │   └── users_db.py            # Capa de Datos: Simulación persistente de BD en memoria RAM
│   │
│   │── dependencies/
│   │   │── __init__.py
│   │   └── user_dependencies.py   # Capa de Intercepción: Validaciones transversales con Depends()
│   │
│   │── routes/
│   │   │── __init__.py
│   │   └── user_routes.py         # Capa de Enrutamiento: Define endpoints, métodos HTTP y tags
│   │
│   │── schemas/
│   │   │── __init__.py
│   │   └── user_schema.py         # Capa de Validación: Modelos de Pydantic para entrada/salida
│   │
│   └── services/
│       │── __init__.py
│       └── user_service.py        # Capa de Negocio: Lógica interna del CRUD
│
│── requirements.txt               # Manifiesto de dependencias del ecosistema
│── README.md                      # Manual técnico de la aplicación (Este archivo)
