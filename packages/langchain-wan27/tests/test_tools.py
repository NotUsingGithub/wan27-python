import unittest
from unittest.mock import Mock
from wan27 import Wan27, Wan27Error
from langchain_wan27 import create_wan27_tools


class ToolTests(unittest.TestCase):
    def setUp(self):
        self.client = Mock(spec=Wan27)

    def test_default_tools_have_no_generation_or_credentials(self):
        tools = create_wan27_tools(self.client)
        self.assertEqual(len(tools),6)
        self.assertNotIn("wan27_generate_media",[t.name for t in tools])
        for tool in tools:
            self.assertNotIn("token", tool.args)

    def test_discovery_and_estimate_invoke_client(self):
        tools = {t.name:t for t in create_wan27_tools(self.client)}
        self.client.models.return_value = {"models":[]}
        self.assertEqual(tools["wan27_list_models"].invoke({}),{"models":[]})
        request = {"modelId":"wan2.7-image","prompt":"boat"}
        tools["wan27_estimate_generation"].invoke({"input":request})
        self.client.estimate.assert_called_once_with(request)
        self.client.generate.assert_not_called()

    def test_enabled_generation_keeps_request_id(self):
        tools = {t.name:t for t in create_wan27_tools(self.client,allow_generation=True)}
        request = {"modelId":"wan2.7-image","prompt":"boat"}
        tools["wan27_generate_media"].invoke({"input":request,"request_id":"12345678-1234-1234-1234-123456789abc"})
        self.client.generate.assert_called_once_with(request,request_id="12345678-1234-1234-1234-123456789abc")

    def test_errors_are_not_reported_as_success(self):
        self.client.account.side_effect = Wan27Error("SUBSCRIPTION_REQUIRED","Subscription required",403)
        tool = create_wan27_tools(self.client)[0]
        with self.assertRaises(Wan27Error): tool.invoke({})


if __name__ == "__main__": unittest.main()
