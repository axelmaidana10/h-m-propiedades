from flask import Flask, render_template, request, redirect, url_for
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

app = Flask(__name__)
app.secret_key = "hym_secret_key_web"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.context_processor
def inject_supabase_config():
    # Estas variables se inyectan en el HTML para el JavaScript.
    return dict(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)

@app.route('/')
def home():
    try:
        # Se cargan 6 propiedades destacadas
        response = supabase.table('propiedades').select('*, imagenes(url)').order('created_at', desc=True).limit(6).execute()
        propiedades = response.data
    except Exception:
        propiedades = []
    return render_template('index.html', propiedades=propiedades)

@app.route('/propiedad/<int:id>')
def detalle(id):
    try:
        response = supabase.table('propiedades').select('*, imagenes(url)').eq('id', id).single().execute()
        propiedad = response.data
    except Exception:
        return redirect(url_for('home'))
    return render_template('detalle.html', p=propiedad)

@app.route('/catalogo')
def catalogo():
    tipo = request.args.get('tipo')
    estado = request.args.get('estado')
    query = supabase.table('propiedades').select('*, imagenes(url)')
    if tipo: query = query.eq('tipo', tipo)
    if estado: query = query.eq('estado', estado)
    response = query.execute()
    return render_template('index.html', propiedades=response.data, filtro_activo=True)

# Rutas de Autenticación
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)