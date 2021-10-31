import utxo
from utxo import UTXOPool
from transaction import Transaction
from crypto import Crypto

class TxHandler:
    """
    Creates a public ledger whose current UTXOPool (collection of unspent transaction outputs) is {@code pool}.
    """
    def __init__(self, pool: UTXOPool):
        # IMPLEMENT THIS
        self.__pool = pool

    """
    @return true if:
    (1) all outputs claimed by {@code tx} are in the current UTXO pool, 
    (2) the signatures on each input of {@code tx} are valid, 
    (3) no UTXO is claimed multiple times by {@code tx},
    (4) all of {@code tx}s output values are non-negative, and
    (5) the sum of {@code tx}s input values is greater than or equal to the sum of its output
        values; and false otherwise.
    """
    def isValidTx(self, tx: Transaction) -> bool:
        # IMPLEMENT THIS
        usedUTOX = []
        sum_input = 0
        sum_output = 0
        for trans_input in tx.numInputs():
            input_data = tx.getInput(trans_input)
            output_index = input_data.outputIndex
            pre_hash = input_data.prevTxHash
            signature = input_data.signature
            utxo_verify = utxo.UTXO(pre_hash, output_index)
            output_data = tx.getOutput()
            """
            (1) all outputs claimed by {@code tx} are in the current UTXO pool, 
            """
            if not self.__pool.contains(utxo_verify):
                return False
            """
            Valid all signature
            """
            if not Crypto.verifySignature(output_data.address, tx.getRawDataToSign(output_index), signature):
                return False
            """no UTXO is claimed multiple times by {@code tx}"""
            if usedUTOX.__contains__(utxo_verify):
                return False
            usedUTOX.append(utxo_verify)
            sum_input+=output_data.value
        for trans_output in tx.numOutputs():
            output_data = tx.getOutput(trans_output)
            if output_data.value < 0:
                return False
            sum_output += output_data.value
        if sum_input < sum_output:
            return False
        return True


    """
    Handles each epoch by receiving an unordered array of proposed transactions, checking each
    transaction for correctness, returning a mutually valid array of accepted transactions, and
    updating the current UTXO pool as appropriate.
    """
    def handleTxs(self, txs):
        # IMPLEMENT THIS
        for tx in txs:
            if self.isValidTx(tx):
                self.__pool.getTxOutput(tx)
        return False