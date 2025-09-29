# HANDOFF: Flet Calculator App Implementation

## 作業概要
Flet（Python）を使用したWeb版電卓アプリの実装。MVP機能（四則演算、クリア、バックスペース等）を持つ動作可能なアプリケーションを作成する。

## 前提条件
- 作業環境: WSL2 / Ubuntu 24.04
- Python 3.10+ がインストール済み
- インターネット接続可能（pip install用）
- 現在のディレクトリ: `/home/akimi/dev/flet-app`

## 実行手順

### Phase 1: 環境構築
- [x] **Step 1.1**: 仮想環境作成・有効化
  ```bash
  make venv
  ```
  **確認**: `.venv/` ディレクトリが作成され、仮想環境がアクティブになること

- [x] **Step 1.2**: 依存関係インストール
  ```bash
  source .venv/bin/activate
  pip install 'flet[all]' pytest
  pip freeze > requirements.txt
  ```
  **確認**: `flet[all]` と `pytest` がインストールされること

### Phase 2: 核心ロジック実装
- [x] **Step 2.1**: 計算ロジック実装 (`app/logic.py`)
  - Decimal（`ROUND_HALF_UP`）で演算、浮動小数誤差防止
  - 演算子優先順位付きの式評価（連続演算チェーン対応）
  - `%`（割合計算）サポート
  - ゼロ除算や桁あふれ時の例外ハンドリング（フォールバック表示）
  - UI層から呼び出せる純関数APIを提供

- [x] **Step 2.2**: 計算ロジックテスト実装 (`tests/test_logic.py`)
  - 四則演算、連続演算、小数、丸め、% 変換、ゼロ除算、端数ケースを網羅
  - 正常系/異常系の期待結果を明示

- [x] **Step 2.3**: テスト実行確認
  ```bash
  make test
  # または pytest tests/test_logic.py -v
  ```
  **確認**: 全テストがPASS、計算ロジックが正常動作

### Phase 3: 状態管理実装
- [x] **Step 3.1**: 状態クラス実装 (`app/state.py`)
  ```python
  @dataclass
  class CalculatorState:
      display_value: str = "0"
      input_buffer: str = ""
      last_operator: Optional[str] = None
      pending_value: Optional[Decimal] = None
      should_reset_display: bool = False
      error_state: bool = False
      memory_value: Decimal = Decimal("0")
  ```

- [x] **Step 3.2**: 状態管理メソッド実装
  - 数字/小数点入力、演算子入力、等号、AC/C/BS、±、% を制御
  - メモリ操作（M+, M-, MR, MC）を用意（利用は任意）
  - エラーリセット・桁あふれ対応

### Phase 4: UI実装
- [x] **Step 4.1**: 基本UI構造 (`app/ui.py`)
  - ディスプレイエリア（Text + Card）
  - スマホ幅でも折り返さないボタングリッド（`ResponsiveRow` など）
  - 数字ボタン（0-9）
  - 演算子ボタン（+, -, ×, ÷, =）
  - 機能ボタン（AC, C, BS, ±, ., %）

- [x] **Step 4.2**: イベントハンドリング
  - ボタンクリックイベント処理（状態→表示更新）
  - AC/C/BS/±/./%/演算子/= の全ボタン対応
  - 桁あふれ・エラー状態の表示切替

### Phase 5: メインアプリ統合
- [x] **Step 5.1**: メインアプリ実装 (`main.py`)
  ```python
  import flet as ft
  from app.ui import CalculatorApp

  def main(page: ft.Page):
      # ページ設定
      # CalculatorApp インスタンス作成・追加

  if __name__ == "__main__":
      ft.app(target=main)  # Web版
  ```

- [ ] **Step 5.2**: 初回起動テスト
  ```bash
  make run
  # または python main.py
  ```
  **確認**: Webサーバが起動し、ブラウザで電卓画面が表示される

### Phase 6: 動作確認・デバッグ
- [ ] **Step 6.1**: 基本操作確認
  - 初期状態で「0」が表示される
  - 数字ボタン（1, 2, 3...）クリックで表示更新
  - 演算子ボタン（+）クリックで操作受付
  - 等号ボタン（=）クリックで計算実行

- [ ] **Step 6.2**: 計算フロー確認
  ```
  操作手順: [1] → [+] → [2] → [=]
  期待結果: 「3」が表示される
  ```

- [ ] **Step 6.3**: エラーケース確認
  - ゼロ除算: [5] → [÷] → [0] → [=] → "Error" 表示
  - 桁あふれ時のフォールバック表示
  - AC操作: [AC] → 「0」表示、状態リセット

