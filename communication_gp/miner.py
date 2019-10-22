import hashlib
import requests

import sys

import json


# TODO: Implement functionality to search for a proof

def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes
    :return: A valid proof for the provided block
    """

    block_string = json.dumps(block, sort_keys=True).encode()

    proof = 0
    while valid_proof(block_string, proof) is False:
        proof += 1

    return proof


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """

    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    # TODO: Change back to six zeroes
    return guess_hash[:6] == "000000"


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        print("starting loop")
        # TODO: Get the last block from the server and look for a new one
        r = requests.get(url=node+'/last_block')
        last_block = r.json()
        new_proof = proof_of_work(last_block['last_block'])

        print(f"Found Proof and submitting it:{new_proof}")
        # TODO: When found, POST it to the server {"proof": new_proof}
        post_data = {"proof": new_proof}
        r = requests.post(url=node+"/mine", json=post_data)
        data = r.json()
        print(data)
        # TODO: We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        pass
