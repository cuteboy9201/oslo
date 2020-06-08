from oslo.web.httpclient import Request

client = Request()
client.set_method("GET")
client.set_domain("api.kuaiwan.com")
client.set_uri_pattern("/sms/send/")
client.add_uri_params("phonenumber", 17600878987)
client.add_uri_params("typecode", "sms_rerpassword")
client.set_protocol_type("https")
client.set_port = 443
req = client.fetch()
code, head, content = req.get_response_object()
print(code, head, content)
