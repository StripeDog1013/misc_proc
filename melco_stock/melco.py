import argparse
import yfinance as yf
from datetime import datetime
import time # timeモジュールを追加
import sys # sysモジュールを追加
from tqdm import tqdm

def parse_arguments():
    parser = argparse.ArgumentParser(description='積立シミュレーション（株価変動＋賞与対応）')
    parser.add_argument('-c', '--contribution', type=int, metavar=('個人'), default=5000, help='個人拠出額（毎月）')
    parser.add_argument('-b', '--bonus', type=int, default=10000, help='賞与時（6月・12月）の拠出額')
    parser.add_argument('-r', '--ratio', type=float, default=5.5, help='奨励金率（%）')
    return parser.parse_args()


def calculate_months_since_june_2017():
    start = datetime(2017, 7, 25)
    now = datetime.now()
    return (now.year - start.year) * 12 + (now.month - start.month)


def fetch_monthly_prices(ticker_symbol="6503.T", months=93, retries=5, delay=10): # retriesとdelayを追加
    ticker = yf.Ticker(ticker_symbol)
    for i in tqdm(range(retries)):
        try:
            hist = ticker.history(period=f"{months}mo", interval="1mo")
            prices = hist['Close'].tolist()
            return prices[-months:]
        except yf.exceptions.YFRateLimitError:
            # print(f"レート制限に達しました。{delay}秒待機して再試行します... (残り{retries - 1 - i}回)")
            time.sleep(delay)
        except Exception as e:
            print(f"株価データの取得中に予期せぬエラーが発生しました: {e}")
            print(f"再試行します... (残り{retries - 1 - i}回)")
            time.sleep(delay) # その他のエラーでも待機
    print(f"エラー: {retries}回の再試行後も株価データを取得できませんでした。")
    sys.exit(1) # エラーが発生した場合はプログラムを終了する


def simulate_accumulation(prices, personal, bonus_amount, ratio):
    total_shares = 0
    total_investment = 0
    for i, price in enumerate(prices):
        if price == 0:
            continue
        bonus = personal * (ratio / 100)
        company_contribution = bonus_amount if ((i + 1) % 12 == 6 or (i + 1) % 12 == 0) else 0
        monthly_total = personal + bonus + company_contribution
        shares = monthly_total / price
        total_shares += shares
        total_investment += monthly_total
    avg_unit_price = total_investment / total_shares if total_shares else 0
    return total_shares, total_investment, avg_unit_price, prices[-1]


def main():
    args = parse_arguments()
    personal = args.contribution
    bonus = args.bonus
    months = calculate_months_since_june_2017()

    print(f"過去 {months} ヶ月分の株価データを取得中...")
    prices = fetch_monthly_prices(months=months)
    
    if len(prices) < months:
        print(f"取得できた株価データが不足しています（{len(prices)}ヶ月分）。正確なシミュレーションができません。")
        # ここでプログラムを終了するか、取得できたデータで続行するか判断
        # 今回は警告を出して続行する
        pass
    
    print("\n--- 情報 ---")
    print(f"【積立期間: {months} ヶ月（賞与月に賞与拠出）】")
    print(f"【個人拠出: {personal}円/月, 賞与拠出: {bonus}円/回, 奨励金率: {args.ratio}%】")

    shares, total, avg_price, latest = simulate_accumulation(prices, personal, bonus, args.ratio)

    print("\n--- 結果 ---")
    print(f"累計拠出額: {total:,.0f} 円")
    print(f"累積株数: {shares:.2f} 株")
    print(f"平均取得単価: {avg_price:.2f} 円")
    print(f"現在株価: {latest:.2f} 円")
    print(f"想定資産額: {shares * latest:,.0f} 円\n")


if __name__ == "__main__":
    main()