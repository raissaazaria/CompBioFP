# app.py
from flask import Flask, render_template, request
from Bio.KEGG.REST import kegg_get
import re

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/explore_pathway', methods=['POST'])
def explore_pathway():
    pathway_id = request.form.get('pathway_id')
    pathway_info = kegg_get(pathway_id).read()
    
    pathway_info = pathway_info.split('\n')
    
    pathway_info_list = []
    for path in pathway_info:
        parts = re.split(r'\s+', path)
        parts = [part for part in parts if part]
        if len(parts) > 1:
            heading = parts[0]
            content = parts[1:]
            result_content = ' '.join(content)
            res_dict = {heading:result_content}
            pathway_info_list.append(res_dict)

    pathway_info_dict = {}
    for dic in pathway_info_list:
        for key, value in dic.items():
            if key in pathway_info_dict:
                pathway_info_dict[key].append(value)
            else:
                pathway_info_dict[key] = [value]

    for key, values in pathway_info_dict.items():
        print(f'{key} || {values}')
    
    return render_template('result.html', pathway_info_dict=pathway_info_dict)

if __name__ == '__main__':
    app.run(debug=True)
