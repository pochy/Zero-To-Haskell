# Haskell 完全チュートリアル設計

このファイルは教材全体の索引です。本文は `chapters/` 以下に章ごとに分かれています。

## 核となる一文

Haskellは、型で世界を設計し、純粋関数で意味を記述し、副作用を型で隔離し、小さな計算を合成して大きなプログラムを作る言語です。

## 方針

この教材は、関数の使い方集ではありません。次の思想を、章ごとのコード、演習、設計判断に接続して学びます。

```text
なぜ純粋であるべきなのか
なぜ型で設計するのか
なぜ副作用を分けるのか
なぜ遅延評価なのか
なぜモナドや型クラスが重要なのか
なぜHaskellらしいコードは他言語と考え方が違うのか
```

Haskell公式サイトと Haskell 2010 Report が示す、純粋関数型、参照透過性、不変性、遅延評価、静的多相型、代数的データ型、型クラス、モナド的I/Oという特徴を学習順序に反映しています。

## Level 0-9 到達マップ

| Level | 対象 | 目標 |
| --- | --- | --- |
| 0 | 第0部 | Haskellの思想を説明する |
| 1 | 第1部 | Hello Worldと `IO ()` を読む |
| 2 | 第2部-第5部 | 純粋関数、ADT、再帰で小さな計算を書く |
| 3 | 第3部-第4部, 第10部 | 型で不正状態と失敗を表す |
| 4 | 第6部-第8部 | 遅延評価、型クラス、Monadを設計判断として使う |
| 5 | 第9部 | Pure Core / Effectful Shellに分ける |
| 6 | 第12部 | 型では表せない仕様をテストする |
| 7 | 第13部-第18部 | 実務アプリの境界を設計する |
| 8 | 第15部-第19部 | 性能、並行性、再現性を運用観点で見る |
| 9 | 第20部-第22部 | capstoneを実装し、設計をレビューする |

## 章一覧

## 第0部: Haskellを学ぶ前に
- 第0章: [Haskellとは何か](chapters/part_00_foundations/chapter_00_what_is_haskell/README.md) - 手順ではなく意味を書く言語としてHaskellを見る

## 第1部: Hello, World! から始める
- 第1章: [Hello, World! の本当の意味](chapters/part_01_hello_world/chapter_01_hello_world/README.md) - `IO ()` を命令ではなく値として理解する
- 第2章: [GHCiで「型を見る」習慣を作る](chapters/part_01_hello_world/chapter_02_ghci_types/README.md) - 実装より先に型を読む習慣を作る

## 第2部: 値・式・関数
- 第3章: [変数ではなく「束縛」](chapters/part_02_values_expressions_functions/chapter_03_bindings/README.md) - 値は書き換える箱ではなく名前に束縛された意味だと捉える
- 第4章: [参照透過性](chapters/part_02_values_expressions_functions/chapter_04_referential_transparency/README.md) - 式を同じ値で置き換えても意味が変わらない感覚を身につける
- 第5章: [関数とは何か](chapters/part_02_values_expressions_functions/chapter_05_functions/README.md) - 関数適用、カリー化、部分適用を設計の道具として使う
- 第6章: [高階関数](chapters/part_02_values_expressions_functions/chapter_06_higher_order_functions/README.md) - 関数を値として渡し、処理の形を抽象化する
- 第7章: [関数合成とポイントフリースタイル](chapters/part_02_values_expressions_functions/chapter_07_composition/README.md) - 小さな変換を合成して読みやすい処理の流れを作る

## 第3部: 型で考える
- 第8章: [型注釈と型推論](chapters/part_03_thinking_with_types/chapter_08_types/README.md) - 型をコンパイラ向け情報ではなく設計メモとして使う
- 第9章: [多相性](chapters/part_03_thinking_with_types/chapter_09_polymorphism/README.md) - 型変数から関数ができることとできないことを読む
- 第10章: [型エイリアスと newtype](chapters/part_03_thinking_with_types/chapter_10_newtype/README.md) - 意味の違う値を型で分ける

## 第4部: 代数的データ型とパターンマッチ
- 第11章: [代数的データ型](chapters/part_04_adt_pattern_matching/chapter_11_algebraic_data_types/README.md) - 不正な状態を型で表現できなくする
- 第12章: [パターンマッチ](chapters/part_04_adt_pattern_matching/chapter_12_pattern_matching/README.md) - 型の形に沿って安全に値を分解する
- 第13章: [Maybe](chapters/part_04_adt_pattern_matching/chapter_13_maybe/README.md) - 値がない可能性を型に出す
- 第14章: [Either](chapters/part_04_adt_pattern_matching/chapter_14_either/README.md) - 失敗理由を型として扱う

## 第5部: 再帰・リスト・fold
- 第15章: [ループではなく再帰](chapters/part_05_recursion_lists_fold/chapter_15_recursion/README.md) - データ構造の形に従って計算を書く
- 第16章: [map / filter / fold](chapters/part_05_recursion_lists_fold/chapter_16_map_filter_fold/README.md) - リスト処理を変換・選別・畳み込みとして読む
- 第17章: [リスト内包表記](chapters/part_05_recursion_lists_fold/chapter_17_list_comprehension/README.md) - 宣言的にリストを生成する

