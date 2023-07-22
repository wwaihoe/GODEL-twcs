from flask import Flask, request, render_template, jsonify
import GODEL_twcs, GODEL_twcs_AppleSupport, GODEL_twcs_SpotifyCares, db, sqlite3


def create_app():
    app = Flask(__name__, template_folder="templates")
    db.init_app(app)
    return app

app = create_app()
app.config.update(
    DATABASE = 'sqldb.db',
    TEMPLATES_AUTO_RELOAD = True
)

def page_not_found(e):
  return render_template('404.html'), 404

app.register_error_handler(404, page_not_found)

@app.route('/', methods = ['POST', 'GET', 'DELETE'])
def index():
    con = sqlite3.connect('sqldb.db')
    cur = con.cursor()
    curr_chat_id = 0
    res = cur.execute("SELECT chat_id FROM chat ORDER BY chat_id DESC LIMIT 1")
    row = res.fetchone()
    if row is None:
        curr_chat_id = 1
    else:
        curr_chat_id = row[0] + 1
    con.close()
    # Instruction for a chitchat task
    instruction = f"Instruction: given a dialog context, provide a helpful response."
    # Leave the knowldge empty
    knowledge = ""
    dialog = []
    if request.method == 'POST':
        user_input = request.get_json()
        dialog.append(user_input['user_dialog'])
        res = {}
        output = GODEL_twcs.generate(instruction, knowledge, dialog)
        dialog.append(output)
        res['output'] = output
        con = sqlite3.connect('sqldb.db')
        cur = con.cursor()
        cur.execute("INSERT INTO chat (author_id, chatbot, chat_id, query, response) values (?, ?, ?, ?, ?)", (0, "General" , curr_chat_id, user_input['user_dialog'], output))
        con.commit()
        con.close()
        return jsonify(res), 200
    if request.method == 'DELETE':
        dialog.clear()
        curr_chat_id += 1
    return render_template('index.html')

@app.route('/apple_support', methods = ['POST', 'GET', 'DELETE'])
def GODEL_twcs_AppleSupport_chat():
    con = sqlite3.connect('sqldb.db')
    cur = con.cursor()
    curr_chat_id = 0
    res = cur.execute("SELECT chat_id FROM chat ORDER BY chat_id DESC LIMIT 1")
    row = res.fetchone()
    if row is None:
        curr_chat_id = 1
    else:
        curr_chat_id = row[0] + 1
    con.close()
    # Instruction for a chitchat task
    instruction = f"Instruction: given a dialog context, provide a helpful response."
    # Leave the knowldge empty
    knowledge = ""
    dialog = []
    if request.method == 'POST':
        user_input = request.get_json()
        dialog.append(user_input['user_dialog'])
        res = {}
        output = GODEL_twcs_AppleSupport.generate(instruction, knowledge, dialog)
        dialog.append(output)
        res['output'] = output
        con = sqlite3.connect('sqldb.db')
        cur = con.cursor()
        cur.execute("INSERT INTO chat (author_id, chatbot, chat_id, query, response) values (?, ?, ?, ?, ?)", (0, "AppleSupport" , curr_chat_id, user_input['user_dialog'], output))
        con.commit()
        con.close()
        return jsonify(res), 200
    if request.method == 'DELETE':
        dialog.clear()
        curr_chat_id += 1
    return render_template('apple_support.html')

@app.route('/spotify_cares', methods = ['POST', 'GET', 'DELETE'])
def GODEL_twcs_SpotifyCares_chat():
    con = sqlite3.connect('sqldb.db')
    cur = con.cursor()
    curr_chat_id = 0
    res = cur.execute("SELECT chat_id FROM chat ORDER BY chat_id DESC LIMIT 1")
    row = res.fetchone()
    if row is None:
        curr_chat_id = 1
    else:
        curr_chat_id = row[0] + 1
    con.close()
    # Instruction for a chitchat task
    instruction = f"Instruction: given a dialog context, provide a helpful response."
    # Leave the knowldge empty
    knowledge = ""
    dialog = []
    if request.method == 'POST':
        user_input = request.get_json()
        dialog.append(user_input['user_dialog'])
        res = {}
        output = GODEL_twcs_SpotifyCares.generate(instruction, knowledge, dialog)
        dialog.append(output)
        res['output'] = output
        con = sqlite3.connect('sqldb.db')
        cur = con.cursor()
        cur.execute("INSERT INTO chat (author_id, chatbot, chat_id, query, response) values (?, ?, ?, ?, ?)", (0, "SpotifyCares" , curr_chat_id, user_input['user_dialog'], output))
        con.commit()
        con.close()
        return jsonify(res), 200
    if request.method == 'DELETE':
        dialog.clear()
        curr_chat_id += 1
    return render_template('spotify_cares.html')

@app.route('/info')
def info():
    return render_template('info.html')

if __name__ == '__main__':
    app.run()