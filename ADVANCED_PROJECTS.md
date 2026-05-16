# Advanced Projects

このドキュメントは、チュートリアル完了後に作るツールやアプリの候補です。目的は、関数の使い方を増やすことではなく、チュートリアルで学んだ **型で設計する、純粋な中心を作る、副作用を境界に置く、失敗を型に出す、仕様をテストする** という考え方を、実際の制作物へ移すことです。

## 選び方

最初に作るなら、既存のcapstoneから自然に伸ばせる **型安全なタスク管理CLI / TUI** を推奨します。ParserやDSLを深く練習したい場合は、**Markdown / Zettelkasten ノート管理ツール** または **小さな設定言語** が向いています。Webや実務APIに進みたい場合は、**型安全Web API** を選びます。

## 1. 型安全なタスク管理CLI / TUI

何を作るか:

タスク、期限、優先度、状態を持つCLIツールを作ります。最初は `task add`、`task list`、`task done` だけで十分です。発展版ではTUIで一覧表示、検索、絞り込み、JSON保存を追加します。

なぜHaskell向きか:

タスクの状態遷移は型で表しやすい題材です。`Todo`、`Doing`、`Done`、`Archived` のような状態をADTにし、不正な遷移を関数の境界で防げます。CLIの入出力はEffectful Shellへ置き、タスク更新ロジックはPure Coreとしてテストできます。

活用する章/概念:

```text
newtype, ADT, Either, Pure Core / Effectful Shell
optparse-applicative, JSON境界, property test
```

最小版の完成条件:

```text
□ タスクを追加できる
□ タスク一覧を表示できる
□ タスクを完了状態にできる
□ 不正な入力を AppError で返せる
□ Pure CoreをIOなしでテストできる
```

Advanced版の拡張案:

TUI化、期限順ソート、タグ検索、JSON永続化、状態遷移の型安全化、QuickCheckによる状態遷移テスト。

## 2. Markdown / Zettelkasten ノート管理ツール

何を作るか:

Markdownファイル群を読み、frontmatter、タグ、内部リンク、見出し構造を解析します。リンク切れ、タグの揺れ、孤立ノート、重複タイトルを検出してレポートします。

なぜHaskell向きか:

Markdownやfrontmatterは小さな言語として扱えます。Parserで外部表現を読み、ADTで内部モデルを作り、検査ロジックを純粋関数として分離できます。ファイル読み込みだけをEffectful Shellに置けます。

活用する章/概念:

```text
Parser, ADT, Typed Error, file IO
Map/Set, DSL的な内部モデル, レポート生成
```

最小版の完成条件:

```text
□ ディレクトリ内のMarkdownを列挙できる
□ [[note-link]] のようなリンクを抽出できる
□ 存在しないリンクを検出できる
□ 検出結果を人間向けに表示できる
```

Advanced版の拡張案:

frontmatter parser、タグ正規化、Graphviz出力、HTMLレポート、CIでのリンク検査、差分検査。

## 3. DSL付きワークフローエンジン

何を作るか:

`fetch -> validate -> transform -> report` のような処理パイプラインを、小さなDSLとして定義し、インタプリタで実行します。

なぜHaskell向きか:

Haskellでは「何をするか」をADTやGADTで表し、「どう実行するか」を別の関数へ分けられます。これにより、同じDSLをテスト用、ログ付き実行、本番実行など複数の解釈で使えます。

活用する章/概念:

```text
ADT/GADT, Interpreter分離, Monad, Typed Error
Pure Core / Effectful Shell, テスト用インタプリタ
```

最小版の完成条件:

```text
□ Step型で処理の種類を表せる
□ Pipeline型で複数Stepを並べられる
□ 純粋なvalidate/transformを実行できる
□ 失敗をEitherで返せる
```

Advanced版の拡張案:

GADTで入出力型を持つStep、ログ収集、並行実行、リトライ、設定ファイルからのDSL読み込み。

## 4. 型安全Web API

何を作るか:

タスク、読書ログ、家計簿、学習進捗などの小さなWeb APIを作ります。APIのルート、入力、出力、エラーを型で表します。

