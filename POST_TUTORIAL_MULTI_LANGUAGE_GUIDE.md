# チュートリアル完了後ガイド: 関数型を「複数の顔」で理解する

このドキュメントは、Haskellチュートリアル完了後に「次に何を学ぶか」を整理したものです。

結論はシンプルです。

- **最初の3つ（OCaml / Clojure / Elixir）は全部学べる。**
- ただし意図は「Haskellが不十分」という話ではない。  
- **各概念が最も鮮明に見える言語で補助的に学ぶと、理解が深くなる**という話です。

## 1. 役割分担（全体像）

```text
Haskell  = 関数型の思想・純粋性・型クラス・モナド
OCaml    = 実用的な型推論・代数的データ型・ML系の設計感覚
Clojure  = データ指向・REPL駆動・不変データ構造
Elixir   = 並行処理・分散処理・耐障害性・OTP
Scala/F# = 関数型を企業実務に接続する感覚
```

---

## 2. OCaml: 実用的な型推論を体で覚える

**学べます。むしろ非常に向いています。**

Haskellは型推論が強力な一方で、純粋性・遅延評価・型クラス・モナドなど「同時に学ぶ対象」が多く、初学時には情報量が多くなります。

OCamlは、次のように「書いた式から自然に型が決まる」体験がしやすいです。

```ocaml
let add x y = x + y
(* int -> int -> int *)

let greet name = "Hello, " ^ name
(* string -> string *)
```

### OCamlで特に学びやすい領域

- 型推論
- 代数的データ型
- パターンマッチ
- Option / Result
- イミュータブル設計
- モジュール / ファンクター
- 再帰とリスト処理
- 命令型との実務的なバランス

例（Union Typeに近い感覚）:

```ocaml
type payment =
  | CreditCard of string
  | BankTransfer of string
  | Cash

let describe_payment payment =
  match payment with
  | CreditCard number -> "Credit card: " ^ number
  | BankTransfer account -> "Bank transfer: " ^ account
  | Cash -> "Cash"
```

コンパイラが網羅性・型整合性を確認してくれる体験は、実務でも強力です。

---

## 3. Clojure: データ中心設計を学ぶ

**学べます。代表的な選択肢です。**

Clojureでは「クラス中心」ではなく「データ中心」で設計します。

- オブジェクトより map / vector / set / list
- メソッドより関数
- 破壊的更新より不変データ変換

```clojure
{:id 1 :name "Kenta" :age 30}
(update user :age inc)
```

### データ指向の本質

- システムの中心をオブジェクトではなくデータに置く
- 汎用データ構造で表現する
- 小さな関数を合成して変換パイプラインを作る

```clojure
(-> user
    (assoc :active true)
    (update :login-count inc)
    (select-keys [:id :name :active]))
```

Haskellが「閉じた型で厳密に表現する」方向に強いのに対し、Clojureは「変化しやすく不揃いな現実データ」を柔軟に扱う設計感覚を育てます。

---

## 4. Elixir: 並行・分散・耐障害性を設計で学ぶ

**学べます。非常に向いています。**

ElixirはBEAM VM上で動き、以下を前提にした世界観を持ちます。

- 大量同時接続
- 一部故障を許容
- 分散環境で継続稼働

```elixir
spawn(fn ->
  IO.puts("Hello from process")
end)
```

```elixir
send(pid, {:hello, "Kenta"})

receive do
  {:hello, name} -> IO.puts("Hello, #{name}")
end
```

### Elixirで本当に重要な点

- メッセージパッシング
- Supervisorによる監視・再起動
- GenServerによる状態管理
- OTPによる構造化
- Let it crash（障害前提設計）

Haskellにも並行技法（STM, async等）はありますが、Elixirは並行・分散・復旧が**言語文化の中心**にあります。

---

## 5. Haskellだけではダメか？

**ダメではありません。むしろ非常に価値があります。**

Haskell単体でも次が深く身につきます。

- 参照透過性
- 純粋関数
- 副作用分離
- 遅延評価
- 型クラス
- 関数合成
- ADT / パターンマッチ
- Functor / Applicative / Monad
- 型駆動設計

ただし学習初期は、次のギャップを感じることがあります。

- 動的で不揃いなデータ処理（Clojureが得意）
- 実務的な型推論の軽快さ（OCamlが得意）
- 障害前提の分散設計（Elixirが得意）
- 既存企業基盤への接続（Scala/F#が得意）

---

## 6. 複数言語で学ぶメリット

「関数型」を一枚岩ではなく複数流派として理解できます。

| 言語 | 強みの中心 |
| --- | --- |
| Haskell | 純粋性・型・遅延評価・抽象化 |
| OCaml | ML系・実用型推論・ADT |
| Clojure | データ指向・REPL・不変データ |
| Elixir | Actorモデル・耐障害性・分散 |
| Scala | JVM実務との接続 |
| F# | .NET実務との接続 |

結果として得られるのは「言語知識の数」よりも、**設計の引き出し**です。

---

## 7. 推奨学習順（言い直し版）

1. **Haskell**: 関数型の思想・純粋性・型設計の土台を作る
2. **OCaml**: 実用的な型推論とML系の設計感覚を得る
3. **Clojure**: データ変換中心の設計感覚を得る
4. **Elixir**: 並行・分散・耐障害性の実装感覚を得る
5. **Scala/F#**: JVM/.NET実務へ関数型を接続する

---

## 8. 「全部を深く」は不要

各言語をプロレベルまで掘る必要はありません。まずはミニプロジェクトで十分です。

| 言語 | ミニプロジェクト案 |
| --- | --- |
| Haskell | Parser Combinatorで小さなDSL |
| OCaml | JSONを型安全に変換するCLI |
| Clojure | CSV/JSON変換パイプライン |
| Elixir | 複数プロセスのジョブキュー |
| Scala/F# | Option/Either/Result中心の小さなWeb API |

---

## 9. 最終メッセージ

- **Haskellだけでも十分価値がある。**
- ただしHaskellは関数型の「中心」であり、関数型の「全体」ではない。  
- Haskellで土台を作り、他言語で別の顔を見ると、設計者として一段強くなる。

要するに:

```text
Haskellだけでは足りない、ではない。
Haskellで深く学んだ上で、他の流派に触れると理解が立体化する。
```
