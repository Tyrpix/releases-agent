import json
import unittest
import main
import responses
from datetime import datetime


class TestMain(unittest.TestCase):

    def test_payload(self):
        now = datetime.now()
        expected_result = {
            "service": "test",
            "date": now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
            "environment": "testing",
            "eventType": "deployment",
            "message": "Deployed Version: v.1.0"

        }
        result = main.payload("test", "v.1.0", "testing")
        self.assertTrue(result, expected_result)

    def test_parse_json(self):
        data = {
            "cloudformation_template_version": "v0.0.79",
            "deployer_name": "deploy-with-docktor",
            "deployer_principal": "jenkins-orchestrator",
            "deployer_version": "0.186.0",
            "environment": "development",
            "event_date_time": "2020-05-21T12:36:23.953Z",
            "event_type": "deployment-complete",
            "lambda_name": "ecs-mdtp-deployer-protected",
            "lambda_version": "v0.1.269",
            "mdtp_zone": "protected",
            "microservice": "test-service",
            "microservice_version": "0.82.0",
            "slug_uri": "test",
            "stack_id": "test"
        }

        expected_result = {
            "service_name": "test-service",
            "version": "0.82.0",
            "environment": "development"
        }
        result = main.parse_json(json.dumps(data))
        self.assertEqual(result, expected_result)

        result = main.parse_json("x")
        self.assertEqual(result, None)

    @responses.activate
    def test_send_to_timeline(self):
        pass
