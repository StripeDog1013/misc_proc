import argparse
from datetime import date
from dateutil.relativedelta import relativedelta


def calculate_average_incentive(initial_incentive, initial_months, increased_incentive, increased_months):
  """
  持株会の奨励金の平均を計算する関数

  Args:
    initial_incentive: 最初の奨励金（パーセント）
    initial_months: 最初の奨励金が適用された期間（ヶ月）
    increased_incentive: 増加後の奨励金（パーセント）
    increased_months: 増加後の奨励金が適用された期間（ヶ月）

  Returns:
    float: 奨励金の平均（パーセント）
  """
  total_months = initial_months + increased_months
  total_incentive_percentage = (initial_incentive * initial_months) + (increased_incentive * increased_months)
  average_incentive = total_incentive_percentage / total_months
  return average_incentive

def calculate_months_from_start(start_year, start_month, start_day):
  """
  指定された開始日から今日までの月数を計算する関数

  Args:
    start_year: 開始年 (int)
    start_month: 開始月 (int)
    start_day: 開始日 (int)

  Returns:
    int: 開始日から今日までの月数
  """
  start_date = date(start_year, start_month, start_day)
  end_date = date.today()
  difference = relativedelta(end_date, start_date)
  return difference.years * 12 + difference.months

if __name__ == "__main__":
  initial_incentive = 5.0
  initial_months = 70
  increased_incentive = 10
  increased_months = 24
  
  start_year = 2017
  start_month = 6
  start_day = 25
  months = calculate_months_from_start(2017, 6, 25)
  today = date.today()
  print("================================================")
  print(f"{start_year}年{start_month}月{start_day}日から{today.year}年{today.month}月{today.day}日までの月数: {months}ヶ月")
  print("================================================")
  
  increased_months = months - initial_months
  average_incentive = calculate_average_incentive(initial_incentive, initial_months, increased_incentive, increased_months)
  print(f"最初の奨励金: {initial_incentive}% ({initial_months}ヶ月)")
  print(f"増加後の奨励金: {increased_incentive}% ({increased_months}ヶ月)")
  print(f"奨励金の平均: {average_incentive:.2f}%")
  print("================================================")
