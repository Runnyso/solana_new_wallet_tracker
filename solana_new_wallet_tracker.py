import requests, time

def track_new_wallets():
    print("Tracking brand new Solana wallets with first tx > $10k")
    seen = set()
    while True:
        r = requests.get("https://api.solscan.io/account/list?sort_by=balance&order=desc&from_time=0&page=1&page_size=50")
        for acc in r.json().get("data", []):
            addr = acc["address"]
            if addr in seen: continue
            if acc.get("firstTransaction", 0) > time.time() - 300:  # created <5 min ago
                if acc["balance"] > 10_000_000_000:  # >10k USD
                    seen.add(addr)
                    print(f"NEW RICH WALLET!\n"
                          f"Address: {addr}\n"
                          f"Balance: ${acc['balance']/1e9:,.2f}\n"
                          f"First tx: {time.strftime('%H:%M:%S', time.localtime(acc['firstTransaction']))}\n"
                          f"https://solscan.io/account/{addr}\n"
                          f"{'-'*50}")
        time.sleep(12)

if __name__ == "__main__":
    track_new_wallets()
