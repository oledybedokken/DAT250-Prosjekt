from flask import Flask, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_required
from flask_bcrypt import Bcrypt
from flask_admin import helpers as admin_helpers
from flask_admin import Admin
from datetime import datetime, timedelta
from .models import db
from flask_admin.contrib.sqla import ModelView
from flask_security import Security, SQLAlchemyUserDatastore

admin = Admin()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.database'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECURITY_PASSWORD_SALT'] = 'OLEGAY'
    app.permanent_session_lifetime = timedelta(days=5)
    db.init_app(app)
    #admin.init_app(app)
    #login_manager = LoginManager()
    #login_manager.login_view = 'auth.login'
    #login_manager.init_app(app)
    from .models import User, Transaction, BankAccount, Roles


    user_datastore = SQLAlchemyUserDatastore(db, User, Roles)
    security = Security(app, user_datastore)

    @app.before_first_request
    def create_user():
        #db.drop_all()
        db.create_all()
        #user_datastore.create_user(email='admin', password='admin')
        db.session.commit()

    admin = Admin(app, name='Admin', base_template='my_master.html', template_mode='bootstrap3')

    class UserModelView(ModelView):
        def is_accessible(self):
            return(current_user.is_active and current_user.is_authenticated)

        def _handle_view(self, name):
            if not self.is_accessible():
                return redirect(url_for('security.login'))
    
    # Add administrative views to Flask-Admin
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(UserModelView(Transaction, db.session))
    admin.add_view(UserModelView(BankAccount, db.session))

    # Add the context processor
    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template = admin.base_template,
            admin_view = admin.index_view,
            get_url = url_for,
            h = admin_helpers
        )

    @app.route('/tiss')
    def index():
        return render_template('index-admin.html')
    #@login_manager.user_loader
    #def load_user(user_id):
    #    return User.query.get(int(user_id))

    with app.app_context():
        # blueprint for auth routes in our app
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        # blueprint for non-auth parts of app
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        # Create Database Models
        db.create_all()
        
        return app