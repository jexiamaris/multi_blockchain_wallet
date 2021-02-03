from constants import *
import subprocess
import json
import os
from dotenv import load_dotenv
load_dotenv()
from constants import *
from bit import wif_to_key

mnemonic = os.getenv('MNEMONIC')

def derive_wallets(crypto, mnemonic=mnemonic, n_derive=3):
    command = f'php Blockchain-Tools-Wallet/hd-wallet-derive/hd-wallet-derive.php -g --mnemonic="{mnemonic}" --cols=path,address,privkey,pubkey --coin={crypto} --numderive={n_derive} --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    print(command)
    keys = json.loads(output)
    return keys

coins= {'eth': derive_wallets(ETH),
    'btc-test': derive_wallets(BTCTEST)}
print(coins)

def  priv_key_to_account(coin, priv_key):
    if coin== ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin== BTCTEST:
        return PrivateKeyTestnet(priv_key)

def create_tx(coin, account, to, amount):
    if coin== ETH:
        value= w3.toWei(amount, "ether") # convert 1.2 ETH to 120000000000 wei
        gasEstimate = w3.eth.estimateGas({ "to": to, "from": account.address, "amount": value })
        return {'to'= to,
            'from'= account.address,
            'value'= value
            'gas'= gasEstimate,
            'gas_price'= w3.eth.generateGasPrice(),
            'nonce'= w3.eth.getTransactionCount(account.address),
            'chainID'= w3.net.chainId}

    elif coin== BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])

def send_tx (coin, account, to, amount):
    tx = create_tx(coin, account, to, amount)
    signed_tx = account.sign_transaction(tx)
    if coin== ETH:
        return w3.eth.sendRawTransaction(signed_tx.rawTransaction)

    elif coin== BTCTEST
        return NetworkAPI.broadcast_tx_testnet(signed) 
    
