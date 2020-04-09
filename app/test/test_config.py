import os
import unittest

from flask import current_app
from flask_testing import TestCase

from manage import app
from config import basedir


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'postgres://hvqhidstfdeetm:9ca3a9492da4d277312046186f7cc8c969602fa377ff107d8b60048beb9eedde@ec2-34-202-7-83.compute-1.amazonaws.com:5432/d5khtdmlbch2t0'
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(
            #app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///' + os.path.join(basedir, 'test.db')
            app.config['SQLALCHEMY_DATABASE_URI'] == 'postgres://hvqhidstfdeetm:9ca3a9492da4d277312046186f7cc8c969602fa377ff107d8b60048beb9eedde@ec2-34-202-7-83.compute-1.amazonaws.com:5432/d5khtdmlbch2t0'
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()