from flask_appbuilder import AppBuilder, SQLA

db = SQLA()
appbuilder = AppBuilder(session=db.session)