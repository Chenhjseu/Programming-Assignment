from flask import Flask
from flask_restful import reqparse, fields, abort, Api, Resource, marshal_with
import pandas as pd
from flasgger import Swagger


def get_filtered_df(df, args):
    """
    process the data to extract the required ones
    :param df: dataset input
    :param args: filters
    :return: filtered df
    """
    filtered_df = df
    for key, value in args.items():
        if key not in df.columns:
            abort(400, message="Column {} doesn't exist".format(key))
            return
        if value:
            filtered_df = filtered_df[filtered_df[key].isin(value)]
    return filtered_df


def get_statistics(df):
    """
    :param df: filtered df
    :return: json format statistical information
    """

    entries = len(df)
    avg = df.mean()
    median = df.median()
    var = df.var()
    std = df.std()

    output = {'entries': entries,
              'avg': avg,
              'median': median,
              'var': var,
              'std': std}

    return output


app = Flask(__name__)
api = Api(app)

# file parser
task_df = pd.read_excel('data/task_data.xls')
sales_df = pd.read_csv('data/sales_data.csv', sep=';', thousands=',', dtype={'Sales': 'int'}, encoding='unicode_escape')


class Sales(Resource):
    output_fields = {'entries': fields.Integer,
                     'avg': fields.Float,
                     'median': fields.Float,
                     'var': fields.Float,
                     'std': fields.Float
                     }

    @marshal_with(output_fields)
    def get(self):
        """To get the analyzed values
    ---
    schemes:
      - http
    parameters:
      - name: kwargs
        type: string
        required: false
        description: parameters as filters (i.e. "Country" "City", "Customer ID"))
    responses:
      200:
        description: successful return
      400:
        description: Params error
    """
        parser = reqparse.RequestParser(bundle_errors=True)
        for column in sales_df.columns:
            parser.add_argument(column, action='append')
        args = parser.parse_args()
        if args:
            filtered_df = get_filtered_df(sales_df, args)
        return get_statistics(filtered_df['Sales'])


class Task(Resource):
    output_fields = {'entries': fields.Integer,
                     'avg': fields.Float,
                     'median': fields.Float,
                     'var': fields.Float,
                     'std': fields.Float
                     }

    @marshal_with(output_fields)
    def get(self):
        """To get the analyzed values
    ---
    schemes:
      - http
    parameters:
      - name: kwargs
        type: string
        required: false
        description: parameters as filters (i.e. "Country" "City", "Customer ID"))
    responses:
      200:
        description: successful return
      400:
        description: Params error
    """
        parser = reqparse.RequestParser(bundle_errors=True)
        for column in task_df.columns:
            parser.add_argument(column, action='append')
        args = parser.parse_args()
        if args:
            filtered_df = get_filtered_df(task_df, args)
        return get_statistics(filtered_df['Time_used'])


api.add_resource(Task, '/task')
api.add_resource(Sales, '/sales')

# Swagger config setting
swagger_config = Swagger.DEFAULT_CONFIG
swagger_config['title'] = 'Programming Assignment'
swagger_config[
    'description'] = 'This API could be used by passing the input parameters to extract specific data and get the statistical values.'
swagger_config['host'] = 'localhost:5000'
swagger = Swagger(app, config=swagger_config)

if __name__ == '__main__':
    app.run(debug=True)
