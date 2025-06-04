# Projeto_Final_Python

A. Estrutura do Projeto.

├── .idea
├── .venv
├── static
├── templates
│   ├── alterar_termo.html
│   ├── deletar_termo.html
│   ├── duvidas.html
│   ├── funcoes_procedimentos.html
│   ├── glossario.html
│   ├── index.html
│   ├── login.html
│   ├── modelo.html
│   ├── novo_termo.html
│   ├── repeticao.html
│   ├── search_results.html
│   ├── selecao.html
│   ├── sobre_equipe.html
│   ├── tratamento.html
│   └── usuario.html
│   └── vetores_matrizes.html
├── app.py
├── bd_glossario.csv
├── Suggestions.csv
└── Users.csv

B. Tecnologias usadas Foram: Python, Flask, Html ( CSS, Javascript).
Flask foi usado para definir as rotas do site ( URLs) e as funções do Python
que serão executadas quando as rotas forem acessadas via HTML para formar os códigos
das páginas a serem navegadas , CSS para estilizar a aparência do site,
Javascript para adicionar funcionalidades interativas em cada página.
Foram utilizadas .CSV como banco de dados de Glossário, 
Sugestões para o Site e Login e senha de usuários cadastrados.


C. Utilizamos a ajudante do google Devs para implantação API Gemini Ai, instalando o pip install -q -U google-genai e fazendo a importação  do Genai from Google,
adicionamos código ao Flask e tivemos que criar e adicionar a API Key para funcionamento do código do Gemini.

D. Após a integração de todas as rotas no flask, utilizamos o App.py e damos "Start"
que ele irá exacutar todo Aplicativo/Site.
Com isso, o Flask faz a ligação de rotas em todas as Abas do Site.

E. Importamos .CSV no Glossário, Usuário e Sugestões para ser adicionado um banco de dados ao nosso projeto e guardar todas informações das páginas referidas. Em usuários, adicionamos a ultilização de login e senha para caso tenham interesse em serem administradores ou enviar sugestões de melhorias para o site. Ao glóssario adicionamos a ultilização de senha para adicionar,alterar ou deletar termo.

- Implantamos uma navegação para pesquisar  qualquer conteúdo no site e fazer uma breve
exposição para que vpcê veja se é esse conteúdo a ser acessado e você usuário possa ir até ele.

- Ao menu um breve conteúdo de python com as principais funcionalidades, 
funções e procedimentos e algumas estruturas com exemplos.

- No Glossário importamos uma navegação direta no dicionario de termos, onde o usuário terá acesso a todo glossário adicionado, com seus termos e definições e os administradores, poderam apagar/alterar ou adicionar termos. Também adicionamos um filtro de pesquisa para que o usuário possa pesquisar direto um conteúdo especifico na aba e filtrando automáticamente por palavras relacionadas.

- - Se o usuário tiver interesse no assunto ele poderá fazer o cadastro/login e enviar algumas 
sugestões, e pedido para ser moderador e ter acesso a alteração do glossário para adicionar seus 
termos e algumas coisas que ele ache que seja necessário.





