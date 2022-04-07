from paypalcheckoutsdk.orders import OrdersCreateRequest
from tools.paypalClient import PaypalClient

RETURN_URL = "http://127.0.0.1:5000/usercenter"
CANCEL_URL = "http://127.0.0.1:5000/cart"


class CreateOrder(PaypalClient):

    @staticmethod
    def build_request_body(currency_code, value):
        print("currency_code is:", currency_code)
        return \
            {
                "intent": "CAPTURE",
                "application_context": {
                    "return_url": RETURN_URL,
                    "cancel_url": CANCEL_URL,
                    "brand_name": "M-FIT",
                    "landing_page": "BILLING",
                },
                "purchase_units": [
                    {
                        "amount": {
                            "currency_code": currency_code,
                            "value": value
                        }
                    }
                ]
            }

    def create_order(self, currency_code, value, debug=False):
        request = OrdersCreateRequest()
        request.headers['prefer'] = 'return=representation'
        request.request_body(self.build_request_body(currency_code, value))
        response = self.client.execute(request)
        if debug:
            print("Status code:", response.status_code)
            print("Status:", response.result.status)
            print("Order ID:", response.result.id)
            print("intent:", response.result.intent)
            print("links:")
            for link in response.result.links:
                print("\t{}: {}\tCall Type: {}".format(link.rel, link.href, link.method))
            print("total Amount: {} {}".format(response.result.purchase_units[0].amount.currency_code,
                                               response.result.purchase_units[0].amount.value))
        return response
