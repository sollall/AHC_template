# AHC_template

## 使い方
以下のコマンドを参考に、AHC提出用のスクリプトを引数で指定してdebug.pyを実行することで各テストケースを実行することができる。

``` bash
python debug.py scripts.sample
```

- scriptには自作したsolve()を含む必要がある、main()はdebug.pyが使用する用なので基本変更する必要はない
- scriptごとに適したconfig.yamlをconf内に作成してもらう
    - cfg.optimizerを自作solverに与える


## 機能
- 複数のテストケースを自動で並列に実行
- optunaでのパラメータ最適化
- mlflowで実験記録、スコアの可視化を保存(予定)