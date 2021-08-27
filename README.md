# Controle de clientes e serviços  
## Aplicativo para cadastro de clientes e serviços  

Essa é a primeira versão.  
Novas funcionalidades serão implementadas em breve.  

### Features

- [x] Cadastro de usuário (pelo admin)
- [x] Cadastro de cliente
- [x] Cadastro de produtos
- [ ] Cadastro de tabela de serviços
- [ ] Relatórios

### Dependências

É necessário ter o Python 3 instalado e o framework django.  
Caso não tenha o django instalado, digite no terminal:  
`pip install Django`  

### Inicialização

`python manage.py runserver`  

## Instruções de uso

No terminal, navegue até a pasta do app e digite: `python manage.py createsuperuser`.  
*Dessa forma, é possível criar o usuário para acessar as configurações do app.*  

### Passos iniciais

1. Vá até as configurações do app para cadastrar os **mensageiros** que seus clientes utilizam e os possíveis **status** que os serviços podem ter.  
2. Cadastre primeiramente o cliente, antes de registrar o serviço.  
3. Por fim, cadastre o serviço selecionando o cliente que contratou o serviço.