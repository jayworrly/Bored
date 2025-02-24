from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://api.avax.network/ext/bc/C/rpc'))

if w3.is_connected():
    print('Connected')
else:
    print('Not Connected')
abi = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view", 
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_spender", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_from", "type": "address"},
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transferFrom",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {"name": "_owner", "type": "address"},
            {"name": "_spender", "type": "address"}
        ],
        "name": "allowance",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "owner", "type": "address"},
            {"indexed": True, "name": "spender", "type": "address"},
            {"indexed": False, "name": "value", "type": "uint256"}
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "from", "type": "address"},
            {"indexed": True, "name": "to", "type": "address"},
            {"indexed": False, "name": "value", "type": "uint256"}
        ],
        "name": "Transfer",
        "type": "event"
    }
]
def send_tokens(from_address, private_key, to_address, amount, token_address):
    # Create contract instance for the specific token
    token_contract = w3.eth.contract(address=Web3.to_checksum_address(token_address), abi=abi)
    
    # Get nonce (required for transaction)
    nonce = w3.eth.get_transaction_count(from_address)
    
    # Build transaction
    token_tx = token_contract.functions.transfer(
        Web3.to_checksum_address(to_address),
        Web3.to_wei(amount, 'ether')
    ).build_transaction({
        'chainId': 43114,  # AVAX C-Chain
        'gas': 100000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce,
    })

    # Sign transaction
    signed_tx = w3.eth.account.sign_transaction(token_tx, private_key)
    
    # Send transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    return tx_receipt

from_addr = ""  # Your wallet address
priv_key = ""  # Replace with your actual private key
to_addr = ""  # Recipient address
token_addr = ""  # Token contract address
amount = '' # Amount of tokens to send

# Loop 5 times to send tokens back and forth
for i in range(5):
    if i % 2 == 0:
        # Send from from_addr to to_addr
        print(f"\nTransaction {i+1}: Sending from {from_addr} to {to_addr}")
        receipt = send_tokens(from_addr, priv_key, to_addr, amount, token_addr)
        print(f"Transaction hash: {receipt['transactionHash'].hex()}")
    else:
        # Send from to_addr back to from_addr
        print(f"\nTransaction {i+1}: Sending from {to_addr} to {from_addr}")
        receipt = send_tokens(to_addr, priv_key, from_addr, amount, token_addr)
        print(f"Transaction hash: {receipt['transactionHash'].hex()}")

receipt = send_tokens(from_addr, priv_key, to_addr, amount, token_addr)
print(f"Transaction hash: {receipt['transactionHash'].hex()}")
