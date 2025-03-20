import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

from task.app import get_app
from task.api.products import ProductsApi
from task.extensions import db, appbuilder

if __name__ == "__main__":

    app = get_app()
    with app.app_context():
        db.init_app(app)
        appbuilder.init_app(app, session=db.session)
        appbuilder.add_api(ProductsApi)

    app.run(port=8000)