なぜHaskell向きか:

Web APIは外部表現と内部モデルの境界が多い題材です。JSON、HTTP status、validation、DB行をそのまま内部に持ち込まず、変換境界を設計する練習になります。

活用する章/概念:

```text
servant, aeson, ReaderT, Typed Error
JSON境界, DB境界, Pure Core / Effectful Shell
```

最小版の完成条件:

```text
□ GET/POSTの小さなAPIを定義できる
□ JSON入力を検証してドメイン型に変換できる
□ エラーを型で表せる
□ Pure CoreをHTTPなしでテストできる
```

Advanced版の拡張案:

SQLite/PostgreSQL接続、認証、OpenAPI生成、構造化ログ、Docker Composeでのローカル実行。

## 5. Parser + Interpreter: 小さな設定言語

何を作るか:

独自の設定言語を作り、MegaparsecでparseしてASTにし、インタプリタで評価します。

例:

```text
backup "notes" every day to "/archive"
notify email when failed
```

なぜHaskell向きか:

Parser、AST、Typed Error、Interpreter分離を一つの題材で練習できます。入力の文字列と、内部で安全に扱う構造を明確に分けられます。

活用する章/概念:

```text
megaparsec, ADT, Either, pretty error
Parser combinator, DSL設計, Interpreter
```

最小版の完成条件:

```text
□ 設定文をparseできる
□ ASTとして表示できる
□ 不正な入力に位置付きエラーを返せる
□ ASTを純粋に評価できる
```

Advanced版の拡張案:

複数コマンド、型付きAST、設定ファイル実行、dry-run、lint、補完候補生成。

## 6. Property-based Testing Playground

何を作るか:

自分で小さなデータ型と型クラスインスタンスを作り、Functor、Applicative、Monoidなどの法則をQuickCheck/Tastyで検査します。

なぜHaskell向きか:

Haskellでは「型が合う」だけでは十分ではありません。抽象には期待される法則があります。このプロジェクトは、法則を実行可能な仕様として扱う練習になります。

活用する章/概念:

```text
型クラス, 型クラス法則, QuickCheck, tasty
Arbitrary, property test, 反例の読み方
```

最小版の完成条件:

```text
□ 独自データ型を定義できる
□ Eq/Show/Functorなどを実装できる
□ 少なくとも3つの法則をテストできる
□ 失敗するインスタンスを作り、反例を説明できる
```

Advanced版の拡張案:

Applicative/Monad laws、shrinking、law test helper、CI連携、ドキュメント化。

## 7. 並行ジョブキュー / バッチ処理システム

何を作るか:

ジョブを投入し、並行実行し、成功、失敗、再試行、ログを管理する小さなバッチ処理システムを作ります。

なぜHaskell向きか:

純粋なジョブ定義と、副作用を持つ実行を分けられます。STMやasyncを使うことで、共有状態、キャンセル、例外、リトライを構造化して扱えます。

活用する章/概念:

```text
async, STM, TVar, retry
Typed Error, logging, cancellation, retry policy
```

最小版の完成条件:

```text
□ ジョブをキューに追加できる
□ 複数workerで処理できる
□ 成功/失敗状態を記録できる
□ 失敗理由を型で表せる
```

Advanced版の拡張案:

優先度付きキュー、指数バックオフ、永続化、メトリクス、graceful shutdown、Web APIからの投入。

## 推奨ロードマップ

```text
1. 型安全なタスク管理CLI / TUI
2. Markdown / Zettelkasten ノート管理ツール
3. Parser + Interpreter: 小さな設定言語
4. DSL付きワークフローエンジン
5. 型安全Web API
6. 並行ジョブキュー / バッチ処理システム
```

学習効果を最大化するには、どのプロジェクトでも `README.md` に次を必ず書きます。

```text
なぜこの型にしたのか
どの不正状態を表現不能にしたのか
どこがPure Coreで、どこがEffectful Shellか
型では表せない仕様をどのテストで守るか
実務で残るトレードオフは何か
```
