### Documentação: Esteira CI/CD para Build e Teste com GitHub Actions

(Integração Contínua / Entrega Contínua)** configurada para automatizar o **build**, **execução dos testes unitários** e a **validação do código** no repositório GitHub. A esteira foi configurada usando **GitHub Actions** e **Docker** para garantir que a aplicação esteja funcionando corretamente antes de ser implantada ou movida para a próxima etapa.

---

### Visão Geral

A esteira de CI/CD tem como objetivo:

1. **Construir uma imagem Docker** com a aplicação.
2. **Executar os testes unitários** dentro da imagem Docker.
3. **Validar o código** garantindo que a aplicação esteja funcionando corretamente.

### Estrutura do Workflow

O workflow do GitHub Actions é configurado no arquivo `.github/workflows/ci.yml`, e é composto por uma série de etapas que são executadas sempre que houver um **push** ou **pull request** para a branch `dev`.

### Arquivo do Workflow

~~~yml
name: CI - Run Tests

on:

  push:

    branches:

      - dev

  pull_request:

    branches:

      - dev

jobs:

  run-tests:

    runs-on: ubuntu-latest
  

    steps:

      - name: Checkout repository

        uses: actions/checkout@v2


      - name: Set up Docker

        uses: docker/setup-buildx-action@v2


      - name: Build Docker image

        run: |

          docker build -t my-app:latest .


      - name: Run Unit Tests

        run: |

          docker run my-app:latest python -m unittest discover -s tests
~~~

### Etapas do Workflow

#### 1. **Acionamento do Workflow**

O workflow é acionado automaticamente nos seguintes cenários:

- **`push` para a branch `dev`**: Quando um commit é enviado para a branch `dev`.
- **`pull_request` para a branch `dev`**: Quando uma pull request é criada com destino à branch `dev`.

#### 2. **Job `run-tests`**

O job `run-tests` é o processo responsável por garantir que os testes sejam executados após a construção da imagem Docker. Esse job é dividido em quatro etapas principais.

##### **2.1. Checkout do Repositório**

`- name: Checkout repository   uses: actions/checkout@v2`

- **Objetivo**: Baixar o código do repositório para o runner do GitHub Actions, para garantir que a versão mais recente do código-fonte seja utilizada no build e nos testes.

##### **2.2. Configuração do Docker**

`- name: Set up Docker   uses: docker/setup-buildx-action@v2`

- **Objetivo**: Configurar o **Docker Buildx**, uma ferramenta avançada para construção de imagens Docker que oferece funcionalidades como suporte a multiplataformas e cache de construção.

##### **2.3. Construção da Imagem Docker**

`- name: Build Docker image   run: |     docker build -t my-app:latest .`

- **Objetivo**: Construir a imagem Docker usando o **Dockerfile** localizado no repositório. A imagem gerada será etiquetada como `my-app:latest`. A imagem contém a aplicação e todas as suas dependências.

##### **2.4. Execução dos Testes Unitários**

`- name: Run Unit Tests   run: |     docker run my-app:latest python -m unittest discover -s tests`

- **Objetivo**: Rodar os testes unitários dentro da imagem Docker construída na etapa anterior. O comando `python -m unittest discover -s tests` procura e executa todos os testes na pasta `tests`. Se algum teste falhar, o workflow será interrompido e o código não será implantado.

#### 3. **Resultado da Execução**

- **Se todos os testes passarem**: A esteira de CI/CD completará com sucesso, indicando que o código está pronto para ser implantado (em uma etapa posterior).
- **Se algum teste falhar**: A execução dos testes será interrompida, e o status do workflow indicará erro. Nesse caso, o código não será implantado ou movido para qualquer outra etapa até que os problemas sejam corrigidos.

---

### Como Funciona o Processo

1. **Commit ou Pull Request**: Quando você faz um `push` para a branch `dev` ou cria uma `pull request` para a mesma branch, o GitHub aciona o workflow de CI/CD.
2. **Checkout do código**: O GitHub Actions baixa o código mais recente do repositório.
3. **Construção da Imagem Docker**: A imagem Docker da aplicação é construída.
4. **Execução dos Testes**: Os testes unitários são executados dentro da imagem Docker para garantir que tudo esteja funcionando corretamente.
5. **Resultado**: Se os testes passarem, o workflow é considerado bem-sucedido. Caso contrário, o processo é interrompido, e os desenvolvedores devem corrigir os erros antes de tentar novamente.

### Conclusão

A esteira de CI/CD configurada com **GitHub Actions** e **Docker** facilita o processo de **build** e **testes** automatizados para garantir que o código da aplicação esteja sempre funcional antes de ser movido para o próximo estágio (deploy). A execução dos testes unitários após a construção da imagem Docker ajuda a identificar problemas de forma rápida e eficiente, melhorando a qualidade do software.

#### Como testar a API?

Esta API permite requisições GET, POST e PUT. Para testá-la, utilize as seguintes URLs, substituindo <método> pelo verbo HTTP desejado (GET, POST ou PUT):

- **Produtos:** dev-ops-lab-beta.vercel.app/produtos/<método>
    
- **Categorias:** dev-ops-lab-beta.vercel.app/categorias/<método>
    
- **Login:** dev-ops-lab-beta.vercel.app/login (requisição POST com admin como usuário e senha).
    

**Para requisições POST:** Você precisará enviar um corpo de requisição com os dados apropriados para a operação. A estrutura do corpo dependerá de cada endpoint. Consulte a documentação da API para mais detalhes sobre os formatos esperados.

**Exemplo (usando curl para uma requisição GET):**

      `curl dev-ops-lab-beta.vercel.app/produtos`

**Exemplo (usando curl para uma requisição POST de login):**

      `curl -X POST -H "Content-Type: application/json" -d '{"usuario": "admin", "senha": "admin"}' dev-ops-lab-beta.vercel.app/login`
    

**Recomendações:**

- Utilize uma ferramenta como Postman, curl ou Insomnia para testar os endpoints de forma mais eficiente. Estas ferramentas permitem configurar facilmente headers, corpos de requisição e visualizar as respostas da API.
    
- Consulte a documentação completa da API (se disponível) para obter informações detalhadas sobre cada endpoint, incluindo os parâmetros esperados e os formatos de resposta.
    

