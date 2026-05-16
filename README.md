# Haskell 完全チュートリアル

このリポジトリは、`TUTORIAL.md` の構想を元にした日本語のHaskellチュートリアルです。Hello, World! から始めて、型設計、副作用の分離、Functor / Applicative / Monad、テスト、実務アプリケーション、GHC、並行処理、高度な型、総合演習まで進みます。

最初に読むファイルは [START_HERE.md](START_HERE.md) です。

## 学習方針

この教材は、APIや構文の暗記ではなく、**型で世界を設計し、純粋関数で意味を記述し、副作用を型で隔離し、小さな計算を合成して大きなプログラムを作る** 力を育てます。

Haskellを支える中心思想は次の問いです。

```text
なぜ純粋であるべきなのか
なぜ型で設計するのか
なぜ副作用を分けるのか
なぜ遅延評価なのか
なぜモナドや型クラスが重要なのか
なぜHaskellらしいコードは他言語と考え方が違うのか
```

Haskell公式サイトと Haskell 2010 Report は、Haskellを純粋関数型、非正格意味論、静的多相型、代数的データ型、型クラス、モナド的I/Oなどを備える言語として位置づけています。この教材もその特徴を、Hello Worldから実務設計まで一貫して扱います。

各章では、関数の使い方だけでなく、設計思想、歴史的背景、他言語的な発想との違い、実務でその設計を選ぶ理由を説明します。コードは最終目的ではなく、概念を検証するための小さな観察対象です。

## 構成

| 部 | テーマ | 章数 |
| --- | --- | --- |
| 第0部 | Haskellを学ぶ前に | 1章 |
| 第1部 | Hello, World! から始める | 2章 |
| 第2部 | 値・式・関数 | 5章 |
| 第3部 | 型で考える | 3章 |
| 第4部 | 代数的データ型とパターンマッチ | 4章 |
| 第5部 | 再帰・リスト・fold | 3章 |
| 第6部 | 遅延評価と非正格意味論 | 2章 |
| 第7部 | 型クラス | 3章 |
| 第8部 | Functor / Applicative / Monad | 4章 |
| 第9部 | Effect と IO の設計 | 4章 |
| 第10部 | エラー設計 | 2章 |
| 第11部 | モジュール・プロジェクト・ツール | 3章 |
| 第12部 | テストと仕様 | 2章 |
| 第13部 | パーサー・DSL・関数型設計 | 2章 |
| 第14部 | Lens とデータアクセス | 1章 |
| 第15部 | 並行・並列・STM | 2章 |
| 第16部 | 性能・最適化・GHC | 3章 |
| 第17部 | 高度な型システム | 6章 |
| 第18部 | 実務アプリケーション設計 | 4章 |
| 第19部 | FFI・JS・WASM・Nix | 3章 |
| 第20部 | Haskell周辺言語との比較 | 7章 |
| 第21部 | Haskellの歴史と哲学 | 2章 |
| 第22部 | プロフェッショナルへの総合演習 | 3章 |

## 10/10教材としての使い方

- [CHECKPOINTS.md](CHECKPOINTS.md) で到達段階ごとの進級条件を確認します。
- [glossary.md](glossary.md) で用語をコード例、誤解、関連章と一緒に確認します。
- 各章の `solutions.md` は、答え合わせではなく設計レビューの観点として使います。
- [projects/capstone](projects/capstone) で、型安全な小規模アプリを設計、実装、テストします。
- [ADVANCED_PROJECTS.md](ADVANCED_PROJECTS.md) で、チュートリアル完了後に作るツールやアプリの候補を選びます。

## Dockerで始める

```bash
docker-compose build tutorial
docker-compose run --rm tutorial cabal build all
docker-compose run --rm tutorial runghc chapters/part_01_hello_world/chapter_01_hello_world/examples/Main.hs
docker-compose run --rm tutorial cabal test all
```

ローカルのGHC/Cabalを入れずに進められます。Docker内のGHC 9.10.3で、`cabal build all` と全章の `examples/Main.hs` を実行確認する方針です。

GHCupを使う場合は `START_HERE.md` の環境構築手順を参照してください。