## 第6部: 遅延評価と非正格意味論
- 第18章: [遅延評価とは何か](chapters/part_06_lazy_evaluation/chapter_18_lazy_evaluation/README.md) - 必要になるまで評価しないことで可能になる表現を理解する
- 第19章: [遅延評価は万能ではない](chapters/part_06_lazy_evaluation/chapter_19_strictness/README.md) - 遅延と正格性のトレードオフを知る

## 第7部: 型クラス
- 第20章: [型クラスとは何か](chapters/part_07_typeclasses/chapter_20_typeclasses/README.md) - 型ごとの共通操作を法則付きの抽象として扱う
- 第21章: [型クラスの法則](chapters/part_07_typeclasses/chapter_21_typeclass_laws/README.md) - 型が合うだけでなく期待される法則を守る
- 第22章: [標準的な型クラス](chapters/part_07_typeclasses/chapter_22_standard_typeclasses/README.md) - よく使う型クラスの役割と階層を読む

## 第8部: Functor / Applicative / Monad
- 第23章: [Functor](chapters/part_08_functor_applicative_monad/chapter_23_functor/README.md) - 文脈を壊さず中身だけ変換する
- 第24章: [Applicative](chapters/part_08_functor_applicative_monad/chapter_24_applicative/README.md) - 独立した文脈付き計算を組み合わせる
- 第25章: [Monad](chapters/part_08_functor_applicative_monad/chapter_25_monad/README.md) - 前の結果に応じて次の計算を選ぶ
- 第26章: [do記法](chapters/part_08_functor_applicative_monad/chapter_26_do_notation/README.md) - 命令に見える構文をモナド合成として読む

## 第9部: Effect と IO の設計
- 第27章: [副作用とは何か](chapters/part_09_effects_io_design/chapter_27_effects/README.md) - 外界との相互作用を型で境界に出す
- 第28章: [Pure Core / Effectful Shell](chapters/part_09_effects_io_design/chapter_28_pure_core_effectful_shell/README.md) - 純粋な中心と副作用の薄い外側に分ける
- 第29章: [Reader / State / Writer](chapters/part_09_effects_io_design/chapter_29_reader_state_writer/README.md) - 環境・状態・ログを計算の文脈として扱う
- 第30章: [モナド変換子](chapters/part_09_effects_io_design/chapter_30_monad_transformers/README.md) - 複数の文脈を重ねる設計を学ぶ

## 第10部: エラー設計
- 第31章: [partial function を避ける](chapters/part_10_error_design/chapter_31_partial_functions/README.md) - 実行時に壊れる関数を型で置き換える
- 第32章: [エラーを型で設計する](chapters/part_10_error_design/chapter_32_typed_errors/README.md) - エラーを文字列ではなくドメイン型にする

## 第11部: モジュール・プロジェクト・ツール
- 第33章: [モジュールシステム](chapters/part_11_modules_projects_tools/chapter_33_module_system/README.md) - 公開境界で不変条件を守る
- 第34章: [Cabal / Stack / Hackage](chapters/part_11_modules_projects_tools/chapter_34_cabal_stack_hackage/README.md) - Haskellプロジェクトと依存関係を管理する
- 第35章: [Haskell Language Server](chapters/part_11_modules_projects_tools/chapter_35_haskell_language_server/README.md) - 型を見ながら開発する環境を作る

## 第12部: テストと仕様
- 第36章: [例ベースのテスト](chapters/part_12_testing_specification/chapter_36_example_based_tests/README.md) - 具体例で仕様の基礎を固定する
- 第37章: [プロパティベーステスト](chapters/part_12_testing_specification/chapter_37_property_based_tests/README.md) - 性質をランダム生成で検査する

## 第13部: パーサー・DSL・関数型設計
- 第38章: [パーサーコンビネータ](chapters/part_13_parsers_dsl_design/chapter_38_parser_combinators/README.md) - 小さなパーサーを合成して言語を読む
- 第39章: [DSL設計](chapters/part_13_parsers_dsl_design/chapter_39_dsl_design/README.md) - 小さな言語を型と関数で設計する

## 第14部: Lens とデータアクセス
- 第40章: [Lensとは何か](chapters/part_14_lens_data_access/chapter_40_lens/README.md) - 不変データの一部を合成可能に扱う

## 第15部: 並行・並列・STM
- 第41章: [軽量スレッドと async](chapters/part_15_concurrency_parallelism_stm/chapter_41_async/README.md) - 並行処理を構造化して扱う
- 第42章: [STM](chapters/part_15_concurrency_parallelism_stm/chapter_42_stm/README.md) - 共有状態をトランザクションとして扱う

