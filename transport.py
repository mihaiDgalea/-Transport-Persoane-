from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import psycopg2.extras

app = Flask('Transport Persoane app')
app.secret_key = "cairocoders-ednalan"

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="myw0r1d")


def average(p):
    if len(p) == 0:
        return 0
    return round(sum(p) / len(p), 2)


@app.route('/')
@app.route('/acasa/')
def show_home():
    """Se arata home template"""

    return render_template('acasa.html')


@app.route('/grafic/')
def grafic():
    """ Se afiseaza graficul cu toti soferii, rute si vehicule"""
    with conn:
        query = """
                select
                    s.id, s.trs_id, concat(s.nume,' ', s.prenume),
                    t.id, t.masina, t.nr_masina, t.traseul
                from soferi s
                join traseul t on s.trs_id = t.id
                order by s.nume;
                """
        c = conn.cursor()
        c.execute(query)
        records = c.fetchall()

    return render_template('grafic.html', grafic=records, title=grafic)


@app.route('/soferi/')
def soferi():
    """Aratati toti soferii"""

    with conn:
        query = """
            select
                s.id, concat(s.nume, ' ', s.prenume),
                t.id, concat(t.nr_masina)
            from soferi s
            join traseul t on s.trs_id = t.id
            order by s.nume;
        """
        c = conn.cursor()
        c.execute(query)
        records = c.fetchall()

    return render_template('soferi.html', title='Soferi', soferi=records)


@app.route('/soferi/<int:soferi_id>/')
def sofer(soferi_id):
    """Se arata soferul cu sofer_id-ul dat"""

    with conn:
        query = """
            select
                s.id, s.nume, s.prenume,
                concat(t.nr_masina),concat(t.masina),concat(t.traseul)
            from soferi s
            join traseul t on s.trs_id = t.id
            where s.id = %s::integer;
        """
        c = conn.cursor()
        c.execute(query, (soferi_id,))
        record = c.fetchone()
        if record:
            title = f'{record[1]} {record[2]} {record[0]}'
        else:
            title = 'Sofer inexistent'

    return render_template('sofer.html', title=title, sofer=record)


@app.route('/search/', methods=['GET', 'POST'])
def cauta_soferi():
    """Se cauta soferii după un nume dat"""

    if request.method == 'POST':
        srch = request.form
    else:
        srch = request.args

    search = srch.get('search').strip().upper()

    with conn:
        query = """
            select
                s.id, concat(s.nume, ' ', s.prenume),
                t.id, t.traseul
            from soferi s
            join traseul t on s.trs_id = t.id
            where s.nume like %s or s.prenume like %s;
        """

        c = conn.cursor()
        c.execute(query, (f'%{search}%', f'%{search}%'))
        records = c.fetchall()

    return render_template('soferi.html', title='Sofer', soferi=records, search=search)


@app.route('/adauga/')
def adauga():
    """Se arata  templates adauga """

    return render_template('adauga.html')


@app.route('/administratie/')
def index():
    """Afișează  intreaga administratie"""

    with conn:
        query = """
            select
                s.id, s.nume, s.prenume, s.trs_id
            from soferi s 
            order by s.nume;
            """
        c = conn.cursor()
        c.execute(query)
        records = c.fetchall()

    return render_template('administratie.html', index=records, title='Administratie')


@app.route('/add_soferi/', methods=['GET', 'POST'])
def add_soferi():
    """Se adauga soferi"""

    nume1 = request.form['nume']
    prenume1 = request.form['prenume']
    marca = request.form['trs_id']
    if not nume1 or not prenume1 or not marca:
        error_statement = "Toate campurile trebuiesc completate"
        return render_template('adauga.html', error_statement=error_statement,
                               nume=nume1,
                               prenume=prenume1,
                               marca=marca)

    if request.method == 'POST':
        nume1 = request.form['nume'].upper()
        prenume1 = request.form['prenume'].upper()
        marca = request.form['trs_id']
        cond = (nume1, prenume1, marca)

        with conn:
            query = """
                insert into soferi 
                     (nume, prenume, trs_id)
                values (%s, %s, %s) returning id
                """
            c = conn.cursor()
            c.execute(query, cond)
            conn.commit()
            records = c.fetchone()
            return redirect(url_for('sofer', soferi_id=records[0]))


@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def get_marca(id):
    """Se marca soferului"""

    c = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    c.execute('select * from soferi s  where s.id = %s ', (id,))
    data = c.fetchall()
    c.close()
    return render_template('edit.html', marca=data[0])


@app.route('/update/<int:id>', methods=['POST'])
def update_marca(id):
    """Se modifica marca soferului"""

    if request.method == 'POST':
        marca = request.form['trs_id']

        c = conn.cursor()
        c.execute("""
            update soferi
            set trs_id = %s
            where id = %s
            returning id
        """, (marca, id))
        flash('Marca modificata')
        conn.commit()
        records = c.fetchone()
        return redirect(url_for('sofer', soferi_id=records[0]))


@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_sofer(id):
    """Se sterge un sofer"""

    with conn:
        query = """
            delete from soferi where id = {0}
        """
        c = conn.cursor()
        c.execute(query.format(id))
        conn.commit()
        flash('Sofer sters')
        return redirect(url_for('index'))


@app.route('/rute/')
def rute():
    """Se arată toată rutele"""

    with conn:
        query = """
            select id, t.traseul
            from traseul t
            order by t.traseul, t.masina;
        """
        c = conn.cursor()
        c.execute(query)
        records = c.fetchall()

    return render_template('rute.html', rute=records, title='Rute')


@app.route('/traseul/<trs_id>/')
def tras(trs_id):
    """Se afiseaza traseul cu trs_id-ul dat"""

    with conn:
        query = """
            select
                s.id, concat(s.nume, ' ', s.prenume),
                concat(t.traseul,t.nr_masina)
            from soferi s
            join traseul t on s.trs_id = t.id
            where t.id = %s::integer;
        """
        c = conn.cursor()
        c.execute(query, (trs_id,))
        records = c.fetchall()
        if records:
            traseul = records[0][2]
        else:
            traseul = None

    return render_template('traseul.html', soferi=records, traseul_name=traseul, title='Traseul' + traseul[0:3])


@app.errorhandler(404)
def pagina_negasita(e):
    """Se prinde route inexistente"""
    return render_template('errors/404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
