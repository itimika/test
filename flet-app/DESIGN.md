# Flet Calculator App - Design Document

## 画面構成

### レイアウト構造
```
┌─────────────────────────────┐
│         Display             │  ← 計算結果表示エリア
├─────────────────────────────┤
│  AC  │  C  │  BS │  ±  │   │  ← 機能ボタン行
├──────┼─────┼─────┼─────┤───┤
│   7  │  8  │  9  │  ÷  │   │  ← 数字・演算子
├──────┼─────┼─────┼─────┤───┤
│   4  │  5  │  6  │  ×  │   │
├──────┼─────┼─────┼─────┤───┤
│   1  │  2  │  3  │  -  │   │
├──────┼─────┼─────┼─────┤───┤
│   0       │  .  │  +  │ = │  ← 0は2列幅
└─────────────────────────────┘
```

### 画面サイズ対応
- **Desktop**: 固定幅 300px, 縦横比 3:4
- **Mobile**: 画面幅の90%, 最大400px
- **ボタン**: 最小44px × 44px (タッチ操作考慮)

## UIコンポーネント選定

### Fletコンポーネント
- **Container**: 全体レイアウト
- **Column**: 縦配置 (Display + ButtonGrid)
- **Row**: 横配置 (ボタン行)
- **ElevatedButton**: 数字・演算子ボタン
- **Text**: ディスプレイ表示
- **Card**: ディスプレイ背景

### ボタンスタイル
```python
# 数字ボタン
number_button_style = ButtonStyle(
    color=colors.BLACK,
    bgcolor=colors.GREY_200,
    shape=RoundedRectangleBorder(radius=8)
)

# 演算子ボタン
operator_button_style = ButtonStyle(
    color=colors.WHITE,
    bgcolor=colors.ORANGE,
    shape=RoundedRectangleBorder(radius=8)
)

# 機能ボタン
function_button_style = ButtonStyle(
    color=colors.BLACK,
    bgcolor=colors.GREY_300,
    shape=RoundedRectangleBorder(radius=8)
)
```

## 計算ロジック設計

### 演算子優先順位
- **Level 1**: `=` (計算実行)
- **Level 2**: `+`, `-` (加減算)
- **Level 3**: `×`, `÷` (乗除算)
- **即座実行**: 前の演算結果に続けて次の演算を実行

### 入力処理フロー
```python
def handle_input(state, input_type, value):
    match input_type:
        case "number":
            return handle_number_input(state, value)
        case "operator":
            return handle_operator_input(state, value)
        case "equals":
            return handle_equals_input(state)
        case "function":
            return handle_function_input(state, value)
```

### 特殊機能処理
- **バックスペース (BS)**: 表示値の末尾1文字削除
- **小数点 (.)**: 重複チェック、小数点以下入力開始
- **符号反転 (±)**: 現在表示値の正負反転
- **パーセント (%)**: 表示値を100で除算

## 状態管理設計

### Calculator状態クラス
```python
@dataclass
class CalculatorState:
    display_value: str = "0"           # 画面表示値
    input_buffer: str = ""             # 入力バッファ
    last_operator: Optional[str] = None # 直前の演算子
    operand: Optional[Decimal] = None   # 演算対象値
    should_reset_display: bool = False  # 次入力時リセットフラグ
    memory_value: Decimal = Decimal("0") # メモリ値 (M+, M-, MR, MC用)
    error_state: bool = False          # エラー状態フラグ
    last_operation: Optional[str] = None # 履歴用
```

### 状態遷移
1. **初期状態**: `"0"` 表示
2. **数字入力中**: バッファに蓄積、表示更新
3. **演算子入力**: 前の計算実行、演算子保存
4. **計算結果表示**: 結果表示、次入力でリセット
5. **エラー状態**: "Error" 表示、AC以外の入力無効

## エラー処理

### エラーケースと対応
- **ゼロ除算**: `"Error"` 表示、状態リセット
- **オーバーフロー**: `"Error"` 表示、状態リセット
- **不正入力**: 入力無視 (小数点重複など)
- **計算不可**: `"Error"` 表示

### エラー回復
- **AC (All Clear)**: 全状態リセット
- **C (Clear)**: 表示値のみリセット

## 精度・数値処理

### Decimal型使用
```python
from decimal import Decimal, getcontext
getcontext().prec = 15  # 15桁精度
```

### 表示桁数制限
- **最大表示桁数**: 12桁
- **指数表記**: 12桁超過時に `1.23E+10` 形式
- **小数点丸め**: `ROUND_HALF_UP` 使用

## テスト方針

### 単体テスト (Pure Functions)
```python
# tests/test_logic.py
def test_basic_arithmetic():
    assert calculate(Decimal("2"), "+", Decimal("3")) == Decimal("5")
    assert calculate(Decimal("10"), "÷", Decimal("2")) == Decimal("5")

def test_error_cases():
    with pytest.raises(ZeroDivisionError):
        calculate(Decimal("5"), "÷", Decimal("0"))
```

### 統合テスト
- UI操作シミュレーション
- 状態遷移確認
- エラーハンドリング確認

### テストケース例
- 基本四則演算: `2+3=5`, `10÷2=5`
- 連続演算: `2+3+4=9`
- 小数計算: `0.1+0.2=0.3`
- エラー処理: `5÷0=Error`

## リスクと回避策

### 1. 入力の同時押下
**リスク**: ボタン連打による意図しない動作
**回避策**:
- デバウンス処理 (300ms間隔制限)
- 入力処理中のボタン無効化

### 2. 浮動小数点の丸め誤差
**リスク**: `0.1 + 0.2 ≠ 0.3` 問題
**回避策**:
- Decimal型を使用
- 適切な精度設定 (15桁)

### 3. キーボード入力対応
**リスク**: Web版でのキーボードイベント処理
**回避策**:
- Flet `page.on_keyboard_event` 使用
- キーマッピング定義

### 4. アクセシビリティ
**リスク**: 視覚障害者の利用困難
**回避策**:
- `accessibility_label` 設定
- 適切なコントラスト比
- キーボードナビゲーション対応

### 5. レスポンシブ対応
**リスク**: 異なる画面サイズでの表示崩れ
**回避策**:
- `expand=True` を適切に使用
- 最小サイズ制限設定
- メディアクエリ相当の条件分岐

### 6. 国際化 (i18n)
**リスク**: 地域による小数点記号の違い
**回避策**:
- ロケール設定対応準備
- 設定ファイルでの記号定義
- 将来拡張として設計

### 7. メモリリーク
**リスク**: 長時間使用でのメモリ増加
**回避策**:
- 状態の適切なクリア
- イベントハンドラの適切な削除
- 履歴の上限設定

### 8. Flet Web制約
**リスク**: Desktop版との動作差異
**回避策**:
- 共通インターフェース設計
- プラットフォーム判定処理
- 機能の段階的有効化