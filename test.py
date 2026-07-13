import os
import pickle
import unittest

import numpy as np

from app import FEATURE_FIELDS, SCALER_PATH, MODEL_PATH, app


class FlaskTest(unittest.TestCase):

    # check for the response 200
    def test_route(self):
        tester = app.test_client(self)
        response = tester.get('/')
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # test for content type
    def test_content(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    # test for post request data
    def test_post_request(self):
        tester = app.test_client(self)
        info = {field: 1 for field in FEATURE_FIELDS}
        response = tester.post("/", data=info)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Given water sample is', response.data)

    # test for models
    def test_model(self):
        val = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.assertTrue(os.path.exists(MODEL_PATH))
        self.assertTrue(os.path.exists(SCALER_PATH))
        with open(MODEL_PATH, 'rb') as model_file:
            model = pickle.load(model_file)
        with open(SCALER_PATH, 'rb') as scaler_file:
            scc = pickle.load(scaler_file)
        data = scc.transform([val])
        # make a prediction for the given data
        res = model.predict(data)
        self.assertEqual(res.shape, (1,))
        self.assertIn(res[0], [0, 1])


if __name__ == "__main__":
    unittest.main()
