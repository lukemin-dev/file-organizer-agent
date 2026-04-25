# File Organizer Agent

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md)

ファイル拡張子に基づいてディレクトリ内のファイルを自動的に分類・整理するPythonベースのツールです。このツールは、類似のファイルを適切なカテゴリフォルダにグループ化することで、クリーンで構造化されたファイルシステムを維持するのに役立ちます。

このプロジェクトは、AIエージェント支援型ワークフローを活用し、計画、実装、レビュー、テスト、ドキュメント作成の各段階に分けて開発されました。

## 機能

- **自動ファイル分類**: ファイル拡張子に基づいて定義済みのカテゴリにファイルを整理
- **ドライランモード**: 適用前に整理変更をプレビュー
- **重複処理**: ファイル名に番号を追加して重複ファイル名を自動処理
- **包括的なログ**: すべての操作をファイルとコンソールに記録
- **コマンドラインインターフェース**: 柔軟なオプションを備えたシンプルで直感的なCLI
- **拡張可能なカテゴリ**: 新しいファイルカテゴリと拡張子を簡単に追加
- **クロスプラットフォーム**: Windows、macOS、Linuxで動作

### サポートされるカテゴリ

- **PDF**: `.pdf`
- **Slides**: `.pptx`, `.ppt`, `.odp`
- **Docs**: `.docx`, `.doc`, `.odt`, `.txt`
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`
- **Installers**: `.exe`, `.msi`, `.dmg`, `.pkg`
- **Archives**: `.zip`, `.rar`, `.7z`, `.tar`, `.gz`
- **Code**: `.py`, `.js`, `.html`, `.css`, `.java`, `.cpp`, `.c`, `.h`
- **Data**: `.csv`, `.xlsx`, `.xls`, `.json`, `.xml`
- **Others**: その他のすべてのファイル拡張子

## インストール

### 前提条件

- Python 3.7以上
- pip (Pythonパッケージインストーラー)

### ソースからインストール

1. リポジトリをクローンまたはダウンロード:
   ```bash
   git clone <repository-url>
   cd file-organizer-agent
   ```

2. 依存関係をインストール:
   ```bash
   pip install -r requirements.txt
   ```

このプログラムは最小限の依存関係を持ち、ほとんどのPythonインストールでそのまま動作します。

## 使用方法

### 基本的な使用方法

Downloadsフォルダのファイルを整理 (ドライランモード):
```bash
python -m src.main
```

特定のディレクトリのファイルを整理:
```bash
python -m src.main --target /path/to/your/directory
```

整理を適用 (ファイルを移動):
```bash
python -m src.main --target /path/to/your/directory --apply
```

**注意**: `.DS_Store`、`.localized`などのシステムファイルの誤った移動を防ぐため、`.`で始まる隠しファイルは自動的に整理対象から除外されます。

### コマンドラインオプション

- `--target PATH`: 整理対象のディレクトリを指定 (デフォルト: ~/Downloads)
- `--apply`: 整理を適用してファイルを移動 (デフォルト: ドライランモードのみ)

### 例

#### 例1: Downloadsフォルダ整理のプレビュー
```bash
python -m src.main
```
出力:
```
Planned to organize 15 files:
  PDF: 3 files
  Images: 5 files
  Docs: 2 files
  Archives: 2 files
  Others: 3 files
Would move document.pdf to PDF/document.pdf
Would move photo.jpg to Images/photo.jpg
...
```

#### 例2: 特定のフォルダを整理
```bash
python -m src.main --target ./messy_folder --apply
```
出力:
```
Planned to organize 8 files:
  Code: 3 files
  Data: 2 files
  Others: 3 files
