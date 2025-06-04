import csv
import os
import re
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, send_from_directory

from google import genai

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'super secret key')  # Use env variable or default

# Initialize Gemini client using environment variable for API key
GENAI_API_KEY = os.getenv("GENAI_API_KEY", "Troque pela sua API Key")
client = genai.Client(api_key=GENAI_API_KEY)


def call_gemini_api(question):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=question
        )
        return response.text
    except Exception as e:
        return f"Erro ao chamar a API: {e}"


def extract_text_from_html(html_content):
    # Remove script and style tags
    html_content = re.sub(r'&lt;script.*?&gt;.*?&lt;/script&gt;', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'&lt;style.*?&gt;.*?&lt;/style&gt;', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    # Remove all HTML tags
    text = re.sub(r'&lt;.*?&gt;', '', html_content)
    # Decode HTML entities
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'")
    # Replace multiple spaces and newlines by one space
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# User management functions

def user_exists(username):
    try:
        with open('users.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 3 and row[0] == username:
                    return True
    except FileNotFoundError:
        return False
    return False


def validate_user(username, password):
    try:
        with open('users.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 3 and row[0] == username and row[2] == password:
                    return True
    except FileNotFoundError:
        return False
    return False


def save_user(username, email, password, birthdate):
    with open('users.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([username, email, password, birthdate])


@app.route('/')
def ola():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # Verifica se o usuário existe e se a senha está correta
        if user_exists(username) and validate_user(username, password):
            return redirect('/usuario')
        else:
            flash('Usuário ou senha incorretos.', 'error')
            return redirect(url_for('login'))


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('newUsername', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('newPassword', '').strip()
    birthdate = request.form.get('birthdate', '').strip()

    if user_exists(username):
        flash('Nome de usuário já existe. Escolha outro.', 'error')
        return redirect(url_for('login'))

    save_user(username, email, password, birthdate)
    flash('Cadastro realizado com sucesso!', 'success')
    return redirect(url_for('login'))


# Serve usuario.html page with render_template
@app.route('/usuario')
def usuario_page():
    return render_template('usuario.html')


@app.route('/sobre-equipe')
def sobre_equipe():
    return render_template('sobre_equipe.html')


@app.route('/selecao')
def selecao():
    return render_template('selecao.html')


@app.route('/repeticao')
def repeticao():
    return render_template('repeticao.html')


@app.route('/vetores-matrizes')
def vetores_matrizes():
    return render_template('vetores_matrizes.html')


@app.route('/funcoes-procedimentos')
def funcoes_procedimentos():
    return render_template('funcoes_procedimentos.html')


@app.route('/tratamento')
def tratamento():
    return render_template('tratamento.html')


@app.route('/glossario')
def glossario():
    glossario_de_termos = []
    with open('bd_glossario.csv', 'r', newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for linha in reader:
            glossario_de_termos.append(linha)
    return render_template('glossario.html', glossario=glossario_de_termos)


@app.route('/novo-termo')
def novo_termo():
    return render_template('novo_termo.html')


@app.route('/criar_termo', methods=['POST'])
def criar_termo():
    termo = request.form['termo'].strip()
    definicao = request.form['definicao'].strip()

    if not termo or not definicao:
        flash('Termo e definição não podem estar vazios.', 'error')
        return redirect(url_for('novo_termo'))

    with open('bd_glossario.csv', 'a', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerow([termo, definicao])

    flash(f'O termo "{termo}" foi adicionado ao glossário!', 'success')
    return redirect(url_for('glossario'))


@app.route('/deletar_termo', methods=['POST'])
def deletar_termo():
    termo_para_deletar = request.form['termo_para_deletar'].strip()
    if not termo_para_deletar:
        flash('Termo para deletar não pode estar vazio.', 'error')
        return redirect(url_for('glossario'))

    termos_atualizados = []
    try:
        with open('bd_glossario.csv', 'r', newline='', encoding='utf-8') as arquivo_leitura:
            reader = csv.reader(arquivo_leitura, delimiter=';')
            for linha in reader:
                if linha and linha[0] != termo_para_deletar:
                    termos_atualizados.append(linha)
        with open('bd_glossario.csv', 'w', newline='', encoding='utf-8') as arquivo_escrita:
            writer = csv.writer(arquivo_escrita, delimiter=';')
            writer.writerows(termos_atualizados)
        flash(f'O termo "{termo_para_deletar}" foi deletado do glossário!', 'success')
    except FileNotFoundError:
        flash('Erro: O arquivo do glossário não foi encontrado.', 'error')
    except Exception as e:
        flash(f'Ocorreu um erro ao deletar o termo: {e}', 'error')
    return redirect(url_for('glossario'))


@app.route('/alterar_termo/<termo>', methods=['GET'])
def alterar_termo(termo):
    termo = termo.strip()
    termo_encontrado = None
    try:
        with open('bd_glossario.csv', 'r', newline='', encoding='utf-8') as arquivo:
            reader = csv.reader(arquivo, delimiter=';')
            for linha in reader:
                if linha and linha[0] == termo:
                    termo_encontrado = linha
                    break
        if termo_encontrado is None:
            flash(f'Termo "{termo}" não encontrado.', 'error')
            return redirect(url_for('glossario'))
    except FileNotFoundError:
        flash('Arquivo do glossário não encontrado.', 'error')
        return redirect(url_for('glossario'))
    return render_template('alterar_termo.html', termo=termo_encontrado[0], definicao=termo_encontrado[1])


@app.route('/salvar_termo_alterado', methods=['POST'])
def salvar_termo_alterado():
    termo_original = request.form['termo_original'].strip()
    termo_novo = request.form['termo'].strip()
    definicao_nova = request.form['definicao'].strip()

    if not termo_novo or not definicao_nova:
        flash('Termo e definição não podem estar vazios.', 'error')
        return redirect(url_for('alterar_termo', termo=termo_original))

    termos_atualizados = []
    termo_encontrado = False
    try:
        with open('bd_glossario.csv', 'r', newline='', encoding='utf-8') as arquivo_leitura:
            reader = csv.reader(arquivo_leitura, delimiter=';')
            for linha in reader:
                if linha:
                    if linha[0] == termo_original:
                        termos_atualizados.append([termo_novo, definicao_nova])
                        termo_encontrado = True
                    else:
                        termos_atualizados.append(linha)
        if not termo_encontrado:
            flash(f'Termo original "{termo_original}" não encontrado.', 'error')
            return redirect(url_for('glossario'))
        with open('bd_glossario.csv', 'w', newline='', encoding='utf-8') as arquivo_escrita:
            writer = csv.writer(arquivo_escrita, delimiter=';')
            writer.writerows(termos_atualizados)
        flash(f'O termo "{termo_original}" foi alterado para "{termo_novo}".', 'success')
    except FileNotFoundError:
        flash('Arquivo do glossário não encontrado.', 'error')
    except Exception as e:
        flash(f'Ocorreu um erro ao salvar a alteração: {e}', 'error')

    return redirect(url_for('glossario'))


@app.route('/duvidas', methods=['GET', 'POST'])
def duvidas():
    resposta_gemini = None
    pergunta = None
    error = None
    if request.method == 'POST':
        pergunta = request.form['pergunta']
        if pergunta:
            resposta_gemini = call_gemini_api(pergunta)
        else:
            error = "A pergunta não pode estar vazia."
    return render_template('duvidas.html', resposta=resposta_gemini, pergunta=pergunta, error=error)


@app.route('/search')
def search():
    query = request.args.get('query', '').strip()
    results = []

    # Define o mapeamento das rotas para os arquivos/templates e títulos amigáveis
    paginas = {
        'sobre_equipe': {'file': 'templates/sobre_equipe.html', 'title': 'Sobre a Equipe'},
        'selecao': {'file': 'templates/selecao.html', 'title': 'Seleção'},
        'repeticao': {'file': 'templates/repeticao.html', 'title': 'Repetição'},
        'vetores_matrizes': {'file': 'templates/vetores_matrizes.html', 'title': 'Vetores e Matrizes'},
        'funcoes_procedimentos': {'file': 'templates/funcoes_procedimentos.html', 'title': 'Funções e Procedimentos'},
        'tratamento': {'file': 'templates/tratamento.html', 'title': 'Tratamento'},
        'duvidas': {'file': 'templates/duvidas.html', 'title': 'Dúvidas'},
        'glossario': {'file': 'templates/glossario.html', 'title': 'Glossário'},
        'novo_termo': {'file': 'templates/novo_termo.html', 'title': 'Novo Termo'},
        'login': {'file': 'templates/login.html', 'title': 'Login'},
        'user_page': {'file': None, 'title': 'Usuário'}  # user_page is dynamic, skip content search
    }

    if query:
        # Pesquisa no glossário
        with open('bd_glossario.csv', 'r', newline='', encoding='utf-8') as arquivo:
            reader = csv.reader(arquivo, delimiter=';')
            for linha in reader:
                if linha and (query.lower() in linha[0].lower() or query.lower() in linha[1].lower()):
                    preview = linha[1][:100] + ('...' if len(linha[1]) > 100 else '')
                    results.append({'type': 'glossario', 'title': linha[0], 'content': linha[1], 'preview': preview})

        # Pesquisa no conteúdo das páginas HTML da pasta templates
        for route_name, info in paginas.items():
            path = info.get('file')
            title = info.get('title')
            if path and os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    text_content = extract_text_from_html(html_content)
                    # Busca expressão simples case-insensitive
                    if query.lower() in text_content.lower():
                        # Extrai trecho ao redor da query para preview
                        idx = text_content.lower().find(query.lower())
                        start = max(idx - 50, 0)
                        end = min(idx + 50, len(text_content))
                        preview = text_content[start:end]
                        preview = preview.strip()
                        if start > 0:
                            preview = '... ' + preview
                        if end < len(text_content):
                            preview = preview + ' ...'
                        results.append({
                            'type': route_name,
                            'title': title,
                            'content': f'Clique aqui para ver {title}.',
                            'preview': preview
                        })
                except Exception as e:
                    # Se der erro ao abrir ou ler, ignore e continue
                    pass

        # Pesquisa simples no nome das páginas para aumentar chances de resultado
        if 'dúvidas'.find(query.lower()) != -1 and not any(r['type'] == 'duvidas' for r in results):
            results.append({'type': 'duvidas', 'title': 'Dúvidas', 'content': 'Clique aqui para ver as dúvidas.',
                            'preview': 'Veja as perguntas frequentes sobre o tema.'})

        if 'seleção'.find(query.lower()) != -1 and not any(r['type'] == 'selecao' for r in results):
            results.append({'type': 'selecao', 'title': 'Seleção', 'content': 'Clique aqui para ver a seleção.',
                            'preview': 'Veja a lista de itens selecionados.'})

    return render_template('search_results.html', query=query, results=results)


# Rota para enviar sugestões
@app.route('/submit_suggestion', methods=['POST'])
def submit_suggestion():
    username = request.form['username']
    suggestion_type = request.form['suggestion_type']
    suggestion = request.form['suggestion']

    add_suggestion(username, suggestion_type, suggestion)
    return jsonify({'message': 'Sugestão enviada com sucesso!'}), 200


# Função para adicionar uma nova sugestão
def add_suggestion(username, suggestion_type, suggestion):
    with open('suggestions.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([username, suggestion_type, suggestion])


if __name__ == '__main__':
    app.run(debug=True)
