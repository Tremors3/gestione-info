<style>
    ul {
        list-style-type: "▶"; /* Rimuove i punti di default */
        padding-left: 40px; /* Rimuove il padding predefinito */
        margin-left: 0px; /* Rimuove il margin predefinito */
    }

    ul li {
        padding: 10px; /* Imposta il padding desiderato */
        line-height: 20px; /* Imposta l'altezza fissa per le righe */
        transition: cubic-bezier(.09,.33,.03,1.01) background-color 1s; /* Aggiunge una transizione fluida */
    }

    ul li:hover {
        background-color: #373b3e; /* Cambia colore dello sfondo al passaggio del mouse */
    }
</style>

# Progetto Gestione dell'Informazione

Questo progetto si propone di sviluppare un sistema di gestione dell'informazione che consenta di `<specifiche>`. L'obiettivo principale è fornire agli utenti `<obiettivo del progetto>`, migliorando così `<benefici attesi>`.

<br />

## ✅ Funzionalità Principali

- Funzionalità 1
  
- Funzionalità 1

- Funzionalità 3

<br />

## ✅ Tecnologie Utilizzate
Le tecnologie e gli strumenti utilizzati per lo sviluppo del progetto includono:

- *[Flask](https://en.wikipedia.org/wiki/Flask_(web_framework))*,
  *[Flask-Blueprints](https://flask.palletsprojects.com/en/3.0.x/blueprints/)*
  
- *[Nltk](https://www.nltk.org/)*, ...

<br />

## ✅ Setup

### 👉 Start in Windows
- Passo 1

    ```cmd
    ```

### 👉 Start in Unix/Linux
- Passo 1

    ```bash
    ```

### 👉 Start in MacOS
- Passo 1

    ```bash
    ```

<br />

## ✅ Codebase <!-- https://symbl.cc/en/unicode/blocks/box-drawing/ -->

Questo progetto è stato programmato utilizzando `blueprints` e una struttura intuitiva presentata qua sotto: 

```bash
<gestione-info/project/...>
    │
    ├─── app/
    │    │
    │    ├─── home/                          
    │    │    └─── routes.py                  
    │    │
    │    ├─── authentication/                
    │    │    ├─── routes.py                  
    │    │    ├─── models.py                  
    │    │    └─── forms.py                   
    │    │
    │    ├─── static/
    │    │    └─── <css, JS, images>          
    │    │
    │    ├─── templates/                       
    │    │    ├─── includes/                   
    │    │    │    ├─── navigation.html        
    │    │    │    ├─── sidebar.html           
    │    │    │    ├─── footer.html            
    │    │    │    └─── scripts.html           
    │    │    │
    │    │    ├─── layouts/                    
    │    │    │    ├─── base-fullscreen.html   
    │    │    │    └─── base.html              
    │    │    │
    │    │    └─── home/                       
    │    │         ├─── index.html             
    │    │         ├─── 404-page.html          
    │    │         └─── *.html                 
    │    │    
    │    ├─── config.py                              
    │    └─── __init__.py                            
    │
    ├─── requirements.txt                      
    ├─── .env                                  
    └─── run.py                                
```
