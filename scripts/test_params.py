def solve(epsilon, cooling_rate, epoch):
    """
    パラメータが正しく渡されているかテストするソルバー
    """
    # 入力を読み込む
    line1 = input()
    line2 = input()

    # 出力を書き込む（パラメータ値を含める）
    print(f"epsilon={epsilon}, cooling_rate={cooling_rate}, epoch={epoch}")
    print(line1)
    print(line2)

    # スコアを計算（パラメータの値を使う）
    score = epsilon * 1000 + cooling_rate * 100 + epoch
    return score
