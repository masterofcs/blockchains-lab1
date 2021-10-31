import random

import txhandler
import utxo
from transaction import Transaction
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA256
import utils
def init():
    hau_address = RSA.generate(1024)
    hieu_address = RSA.generate(1024)
    print(hau_address.public_key())
    tx = Transaction.NewCoinbase(100, hau_address.public_key())
    tx.addInput(tx.getRawTx(), 0)
    tx.addSignature(sign(tx.getRawDataToSign(0), RSA.construct((hau_address.n, hau_address.e, hau_address.d))), 0)
    utxo_pool = utxo.UTXOPool()
    utxo_init = utxo.UTXO(tx.hash, 0)
    utxo_pool.addUTXO(utxo_init, tx.getOutput(0))


    tx2 = Transaction()

    tx2.addInput(tx.hash, 0)

    tx2.addOutput(50, hieu_address.public_key())
    tx2.addOutput(30, hieu_address.public_key())

    tx2.addSignature(sign(tx2.getRawDataToSign(0), RSA.construct((hau_address.n, hau_address.e, hau_address.d))), 0)

    tx_handler = txhandler.TxHandler(utxo_pool)
    print(tx_handler.isValidTx(tx2))



def sign(M, K):
    signer = PKCS1_v1_5.new(K)
    signature = signer.sign(SHA256.new(M))
    return signature




if __name__ == '__main__':
    init()