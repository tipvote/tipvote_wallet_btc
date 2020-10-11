
from app import db
import requests
import json
from walletconfig import url

from app.models import BtcWalletAddresses


def generate_addresses():

    # query amount addresses that are not uses
    get_available_addresses = db.session.query(BtcWalletAddresses)\
        .filter(BtcWalletAddresses.status == 0)\
        .count()

    # see if less than 50
    if get_available_addresses <= 50:

        # make a 100 new addresses
        for f in range(100):

            # call the rpc
            newwalletaddress = callforaddress()
            if newwalletaddress["error"] is None:
                # get the new address
                the_address = newwalletaddress["result"]

                # add to db addresses
                walletadd = BtcWalletAddresses(
                    btcaddress=the_address,
                    status=0,
                     )

                db.session.add(walletadd)

        db.session.commit()
    else:
        print(f"We have {get_available_addresses} addresses available still.  No need to run")


def callforaddress():

    # standard json header
    headers = {'content-type': 'application/json'}

    # the method/params
    rpc_input = {
        "method": "getnewaddress",
    }

    # add standard rpc values
    rpc_input.update({"jsonrpc": "1.0", "id": "0"})

    # execute the rpc request
    response = requests.post(
        url,
        data=json.dumps(rpc_input),
        headers=headers,
    )

    # the response in json format
    response_json = response.json()
    print(response_json)
    return response_json


if __name__ == '__main__':
    generate_addresses()