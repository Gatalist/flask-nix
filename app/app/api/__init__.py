from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec


# create docs api
def apispec_docs(app: object):
    docs = FlaskApiSpec()
    docs.init_app(app)
    # swagger settings
    app.config.update({
        'APISPES_SPEC': APISpec(
            title='Video',
            version='v1',
            openapi_version='2.0',
            plugins=[MarshmallowPlugin()],
        ),
        'APISPEC_SWAGGER_URL': '/swagger/'
    })

    return docs, app
