from flask import Flask, render_template, request, redirect, url_for, session
import secrets

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Inisialisasi data pemilihan (kandidat dan hasil)
candidates = {
    1: {"name": "SYIFATUROBANI", "votes": 0},
    2: {"name": "ZAKI TRI PAMUNGKAS", "votes": 0},
    3: {"name": "RIO THE JENERO", "votes": 0}
}

# Informasi admin (secara nyata Anda harus mengelola ini dengan lebih aman)
admin_username = "admin"
admin_password = "adminpass"

# Halaman login admin
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == admin_username and password == admin_password:
            session['admin_logged_in'] = True
            return redirect(url_for('results'))
    return render_template('admin_login.html')

# Halaman hasil - hanya bisa diakses oleh admin
@app.route('/results')
def results():
    if 'admin_logged_in' in session:
        sorted_candidates = sorted(candidates.items(), key=lambda x: x[1]['votes'], reverse=True)
        return render_template('results.html', sorted_candidates=sorted_candidates)
    return redirect(url_for('admin_login'))

# Halaman utama - formulir pemilihan dengan kode akses
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'access_code' in session and request.form.get('access_code') == session['access_code']:
            selected_candidate = int(request.form['candidate'])
            candidates[selected_candidate]['votes'] += 1
            return redirect(url_for('index'))
    else:
        # Generate random access code and store it in session
        access_code = secrets.token_urlsafe(8)  # Generate an 8-character random string
        session['access_code'] = access_code

    return render_template('index.html', candidates=candidates, access_code=session['access_code'])

# Logout admin
@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
