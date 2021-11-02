import random
import time

import txhandler
import utxo
from transaction import Transaction
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from Cryptodome import Random
import utils
def init():
    random_generator = Random.new().read
    hau_address = RSA.generate(1024, random_generator)
    hau_pri = hau_address.export_key()
    hau_public = hau_address.public_key()
    print(f'Hau public {hau_public}')
    hieu_address = RSA.generate(1024, random_generator)
    hieu_pri = hieu_address.export_key()


    base_coin = Transaction.NewCoinbase(100, hau_public)
    tx = Transaction.NewCoinbase(100, hau_public)
    tx.addInput(base_coin.getRawTx(), 0)
    tx.addSignature(sign(tx.getRawDataToSign(0), hau_pri), 0)
    tx.finalize()
    utxo_pool = utxo.UTXOPool()
    utxo_init = utxo.UTXO(tx.hash, 0)
    utxo_pool.addUTXO(utxo_init, tx.getOutput(0))


    tx2 = Transaction()
    hieu_public = hieu_address.public_key()
    print(f'Hieu pub {hieu_public}')
    tx2.addInput(tx.hash, 0)
    tx2.addOutput(1, hieu_public)
    tx2.addOutput(5, hieu_address.public_key())
    tx2.addOutput(5, hieu_address.public_key())
    # utxo_pool.addUTXO(utxo.UTXO(tx2), tx.getOutput(0))
    # utxo_pool.addUTXO(utxo_init, tx.getOutput(0))
    tx2.addSignature(sign(tx2.getRawDataToSign(0), hau_pri), 0)
    tx2.finalize()
    tx_handler = txhandler.TxHandler(utxo_pool)
    print(tx_handler.isValidTx(tx2))

    tx2.addOutput(90, hieu_public)
    tx2.addSignature(sign(tx2.getRawDataToSign(0), hau_pri), 0)
    print(tx_handler.isValidTx(tx2))



def sign(M, K):

    key = RSA.import_key(K)
    signer = pkcs1_15.new(key)
    signature = signer.sign(SHA256.new(M))
    print(f'Sign: {key.public_key()} with {M} and {signature}')
    return signature




if __name__ == '__main__':
    init()