- [x] **Step 6.4**: 全テスト再実行
  ```bash
  make test
  pytest -q
  ```
  **確認**: 全テストがPASS

### Phase 7: 最終検証
- [ ] **Step 7.1**: 完全な開発フロー実行
  ```bash
  make clean  # 環境クリア（あれば）
  make venv   # 環境構築
  make dev    # 開発サーバ起動
  ```

- [ ] **Step 7.2**: 受け入れテスト実行
  1. ブラウザで電卓アプリアクセス
  2. 初期表示「0」を確認
  3. 「1+2=3」操作を実行し、結果確認
  4. 主要ボタンの動作確認

> **備考**: 現在の実行環境では TCP ソケットの bind が拒否されるため、`make dev`
> で Flet サーバーを起動できませんでした。ポート制限のない環境で再実行してください。

## 受け入れ基準

### ✅ 必須要件
1. **環境構築成功**: `make venv && make dev` でエラーなし
2. **アプリ起動成功**: WebサーバからFletアプリにアクセス可能
3. **初期表示正常**: 「0」が表示される
4. **基本計算成功**: 「1+2=3」が正常動作
5. **テスト全通過**: `pytest -q` で全テストPASS
6. **主要操作正常**: AC/C/BS/±/./%/÷×−＋/= すべて機能
7. **表示安定性**: 桁あふれ時は科学技術表記か上限表示でフォールバック
8. **精度確保**: Decimal + `ROUND_HALF_UP` で計算が行われる

### ✅ 動作確認項目
- [ ] 数字入力: 0-9 ボタンで数値入力
- [ ] 四則演算: +, -, ×, ÷ で計算実行
- [ ] クリア機能: AC（全クリア）, C（表示クリア）
- [ ] バックスペース: BS で末尾文字削除
- [ ] 符号反転: ± で正負切替
- [ ] 小数点: . で小数入力
- [ ] 端数処理: Decimalで `ROUND_HALF_UP`
- [ ] 桁あふれ: 科学技術表記か上限表示へフォールバック
- [ ] エラー処理: ゼロ除算で "Error" 表示

## トラブルシューティング

### 問題1: Flet インストールエラー
**症状**: `pip install flet` でエラー
**対処**:
```bash
pip install --upgrade pip
pip install flet --no-cache-dir
```

### 問題2: Web サーバが起動しない
**症状**: `python main.py` でエラー
**対処**:
1. ポート使用状況確認: `lsof -i :8550`
2. ファイアウォール設定確認
3. 仮想環境のアクティブ確認

### 問題3: ブラウザでアプリが表示されない
**症状**: ブラウザアクセスでエラー
**対処**:
1. URL確認: `http://localhost:8550`
2. ブラウザキャッシュクリア
3. 別ブラウザでテスト

### 問題4: 計算結果が不正確
**症状**: `0.1 + 0.2` が `0.3` にならない
**対処**: `app/logic.py` でDecimal型使用確認

### 問題5: テストが失敗する
**症状**: `pytest` でテストエラー
**対処**:
1. 依存関係再インストール: `pip install -r requirements.txt`
2. テストファイルの import 文確認
3. 個別テスト実行: `pytest tests/test_logic.py::test_basic_arithmetic -v`

## 完了報告フォーマット

実装完了時は以下を報告：

```
✅ Flet Calculator App 実装完了

【実行確認】
- `make venv && make dev`: ✅ 成功
- ブラウザアクセス: ✅ 成功（http://localhost:8550）
- 初期表示: ✅ 「0」表示確認
- 基本計算: ✅ 「1+2=3」動作確認
- テスト実行: ✅ `pytest -q` 全通過

【ファイル構成】
- main.py: メインアプリケーション
- app/logic.py: 計算ロジック
- app/state.py: 状態管理
- app/ui.py: UIコンポーネント
- tests/test_logic.py: 単体テスト
- requirements.txt: 依存関係

【次のステップ】
1. Git初期化: `git init && git add . && git commit -m "Initial commit"`
2. 拡張機能検討: メモリ機能、キーボード入力対応
3. Desktop版対応: `ft.app(target=main, view=ft.WEB_BROWSER)` → `ft.AppView.FLET_APP`
```

## 注意事項
- **危険コマンド**: `sudo`, `rm -rf`, `chmod 777` 等は提案のみ、実行前に確認
- **ポート競合**: デフォルトポート8550が使用済みの場合、別ポート指定
- **仮想環境**: 必ず `.venv` 内で作業、システムPythonの汚染回避
- **バックアップ**: 重要な変更前はファイルバックアップ推奨
