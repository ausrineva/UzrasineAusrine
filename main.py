from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Temporary storage for notes
uzrasai_atmintyje = []


@app.route('/', methods=['GET', 'POST'])
def notebook():
    if request.method == 'POST':
        vardas = request.form.get('vardas')
        uzrasas = request.form.get('uzrasas')
        if uzrasas:  # Ensure that the note is not empty
            uzrasai_atmintyje.append((vardas, uzrasas))
        return redirect(url_for('notebook'))

    return render_template('uzrasine.html', uzrasai=uzrasai_atmintyje)


if __name__ == '__main__':
    app.run(debug=True)
