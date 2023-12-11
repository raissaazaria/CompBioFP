# app.py
from flask import Flask, render_template, request
from Bio.KEGG.REST import kegg_get

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/explore_pathway', methods=['POST'])
def explore_pathway():
    pathway_id = request.form.get('pathway_id')
    pathway_info = kegg_get(pathway_id).read()
    return render_template('result.html', pathway_info=pathway_info)

if __name__ == '__main__':
    app.run(debug=True) 
