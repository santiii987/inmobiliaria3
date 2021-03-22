from main import app

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/madness_app'

#ROUTES --------------------------------
# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/profile')
# def profile():
#     return render_template('profile.html')

# @app.route('/admin')
# def admin_page():
#     return render_template('admin.html')

#SERVER SETUP (DEBUGGER)-------------------------------
if __name__ == '__main__':
    app.run(port=3000, debug=True)
