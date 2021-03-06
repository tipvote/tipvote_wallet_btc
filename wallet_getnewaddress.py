from app import db

from app.models import \
    BtcWallet, \
    TransactionsBtc, \
    BtcWalletAddresses


def getnewaddress(user_id):

    """
    THIS function gets a new address for the user

    :param user_id:
    :return:
    """

    userswallet = db.session.query(BtcWallet) \
        .filter_by(user_id=user_id) \
        .first()
    walletaddress = db.session.query(BtcWalletAddresses) \
        .filter(BtcWalletAddresses.status == 0) \
        .first()

    # Test to see if user doesnt have any current incomming transactions..get new one if not
    incdeposit = db.session.query(TransactionsBtc) \
        .filter(TransactionsBtc.category == 3,
                TransactionsBtc.confirmed == 0,
                TransactionsBtc.user_id == user_id) \
        .first()

    if incdeposit is None:
        # status 0 = not used
        # status 1 = current main
        # status 2 = used
        if userswallet.address1status == 1:
            userswallet.address1status = 2
            userswallet.address2 = walletaddress.btcaddress
            userswallet.address2status = 1
            userswallet.address3status = 0

            walletaddress.user_id = user_id
            walletaddress.status = 1

        elif userswallet.address2status == 1:
            userswallet.address2status = 2
            userswallet.address3 = walletaddress.btcaddress
            userswallet.address3status = 1
            userswallet.address1status = 0

            walletaddress.user_id = user_id
            walletaddress.status = 1

        elif userswallet.address3status == 1:
            userswallet.address3status = 2
            userswallet.address1 = walletaddress.btcaddress
            userswallet.address1status = 1
            userswallet.address2status = 0

            walletaddress.user_id = user_id
            walletaddress.status = 1

        elif userswallet.address3status == 0 \
                and userswallet.address2status == 0 \
                and userswallet.address1status == 0:
            userswallet.address3status = 2
            userswallet.address1 = walletaddress.btcaddress
            userswallet.address1status = 1
            userswallet.address2status = 0

            walletaddress.user_id = user_id
            walletaddress.status = 1

        elif userswallet.address3status == 1 \
                and userswallet.address2status == 1 \
                and userswallet.address1status == 1:
            userswallet.address3status = 2
            userswallet.address1 = walletaddress.btcaddress
            userswallet.address1status = 1
            userswallet.address2status = 0

            walletaddress.user_id = user_id
            walletaddress.status = 1

        elif userswallet.address3status == 2 \
                and userswallet.address2status == 2 \
                and userswallet.address1status == 2:
            userswallet.address3status = 2
            userswallet.address1 = walletaddress.btcaddress
            userswallet.address1status = 1
            userswallet.address2status = 0

            walletaddress.user_id = user_id
            walletaddress.status = 1

        elif userswallet.address3status == 3 \
                and userswallet.address2status == 3 \
                and userswallet.address1status == 3:
            userswallet.address3status = 2
            userswallet.address1 = walletaddress.btcaddress
            userswallet.address1status = 1
            userswallet.address2status = 0

            walletaddress.user_id = user_id
            walletaddress.status = 1

        else:
            userswallet.address3status = 2
            userswallet.address1 = walletaddress.btcaddress
            userswallet.address1status = 1
            userswallet.address2status = 0

            walletaddress.user_id = user_id
            walletaddress.status = 1

        db.session.add(userswallet)
        db.session.add(walletaddress)
        db.session.commit()