Moved script.py to Code/script.py
Moved data.csv to Data/data.csv
...
```

#### 例3: 重複ファイル名の処理
同じ名前のファイルが複数ある場合、整理ツールは自動的に一意の名前を生成します:
```
original.txt -> Docs/original.txt
original.txt -> Docs/original_1.txt
original.txt -> Docs/original_2.txt
```

## 設定

### デフォルトの対象ディレクトリ

デフォルトでは、整理ツールはシステムのDownloadsフォルダを対象とします:
- **macOS/Linux**: `~/Downloads`
- **Windows**: `C:\Users\<username>\Downloads`

`src/config.py`を変更することでこのデフォルトを変更できます:
```python
DEFAULT_TARGET = Path.home() / "Downloads"  # このパスを変更
```

### 新しいカテゴリの追加

新しいファイルカテゴリを追加するには、`src/config.py`を編集してください:
```python
CATEGORIES = {
    "PDF": ["pdf"],
    "Slides": ["pptx", "ppt", "odp"],
    "YourNewCategory": ["ext1", "ext2", "ext3"],  # カテゴリを追加
    "Others": []
}
```

## ログ

整理ツールはすべての操作の詳細なログを生成します:

- **ログファイル**: `logs/organizer.log`
- **コンソール出力**: リアルタイムの進捗と結果
- **ログ形式**: タイムスタンプ、レベル、メッセージ

ログエントリの例:
```
2024-01-15 10:30:15 - INFO - Starting file organizer on /Users/user/Downloads, apply=False
2024-01-15 10:30:15 - INFO - DRY RUN: Would move document.pdf to PDF/document.pdf
2024-01-15 10:30:16 - INFO - File organization completed.
```

## 要件

- **Python**: 3.7+
- **依存関係**: なし (Python標準ライブラリのみ使用)
- **オペレーティングシステム**: Windows、macOS、Linux

### 開発依存関係

テストおよび開発用:
- pytest
- pytest-cov

## テスト

プロジェクトには包括的なユニットテストと統合テストが含まれています。

### テストの実行

テスト依存関係をインストール:
```bash
pip install -r requirements.txt
```

すべてのテストを実行:
```bash
pytest
```

カバレッジ付きで実行:
```bash
pytest --cov=src --cov-report=html
```

特定のテストカテゴリを実行:
```bash
pytest -m "not slow"  # 遅いテストをスキップ
pytest tests/test_organizer.py  # 特定のテストファイルを実行
```

### 手動テスト

手動テストの手順については、`MANUAL_TESTING.md`を参照してください。

## プロジェクト構造

```
file-organizer-agent/
├── src/
│   ├── main.py          # CLIエントリーポイント
│   ├── organizer.py     # コア整理ロジック
│   ├── config.py        # 設定とカテゴリ
│   └── utils.py         # ユーティリティ関数
├── tests/
│   ├── test_*.py        # ユニットテスト
│   └── conftest.py      # テストフィクスチャ
├── logs/                # ログファイル (実行時に作成)
├── sample_downloads/    # テスト用サンプルファイル
├── requirements.txt     # Python依存関係
├── pytest.ini          # Pytest設定
├── MANUAL_TESTING.md   # 手動テストガイド
└── README.md           # このファイル
```

## 貢献

貢献を歓迎します！以下のガイドラインに従ってください:

### 開発設定

1. リポジトリをフォーク
2. 機能ブランチを作成: `git checkout -b feature/your-feature-name`
3. 開発依存関係をインストール: `pip install -r requirements.txt`
4. テストを実行: `pytest`
5. 変更を適用
6. 新機能のテストを追加
7. すべてのテストが通ることを確認
8. 必要に応じてドキュメントを更新
9. 変更をコミット: `git commit -m "Add your feature"`
10. フォークにプッシュ: `git push origin feature/your-feature-name`
11. Pull Requestを作成

### コードスタイル

- PEP 8スタイルガイドラインに従う
- 関数パラメータと戻り値に型ヒントを使用
- 説明的なコミットメッセージを書く
- すべての公開関数とクラスにドックストリングを追加

### テスト

- すべての新機能にユニットテストを書く
- テストカバレッジを80%以上維持
- エッジケースとエラー条件をテスト
- PR提出前に完全なテストスイートを実行

### イシューの報告

バグを報告したり機能をリクエストしたりする場合:

1. 既存のイシューを先に確認
2. 明確で説明的なタイトルを使用
3. イシューの再現手順を提供
4. 環境情報（OS、Pythonバージョン）を含む
5. 関連するログファイルを添付（可能な場合）

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています - 詳細はLICENSEファイルを参照してください。

## 変更履歴

### バージョン 1.0.0
- 初期リリース
- 基本ファイル整理機能
- ドライランモード
- コマンドラインインターフェース
- 包括的なテストスイート
- ログサポート

## サポート

問題が発生したり質問がある場合:

1. `MANUAL_TESTING.md`のトラブルシューティングセクションを確認
2. `logs/organizer.log`のログを確認
3. GitHubの既存イシューを検索
4. 詳細な情報とともに新しいイシューを作成

## ロードマップ

将来の機能強化:
- GUIインターフェース
- 設定ファイルによるカスタムカテゴリ定義
- アンドゥ機能
- ファイルマネージャーとの統合
- クラウドストレージサポート
- 高度なフィルタリングオプション</content>
<parameter name="filePath">/Users/gyuminlee/Desktop/file-organizer-agent/README.ja.md