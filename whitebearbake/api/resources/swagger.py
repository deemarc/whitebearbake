# Module imports
from apispec import APISpec
from apispec.ext.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import current_app


# App imports
from compute.api.v1 import bp


class BlueprintPlugin(FlaskPlugin):
    """ Customized FlaskPlugin """
    def path_helper(self, view, **kwargs):
        """ Customized path helper with prefix stripping """
        path = super().path_helper(view)
        path.path = path.path.replace(kwargs.get('strip', ''), '')
        return path


def add_blueprint_paths(spec, blueprint, exclude=(), strip=None):
    """ Registers Flask routes on blueprint to spec """
    bp_name = blueprint.name
    for rule in current_app.url_map.iter_rules():
        prefix, sep, endpoint = rule.endpoint.partition('.')
        if prefix == bp_name and endpoint not in exclude:
            spec.add_path(view=current_app.view_functions[rule.endpoint], strip=strip)


@bp.route('/swagger.json', methods=['GET'])
def swagger():
    """ Returns swagger spec JSON """
    # Create an APISpec
    spec = APISpec(
        # **config['APISPEC']['v1'],
        plugins=[
            BlueprintPlugin(),
            MarshmallowPlugin(),
        ],
        # version=config.get('APP_VERSION')
    )

    # Register jSend schema definitions and paths
    # spec.definition('jSendResponse', schema=jSendSchema, description='jSend response wrapper schema')


    # Add all paths for blueprint to spec
    add_blueprint_paths(spec, bp, strip='/api')

    # Return formatted spec
    return spec.to_dict()
