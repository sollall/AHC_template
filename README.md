# AHC_template

AtCoder Heuristic Contest (AHC) 用のテンプレートリポジトリです。Optuna によるハイパーパラメータ最適化と MLflow による実験管理を統合しています。

## セットアップ

### 依存関係のインストール

```bash
pip install -r requirements.txt
```

## 使い方

### 1. デバッグモード (`debug.py`)

単一のテストケースを実行してデバッグします。

```bash
python debug.py --module_name scripts.sample --test_id 0 --epsilon 0.1 --cooling_rate 0.1 --epoch 100
```

**MLflow 統合版:**
```bash
python debug.py --mlflow --module_name scripts.sample --test_id 0 --epsilon 0.1 --cooling_rate 0.1 --epoch 100
```

#### オプション:
- `--module_name`: 実行するソルバーモジュール (必須)
- `--test_id`: テストケースID (必須)
- `--mlflow`: MLflow ロギングを有効化
- `--experiment_name`: MLflow 実験名 (デフォルト: `AHC_debug`)
- `--tracking_uri`: MLflow トラッキングURI (デフォルト: `./mlruns`)
- その他のパラメータ: ハイパーパラメータ (例: `--epsilon 0.1`)

#### 記録される情報 (MLflow有効時):
- パラメータ: すべてのハイパーパラメータ、module_name、test_id
- メトリクス: スコア、実行時間
- タグ: Git commit hash、ブランチ、実行モード

### 2. 最適化モード (`optimizer.py`)

複数のテストケースを並列実行し、Optuna でハイパーパラメータを最適化します。

**シングルラン（パラメータ最適化なし）:**
```bash
python optimizer.py
```
デフォルトパラメータで1回だけ実行します。

**マルチラン（Optuna によるパラメータ最適化）:**
```bash
python optimizer.py --multirun
```

**⚠️ IMPORTANT**: Optuna でハイパーパラメータ最適化を行うには、**`--multirun` フラグが必須**です。

**設定のオーバーライド:**
```bash
# テストケース数とトライアル数を変更
python optimizer.py --multirun general.num_tests=50 hydra.sweeper.n_trials=20

# パラメータ探索範囲を一時的にオーバーライド
python optimizer.py --multirun hydra.sweeper.params.optimizer.epoch="range(100,300)"
```

#### 設定ファイル (`conf/config.yaml`):
- `optimizer`: ハイパーパラメータのデフォルト値
  - `epsilon`: 0.1
  - `cooling_rate`: 0.1
  - `epoch`: 100
- `general`: 実行設定
  - `module_name`: ソルバーモジュール
  - `num_tests`: テストケース数
  - `max_workers`: 並列ワーカー数
- `mlflow`: MLflow 設定
  - `enabled`: MLflow を有効化 (デフォルト: `true`)
  - `experiment_name`: 使用されません（実験名は `{module_name}_{commit_hash}` の形式で自動生成されます）
  - `tracking_uri`: トラッキングURI
- `hydra.sweeper.params`: Optuna パラメータ探索範囲（`--multirun`時のみ有効）
  - `choice(0.1, 0.01, 0.001)`: 離散値から選択
  - `range(50, 200)`: 整数範囲
  - `interval(0.05, 0.2)`: 連続値範囲

#### 記録される情報 (MLflow有効時):
- パラメータ: すべてのハイパーパラメータ、general設定
- メトリクス:
  - 各テストケースのスコアと実行時間
  - 集計スコア: 合計、平均、標準偏差、最小値、最大値
  - 総実行時間、平均実行時間
- タグ: Git commit hash、ブランチ

## MLflow UI の起動

実験結果を可視化するには、MLflow UI を起動します:

```bash
mlflow ui
```

ブラウザで `http://localhost:5000` にアクセスすると、以下が確認できます:
- 実験の比較（実験名は `{module_name}_{commit_hash}` の形式で自動生成）
  - 例: `sample_4983605`
- パラメータとスコアの相関
- 実行履歴とメトリクスのグラフ
- Git commit との紐付け（同じcommitの実験を簡単に見つけられます）

## ディレクトリ構成

```
AHC_template/
├── conf/
│   └── config.yaml          # Hydra設定ファイル
├── scripts/
│   └── sample.py            # サンプルソルバー
├── utils/
│   └── inout.py             # I/Oユーティリティ
├── in/                      # 入力テストケース
├── out/                     # 出力結果
├── mlruns/                  # MLflow実験データ
├── debug.py                 # デバッグ実行スクリプト
├── optimizer.py             # 最適化実行スクリプト
└── requirements.txt         # Python依存関係
```

## ソルバーの作成

### 必須事項
- `scripts/` 内に Python ファイルを作成
- `solve(**kwargs)` 関数を実装
- `input()` で入力を読み込み
- `print()` で出力を書き込み
- スコア (数値) を返す

### サンプル (`scripts/sample.py`):
```python
def solve(epsilon, cooling_rate, epoch):
    """
    ソルバー関数

    Args:
        epsilon: ハイパーパラメータ1
        cooling_rate: ハイパーパラメータ2
        epoch: ハイパーパラメータ3

    Returns:
        スコア (数値)
    """
    # 入力の読み込み
    line1 = input()
    line2 = input()

    # 出力の書き込み
    print(line1)
    print(line2)

    # スコアを返す
    return epoch
```

## 留意点
- ソルバーには `solve(**kwargs)` 関数が必須
- ハイパーパラメータのデフォルト値は `config.yaml` の `optimizer` セクションで定義
- Optunaの探索範囲は `config.yaml` の `hydra.sweeper.params` セクションで定義
- **Optunaで最適化する場合は `--multirun` フラグを必ず指定**
- テストケースは `in/{test_id:04d}.txt` に配置
- 出力は `out/{test_id:04d}.txt` に自動保存
- MLflow を無効化する場合は `config.yaml` で `mlflow.enabled: false` に設定

## 機能

### debug.py
- 単一テストケースの実行とデバッグ
- カスタムハイパーパラメータの指定
- 出力ログの保存
- MLflow による実験記録 (オプション)

### optimizer.py
- 複数テストケースの並列実行 (`ProcessPoolExecutor`)
- Optuna によるハイパーパラメータ最適化 (TPE サンプラー、`--multirun`時)
- スコア統計の自動集計 (平均、標準偏差、最小値、最大値)
- MLflow による自動実験管理
  - 各トライアルのパラメータとメトリクスを個別に記録
  - 実験名の動的生成（モジュール名とcommit hashを含む）
  - Git commit との紐付け
  - 実行履歴の追跡
  - パラメータとスコアの相関分析が可能