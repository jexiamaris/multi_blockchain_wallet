from constants import *
import subprocess
import json
import os
from dotenv import load_dotenv
load_dotenv()
import bit
from bit import wif_to_key
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI



mnemonic = os.getenv('MNEMONIC')
btc_priv_key= os.getenv('BTC_PRIV_KEY')

def derive_wallets(crypto, mnemonic=mnemonic, n_derive=3):
    command = f'php Wallet/hd-wallet-derive/hd-wallet-derive.php -g --mnemonic="{mnemonic}" --cols=path,address,privkey,pubkey --coin={crypto} --numderive={n_derive} --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    keys = json.loads(output)
    return keys

coins= {'eth': derive_wallets(ETH),
    'btc-test': derive_wallets(BTCTEST)}


def  priv_key_to_account(coin, priv_key):
    if coin== ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin== BTCTEST:
        return PrivateKeyTestnet(priv_key)

def create_tx(coin, account, to, amount):
    if coin== ETH:
        value= w3.toWei(amount, "ether") 
        gasEstimate = w3.eth.estimateGas({ "to": to, "from": account.address, "amount": value })
        return {'to': to,
            'from': account.address,
            'value': value,
            'gas': gasEstimate,
            'gas_price': w3.eth.generateGasPrice(),
            'nonce': w3.eth.getTransactionCount(account.address),
            'chainID': w3.net.chainId}

    elif coin== BTCTEST:
        
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])

def send_tx (coin, account, to, amount):
    tx = create_tx(coin, account, to, amount)
    signed_tx = account.sign_transaction(tx)
    print(f"send_tx {coin, account, to, amount}")
    if coin== ETH:
        return w3.eth.sendRawTransaction(signed_tx.rawTransaction)

    elif coin== BTCTEST:
        return NetworkAPI.broadcast_tx_testnet(signed_tx) 
    
account = priv_key_to_account(BTCTEST, btc_priv_key)

    
send_dragan_BTC= send_tx(BTCTEST, account,  "miH2nBqm9g85vtufeyVUbhmBP4znziV3tW", 0.0000067)
print(send_dragan_BTC)
