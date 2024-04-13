from flask import Flask, request, render_template, redirect, url_for
from collections import defaultdict

app = Flask(__name__)

# Change to a dictionary with the user's name as key and a list of their notes as value
uzrasai_atmintyje = defaultdict(list)


@app.route('/', methods=['GET', 'POST'])
def notebook():
    if request.method == 'POST':
        vardas = request.form.get('vardas')
        uzrasas = request.form.get('uzrasas')
        if vardas and uzrasas:  # Ensure that the name and the note are not empty
            uzrasai_atmintyje[vardas].append(uzrasas)
        return redirect(url_for('notebook'))

    return render_template('uzrasine.html', uzrasai=uzrasai_atmintyje)


@app.route('/archyvas', methods=['GET'])
def archyvas():
    # Sort the archive by user name
    sorted_uzrasai = dict(sorted(uzrasai_atmintyje.items()))
    return render_template('archyvas.html', uzrasai=sorted_uzrasai)


if __name__ == '__main__':
    app.run(debug=True)