## 第16部: 性能・最適化・GHC
- 第43章: [GHCの基礎](chapters/part_16_performance_ghc/chapter_43_ghc_basics/README.md) - Haskellがどうコンパイル・実行されるかを見る
- 第44章: [プロファイリング](chapters/part_16_performance_ghc/chapter_44_profiling/README.md) - 性能問題を推測ではなく測定する
- 第45章: [正格性制御](chapters/part_16_performance_ghc/chapter_45_strictness_control/README.md) - 必要な場所で評価を強制する

## 第17部: 高度な型システム
- 第46章: [kind と高階型](chapters/part_17_advanced_types/chapter_46_kinds_higher_kinded_types/README.md) - 型の型を読み、高カインド型を理解する
- 第47章: [GADT](chapters/part_17_advanced_types/chapter_47_gadt/README.md) - 型安全なASTをデータ構造に埋め込む
- 第48章: [Phantom Types](chapters/part_17_advanced_types/chapter_48_phantom_types/README.md) - 値にない状態や権限を型に持たせる
- 第49章: [DataKinds / TypeFamilies / Type-level programming](chapters/part_17_advanced_types/chapter_49_type_level_programming/README.md) - 型レベル計算の使いどころを判断する
- 第50章: [RankNTypes / Existential Types](chapters/part_17_advanced_types/chapter_50_rankn_existentials/README.md) - 高度な多相性で抽象境界を作る
- 第51章: [Deriving と Generics](chapters/part_17_advanced_types/chapter_51_deriving_generics/README.md) - 導出を便利さだけでなく意味として扱う

## 第18部: 実務アプリケーション設計
- 第52章: [CLIアプリを作る](chapters/part_18_application_design/chapter_52_cli_app/README.md) - 純粋ロジックを持つCLIを作る
- 第53章: [Web APIを作る](chapters/part_18_application_design/chapter_53_web_api/README.md) - ルート、入出力、エラーを型で表す
- 第54章: [DBを扱う](chapters/part_18_application_design/chapter_54_database/README.md) - DB境界とドメイン境界を分ける
- 第55章: [JSONと外部API](chapters/part_18_application_design/chapter_55_json_external_api/README.md) - 外部表現と内部モデルを分離する

## 第19部: FFI・JS・WASM・Nix
- 第56章: [FFI](chapters/part_19_ffi_js_wasm_nix/chapter_56_ffi/README.md) - 外部言語との境界を安全に扱う
- 第57章: [JavaScript / WebAssembly backend](chapters/part_19_ffi_js_wasm_nix/chapter_57_javascript_webassembly/README.md) - HaskellをWeb実行環境へ接続する選択肢を知る
- 第58章: [Nixと再現可能ビルド](chapters/part_19_ffi_js_wasm_nix/chapter_58_nix_reproducible_builds/README.md) - 環境差分を減らすビルド設計を知る

## 第20部: Haskell周辺言語との比較
- 第59章: [PureScript](chapters/part_20_language_comparisons/chapter_59_purescript/README.md) - Haskell的設計をJavaScript圏で使う選択肢を比較する
- 第60章: [Elm](chapters/part_20_language_comparisons/chapter_60_elm/README.md) - Web UI向けに単純化された純粋関数型を比較する
- 第61章: [Clean](chapters/part_20_language_comparisons/chapter_61_clean/README.md) - Haskellに近い遅延純粋言語を比較する
- 第62章: [OCaml / F# / Scala](chapters/part_20_language_comparisons/chapter_62_ocaml_fsharp_scala/README.md) - ML系・実務関数型との違いを見る
- 第63章: [Idris / Agda / Lean / F*](chapters/part_20_language_comparisons/chapter_63_idris_agda_lean_fstar/README.md) - 依存型と証明の世界との境界を知る
- 第64章: [Roc / Unison / Gleam](chapters/part_20_language_comparisons/chapter_64_roc_unison_gleam/README.md) - 新しい関数型言語の設計意図を比較する
- 第65章: [TypeScript + Effect / fp-ts](chapters/part_20_language_comparisons/chapter_65_typescript_effect_fpts/README.md) - Haskell的発想をTypeScriptで使う限界を知る

## 第21部: Haskellの歴史と哲学
- 第66章: [なぜHaskellは生まれたのか](chapters/part_21_history_philosophy/chapter_66_history_of_haskell/README.md) - 歴史から設計判断の理由を読む
- 第67章: [Haskellの哲学](chapters/part_21_history_philosophy/chapter_67_haskell_philosophy/README.md) - 型・純粋性・合成・法則を判断軸にする

## 第22部: プロフェッショナルへの総合演習
- 第68章: [小規模演習](chapters/part_22_professional_projects/chapter_68_small_project/README.md) - 安全な小さなライブラリやCLIを完成させる
- 第69章: [中規模演習](chapters/part_22_professional_projects/chapter_69_medium_project/README.md) - ドメイン型とエラー設計を持つアプリを作る
- 第70章: [大規模演習](chapters/part_22_professional_projects/chapter_70_large_project/README.md) - 型安全なアーキテクチャを設計・実装・説明する
