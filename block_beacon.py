"""
Block Beacon — мониторинг новых блоков Bitcoin с анализом на аномалии.
"""

import requests
import time

def fetch_latest_block():
    r = requests.get("https://blockstream.info/api/blocks")
    r.raise_for_status()
    return r.json()[0]

def fetch_block_details(block_hash):
    r = requests.get(f"https://blockstream.info/api/block/{block_hash}")
    r.raise_for_status()
    return r.json()

def analyze_block(block):
    tx_count = block["tx_count"]
    size_kb = block["size"] / 1024
    reward = 6.25  # пока статично, можно доработать

    print(f"
📦 Новый блок: {block['height']}")
    print(f"🔗 Хеш: {block['id']}")
    print(f"⏱️  Время: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(block['timestamp']))}")
    print(f"📊 Размер: {size_kb:.2f} KB")
    print(f"🔢 Транзакций: {tx_count}")
    print(f"💰 Награда: ~{reward} BTC")

    if tx_count > 3000:
        print("⚠️ Много транзакций — блок переполнен!")
    if size_kb > 1400:
        print("⚠️ Размер почти предельный — высокая нагрузка!")

def main():
    print("🚨 Block Beacon активен. Ожидание новых блоков...
")
    last_seen = None

    try:
        while True:
            latest = fetch_latest_block()
            if latest["id"] != last_seen:
                block = fetch_block_details(latest["id"])
                analyze_block(block)
                last_seen = latest["id"]
            time.sleep(30)
    except KeyboardInterrupt:
        print("
Остановлено пользователем.")
    except Exception as e:
        print("Ошибка:", e)

if __name__ == "__main__":
    main()
