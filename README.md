
README - Implementando HATEOAS com FastAPI em Python
Introdução

Neste documento, vamos explorar como implementar HATEOAS (Hypertext as the Engine of Application State) em uma API RESTful usando FastAPI, um framework web rápido para Python.
O que é HATEOAS?

HATEOAS é um princípio de arquitetura de API RESTful que permite aos clientes de API navegarem pela API usando hiperlinks fornecidos pela API. Isso torna a API mais autoexplicativa, reduz a necessidade de que o cliente conheça as URLs exatas e facilita a evolução da API.
Pré-requisitos

Certifique-se de que você tenha o Python e o FastAPI instalados em seu ambiente. Você pode instalá-los usando o seguinte comando:

### **Python:**
Instale o python e crie um ambiente virtual:

```bash
# crie o ambiente virtual venv
~ python3 -m venv venv
#ative o ambiente virtual
~ source venv/bin/activate
```
Implementação

Vamos criar uma API simples para gerenciar uma lista de tarefas. Nossas tarefas terão links para ações que podem ser realizadas com elas.
1. Criando a API

Crie um arquivo Python chamado app.py com o seguinte código:

python
```bash
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Task(BaseModel):
    title: str
    description: str

tasks = []

@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    tasks.append(task)
    return task

@app.get("/tasks/", response_model=List[Task])
def read_tasks():
    return tasks
```
2. Adicionando Links HATEOAS

Vamos adicionar links HATEOAS para cada tarefa. Edite o arquivo app.py para incluir isso:

```bash

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Task(BaseModel):
    title: str
    description: str

tasks = []

@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    tasks.append(task)
    task_dict = task.dict()
    task_dict["links"] = [{"rel": "self", "href": f"/tasks/{len(tasks) - 1}"}]
    return task_dict

@app.get("/tasks/", response_model=List[Task])
def read_tasks():
    task_list = []
    for i, task in enumerate(tasks):
        task_dict = task.dict()
        task_dict["links"] = [{"rel": "self", "href": f"/tasks/{i}"}]
        task_list.append(task_dict)
    return task_list

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    task_dict = tasks[task_id].dict()
    task_dict["links"] = [{"rel": "self", "href": f"/tasks/{task_id}"}]
    return task_dict
```
Agora, cada tarefa possui um link "self" que aponta para sua própria URL.
Executando a aplicação

Para iniciar a aplicação FastAPI, execute o seguinte comando no terminal:

```bash

uvicorn app:app --reload
```
Isso iniciará o servidor de desenvolvimento. Agora você pode acessar a API em http://localhost:8000 e explorar os links HATEOAS das tarefas.
Conclusão

Neste documento, aprendemos a implementar HATEOAS em uma API RESTful usando FastAPI em Python. A inclusão de links HATEOAS torna a API mais autoexplicativa e facilita a interação do cliente com a API. Você pode expandir esses conceitos para criar APIs mais complexas e ricas em recursos. Para mais informações sobre FastAPI e HATEOAS, consulte a documentação oficial.
