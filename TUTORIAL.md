以下は、**Hello, World! から、Haskellを専門的に設計・実装・運用できるレベルまで到達するための完全なチュートリアル構成**です。

単なる「関数の使い方集」ではなく、Haskellを支えている思想、つまり、

**なぜ純粋であるべきなのか**
**なぜ型で設計するのか**
**なぜ副作用を分けるのか**
**なぜ遅延評価なのか**
**なぜモナドや型クラスが重要なのか**
**なぜHaskellっぽいコードは他言語と見た目も考え方も違うのか**

を中心に組み立てています。

Haskell公式サイトは、Haskellを「ラムダ計算に基づく純粋関数型言語」であり、参照透過性・不変性・遅延評価を特徴とすると説明しています。また Haskell 2010 Report は、Haskellを「汎用の純粋関数型言語」とし、高階関数、非正格意味論、静的多相型、代数的データ型、パターンマッチ、リスト内包表記、モジュールシステム、モナド的I/Oなどを備える言語として定義しています。([Haskell][1])

---

# 全体方針

このチュートリアルの主題は、次の一文です。

**Haskellは、型で世界を設計し、純粋関数で意味を記述し、副作用を型で隔離し、小さな計算を合成して大きなプログラムを作る言語である。**

そのため、学習順序は一般的な入門書とは少し違います。

普通の言語チュートリアルだと、

```txt
変数
条件分岐
ループ
関数
クラス
ファイル入出力
```

のように進みます。

Haskellでは、むしろ次のように学ぶべきです。

```txt
値とは何か
式とは何か
関数とは何か
型とは何か
副作用とは何か
計算を合成するとは何か
型で設計するとは何か
```

つまり、Haskellを学ぶことは、単に新しい構文を覚えることではなく、**プログラムを見る目を変えること**です。

---

# 到達レベルの定義

このチュートリアルでは、最終的な「Haskellの専門家・プロフェッショナル」を次のように定義します。

| レベル | 到達状態                                                       |
| --- | ---------------------------------------------------------- |
| 入門者 | `main = putStrLn "Hello, World!"` の意味を `IO ()` まで含めて説明できる  |
| 初級者 | 基本的な関数、型、リスト、再帰、パターンマッチを書ける                                |
| 中級者 | ADT、Maybe、Either、型クラス、Functor、Applicative、Monadを設計に使える     |
| 実務者 | Cabal/Stack、HLS、テスト、エラー設計、API、DB、並行処理を使ってアプリを作れる           |
| 上級者 | 遅延評価、正格性、プロファイリング、モナド変換子、型レベル設計、GHC拡張を使い分けられる              |
| 専門家 | 型・法則・抽象・性能・保守性・ライブラリ設計のトレードオフを説明し、他人のHaskellコードをレビュー・改善できる |

---

# 推奨環境

現代的なHaskell学習では、基本的に次の環境を使う構成にします。

```txt
GHCup
GHC
cabal-install
Haskell Language Server
Stack 任意
VS Code / Neovim / Emacs など
```

Haskell公式のダウンロードページでは、Linux、macOS、FreeBSD、Windows、WSL2向けに、GHCupで GHC、cabal-install、Stack、haskell-language-server をインストールする方法が推奨されています。GHCup自体も、Haskell用の主要インストーラとして説明されています。([Haskell][2])

現代Haskellでは、標準仕様としての Haskell 2010 と、実用上の中心である GHC/GHC拡張を区別して学びます。GHC User’s Guide では Haskell98、Haskell2010、GHC2021、GHC2024 といった言語エディションが説明され、現在は新しいコードに GHC2024 が推奨されています。([GHC GitLab][3])

---

# チュートリアル完全構成

## 第0部: Haskellを学ぶ前に

### 第0章: Haskellとは何か

#### 学ぶこと

```txt
Haskellは何を目指した言語か
命令型言語と何が違うか
関数型言語と純粋関数型言語の違い
Haskellらしさとは何か
```

#### 重要な考え方

Haskellは「手順を書く言語」ではなく、**意味を書く言語**です。

JavaScriptやPythonでは、

```txt
この変数を変える
この関数を呼ぶ
この順番で処理する
```

という発想が中心になりがちです。

Haskellでは、

```txt
この値は何か
この変換は何か
この計算はどんな型を持つか
この副作用はどこに隔離されているか
```

を考えます。

#### 必ず扱うキーワード

```txt
純粋関数型
参照透過性
不変性
静的型付け
型推論
多相性
非正格意味論
遅延評価
型クラス
代数的データ型
パターンマッチ
モナド的I/O
```

Haskell 2010 Report の目次にも、式、パターンマッチ、do式、ユーザー定義データ型、型クラス、モジュール、基本I/O、FFIなどが標準的な構成要素として並んでいます。

---

## 第1部: Hello, World! から始める

## 第1章: Hello, World! の本当の意味

### 最初のコード

```haskell
main :: IO ()
main = putStrLn "Hello, World!"
```

### 表面的な説明

これは画面に `Hello, World!` と出力するプログラムです。

### Haskell的な説明

本当に重要なのは、`putStrLn "Hello, World!"` が「即座に実行される命令」ではなく、

```haskell
IO ()
```

という型を持つ**I/Oアクション**だということです。

つまり、

```haskell
putStrLn "Hello, World!"
```

は、

```txt
実行されると文字列を出力し、意味のある返り値は返さない計算
```

です。

### なぜこうなっているのか

Haskellは純粋関数型言語です。
純粋な世界では、関数は同じ入力に対して同じ出力を返すべきです。

しかし、出力、入力、ファイル操作、HTTP通信、乱数、現在時刻などは、外の世界と関わります。

そこでHaskellは、副作用を隠すのではなく、

```txt
この値は純粋な値です
この値は副作用を起こす計算です
```

という区別を型に出します。

これが `IO` です。

### この章の到達目標

```txt
main :: IO () を説明できる
putStrLn は命令ではなくIOアクションだと説明できる
純粋な値と副作用のある計算を区別できる
```

---

## 第2章: GHCiで「型を見る」習慣を作る

### 学ぶこと

```txt
ghci
:t
:info
:load
:reload
```

### なぜ重要か

Haskell学習では、エラーを怖がるよりも、**型を読む習慣**が重要です。

例えばGHCiで、

```haskell
:t map
```

とすると、

```haskell
map :: (a -> b) -> [a] -> [b]
```

のような型が見えます。

Haskellでは、型はドキュメントです。
型を読めるようになると、実装を読む前に関数の意味をかなり推測できます。

### Haskellらしい学習態度

```txt
まず実装を見る
```

ではなく、

```txt
まず型を見る
```

です。

---

# 第2部: 値・式・関数

## 第3章: 変数ではなく「束縛」

### 学ぶこと

```txt
値
束縛
不変性
式
文ではなく式
```

### Haskell的な考え方

Haskellでは、

```haskell
x = 10
```

は「変数 x に 10 を代入する」ではありません。

より正確には、

```txt
x という名前を 10 という値に束縛する
```

です。

一度束縛した値は、命令型言語の変数のように書き換えるものではありません。

### なぜ不変なのか

不変性があると、プログラムの意味が安定します。

```txt
この値は後で変わるかもしれない
```

と考えなくてよくなります。

これは参照透過性と密接に関係します。

---

## 第4章: 参照透過性

### 学ぶこと

```txt
参照透過性
純粋関数
副作用
等式推論
```

### 例

```haskell
add x y = x + y
```

このとき、

```haskell
add 1 2
```

は常に `3` です。

そのため、コード中の `add 1 2` を `3` に置き換えても意味が変わりません。

これが参照透過性です。

### なぜ重要か

参照透過性があると、プログラムを数学の式のように変形して考えられます。

```txt
デバッグしやすい
テストしやすい
最適化しやすい
並行化しやすい
局所的に理解しやすい
```

Haskellらしい設計では、できる限り多くのコードを参照透過に保ち、副作用を境界に追いやります。

---

## 第5章: 関数とは何か

### 学ぶこと

```txt
関数定義
関数適用
高階関数
カリー化
部分適用
ラムダ式
```

### Haskellの関数適用

```haskell
add x y = x + y
```

呼び出しはこうです。

```haskell
add 1 2
```

括弧やカンマではなく、空白で関数適用します。

### カリー化

Haskellの関数は基本的にカリー化されています。

```haskell
add :: Int -> Int -> Int
```

これは実際には、

```txt
Intを受け取り、Int -> Int の関数を返す関数
```

です。

つまり、

```haskell
add 10
```

は、

```haskell
Int -> Int
```

という関数になります。

### なぜカリー化なのか

カリー化により、関数を部分適用して再利用できます。

```haskell
add10 = add 10
```

これにより、小さな関数を組み合わせる設計が自然になります。

---

## 第6章: 高階関数

### 学ぶこと

```txt
map
filter
foldr
foldl'
関数を受け取る関数
関数を返す関数
```

### 例

```haskell
map (*2) [1,2,3]
```

結果は、

```haskell
[2,4,6]
```

### なぜ高階関数が重要か

Haskellでは、ループを書くよりも、

```txt
何を変換するか
何を残すか
どう畳み込むか
```

を書くことが多いです。

命令型では、

```txt
手順を記述する
```

Haskellでは、

```txt
変換の意味を記述する
```

という違いがあります。

---

## 第7章: 関数合成とポイントフリースタイル

### 学ぶこと

```txt
.
$
ポイントフリー
関数パイプライン
```

### 例

```haskell
process = sum . map (*2) . filter (>0)
```

これは右から左に、

```txt
正の数だけ残す
2倍する
合計する
```

という意味です。

### なぜHaskellらしいのか

Haskellでは、プログラムを「命令の列」ではなく、**関数の合成**として見ます。

ただし、ポイントフリーはやりすぎると読みにくくなります。

この章では、

```txt
美しいポイントフリー
読みにくいポイントフリー
```

を区別して学びます。

---

# 第3部: 型で考える

## 第8章: 型注釈と型推論

### 学ぶこと

```txt
型注釈
型推論
静的型付け
強い型付け
コンパイル時エラー
```

### 例

```haskell
add :: Int -> Int -> Int
add x y = x + y
```

Haskellでは多くの場合、型を書かなくても推論されます。

```haskell
add x y = x + y
```

しかし、トップレベル関数には型を書く文化が強いです。

### なぜ型を書くのか

型はコンパイラのためだけではありません。

```txt
設計メモ
仕様
ドキュメント
制約
レビュー対象
```

でもあります。

Haskellのプロフェッショナルは、実装より先に型を見ることが多いです。

---

## 第9章: 多相性

### 学ぶこと

```txt
多相的
パラメトリック多相
型変数
a
b
```

### 例

```haskell
id :: a -> a
id x = x
```

この関数は、どんな型の値でも受け取り、同じ型の値を返します。

### なぜ重要か

型が抽象的であるほど、できることは少なくなります。
できることが少ないほど、実装の自由度は下がり、意味は明確になります。

例えば、

```haskell
a -> a
```

という型を持つまともな関数は、ほぼ「受け取った値をそのまま返す」しかありません。

これがHaskellで重要な **型から意味を読む** という感覚です。

---

## 第10章: 型エイリアスと newtype

### 学ぶこと

```txt
type
newtype
ドメインモデリング
型安全性
```

### type

```haskell
type UserId = Int
```

これは別名です。
`UserId` と `Int` は実質同じです。

### newtype

```haskell
newtype UserId = UserId Int
newtype ProductId = ProductId Int
```

これは型として別物です。

### なぜ newtype が重要か

`UserId` と `ProductId` の中身がどちらも `Int` でも、意味は違います。

```haskell
getUser :: UserId -> IO User
```

に `ProductId` を渡せないようにすることで、バグを型で防ぎます。

これはHaskellらしい設計です。

```txt
意味が違うものは、型も違うものにする
```

---

# 第4部: 代数的データ型とパターンマッチ

## 第11章: 代数的データ型

### 学ぶこと

```txt
data
直和型
直積型
代数的データ型
コンストラクタ
```

### 例

```haskell
data User
  = Guest
  | Registered UserId Email
```

これは、

```txt
ユーザーは Guest か Registered のどちらか
Registered なら UserId と Email を必ず持つ
```

という意味です。

### なぜ重要か

Haskellでは、状態や仕様を型として表します。

TypeScriptでありがちな、

```ts
type User = {
  id?: string
  email?: string
  status: "guest" | "registered"
}
```

のような設計では、

```txt
registered なのに id がない
guest なのに email がある
```

という不正な状態を作れてしまいます。

Haskellでは、

```haskell
data User
  = Guest
  | Registered UserId Email
```

とすれば、不正な状態を作れません。

この思想は非常に重要です。

```txt
不正な状態を型で表現できなくする
```

---

## 第12章: パターンマッチ

### 学ぶこと

```txt
パターンマッチ
case
関数定義での分解
網羅性
```

### 例

```haskell
greet :: User -> String
greet Guest = "Hello, guest"
greet (Registered _ email) = "Hello, " ++ show email
```

### なぜ重要か

代数的データ型は、作るだけでは意味がありません。
パターンマッチによって、型の構造に従って安全に分解します。

Haskellのコンパイラは、パターンが網羅されていない場合に警告を出せます。

これは、

```txt
仕様の分岐を型に持たせる
その分岐をコンパイラに検査させる
```

というHaskellらしい設計です。

---

## 第13章: Maybe

### 学ぶこと

```txt
Maybe
Just
Nothing
nullの代替
部分関数を避ける
```

### 例

```haskell
findUser :: UserId -> Maybe User
```

これは、

```txt
ユーザーが見つかる場合もある
見つからない場合もある
```

という意味です。

### なぜ null ではないのか

`null` は型に現れません。

しかし `Maybe User` は、失敗可能性が型に現れます。

```haskell
Maybe User
```

を受け取った人は、必ず `Just` と `Nothing` の両方を考えなければいけません。

---

## 第14章: Either

### 学ぶこと

```txt
Either
Left
Right
エラー理由
Result型
例外との違い
```

### 例

```haskell
parseUser :: Text -> Either ParseError User
```

これは、

```txt
成功したら User
失敗したら ParseError
```

という意味です。

### なぜ重要か

Haskellでは、失敗する可能性を型に出すことが多いです。

```txt
失敗するかもしれない
```

という仕様をコメントではなく型に書きます。

これはTypeScriptでいう `Result<T, E>` に近いですが、Haskellではこの設計が文化として深く根付いています。

---

# 第5部: 再帰・リスト・fold

## 第15章: ループではなく再帰

### 学ぶこと

```txt
再帰
基底ケース
再帰ケース
構造的再帰
```

### 例

```haskell
sumList :: [Int] -> Int
sumList [] = 0
sumList (x:xs) = x + sumList xs
```

### なぜ再帰なのか

Haskellでは、状態を変えながら `for` や `while` を回すのではなく、データ構造の形に従って再帰します。

これは、

```txt
リストは空リストか、先頭と残りである
```

という型の構造に従っています。

---

## 第16章: map / filter / fold

### 学ぶこと

```txt
map
filter
foldr
foldl
foldl'
畳み込み
```

### なぜ fold が重要か

リスト処理の多くは、リストを何かの値に畳み込む処理です。

```haskell
sumList = foldr (+) 0
```

Haskellでは、自前で再帰を書く前に、

```txt
これは map か
これは filter か
これは fold か
これは traverse か
```

と考えます。

---

## 第17章: リスト内包表記

### 学ぶこと

```txt
list comprehension
generator
guard
```

### 例

```haskell
[x * 2 | x <- xs, x > 0]
```

これは、

```txt
xs から x を取り出し
x > 0 のものだけ
x * 2 に変換する
```

という意味です。

### なぜHaskellらしいのか

リスト内包表記は、手続きではなく集合的・宣言的にデータ生成を書く方法です。

Haskell 2010 Report にも、リスト内包表記は言語の式構文の一部として含まれています。

---

# 第6部: 遅延評価と非正格意味論

## 第18章: 遅延評価とは何か

### 学ぶこと

```txt
遅延評価
非正格意味論
サンク
必要になるまで評価しない
```

### 例

```haskell
ones :: [Int]
ones = 1 : ones

take 5 ones
```

結果は、

```haskell
[1,1,1,1,1]
```

### なぜ可能なのか

Haskellは、値を必要になるまで評価しません。

そのため、無限リストを定義しても、必要な部分だけ取り出せます。

### PureScriptとの違い

PureScriptはHaskellに構文や型システムがかなり似ていますが、JavaScriptにコンパイルされる都合もあり、基本的には正格評価です。

Haskellでは、

```haskell
const 1 undefined
```

のような式が、第二引数を使わなければ `1` になります。

正格評価の言語では、使わない引数でも先に評価されるため、こうはなりません。

---

## 第19章: 遅延評価は万能ではない

### 学ぶこと

```txt
スペースリーク
正格性
seq
BangPatterns
foldl'
```

### なぜ必要か

遅延評価は強力ですが、評価されていない計算、つまりサンクが溜まりすぎるとメモリを消費します。

そのため、実務では、

```txt
どこを遅延させるか
どこを正格にするか
```

を考える必要があります。

### Haskell専門家に必要な感覚

```txt
遅延評価を信頼する
しかし盲信しない
必要な場所では正格性を明示する
```

---

# 第7部: 型クラス

## 第20章: 型クラスとは何か

### 学ぶこと

```txt
型クラス
インスタンス
制約
オーバーロード
```

### 例

```haskell
class Printable a where
  printValue :: a -> String
```

### なぜ型クラスが必要か

Haskellでは、OOPの継承とは違う形で、多態的な振る舞いを表します。

例えば、

```haskell
show :: Show a => a -> String
```

は、

```txt
a が Show のインスタンスなら String に変換できる
```

という意味です。

### Haskellらしさ

型クラスは、単なるインターフェースではありません。

Haskellでは、型クラスにはしばしば**法則**があります。

---

## 第21章: 型クラスの法則

### 学ぶこと

```txt
Functor laws
Applicative laws
Monad laws
Monoid laws
法則を満たす設計
```

### 例: Functor

```haskell
fmap id == id
fmap (f . g) == fmap f . fmap g
```

### なぜ重要か

コンパイラがすべての法則を証明してくれるわけではありません。

しかし、法則を守ることで、利用者は安心して抽象を使えます。

Haskellのプロフェッショナルは、

```txt
型が合うか
```

だけでなく、

```txt
法則を満たすか
```

を考えます。

---

## 第22章: 標準的な型クラス

### 学ぶこと

```txt
Eq
Ord
Show
Read
Enum
Bounded
Num
Semigroup
Monoid
Functor
Applicative
Monad
Foldable
Traversable
```

### なぜ順番が重要か

特に重要なのはこの階層です。

```txt
Functor
  ↓
Applicative
  ↓
Monad
```

これはHaskell理解の中心です。

```txt
Functor: 中身に関数を適用できる
Applicative: 文脈付きの値を独立に組み合わせられる
Monad: 前の結果に応じて次の計算を決められる
```

---

# 第8部: Functor / Applicative / Monad

## 第23章: Functor

### 学ぶこと

```txt
fmap
<$>
文脈の中の値
```

### 例

```haskell
fmap (+1) (Just 10)
```

結果は、

```haskell
Just 11
```

### なぜ重要か

`Maybe a` はただの `a` ではありません。

```txt
失敗するかもしれない文脈の中にある a
```

です。

Functorは、その文脈を壊さずに中身を変換する抽象です。

---

## 第24章: Applicative

### 学ぶこと

```txt
pure
<*>
独立した文脈の合成
```

### 例

```haskell
User <$> parseName input <*> parseEmail input
```

### なぜ重要か

Applicativeは、互いに依存しない計算を組み合わせるときに使います。

例えばフォームバリデーションでは、

```txt
名前の検証
メールの検証
年齢の検証
```

は互いに独立しています。

その場合、MonadよりApplicativeの方が意図をよく表します。

---

## 第25章: Monad

### 学ぶこと

```txt
>>=
return
pure
do記法
前の結果に依存する計算
```

### 例

```haskell
findUser userId >>= findOrders
```

これは、

```txt
ユーザーを探す
見つかった結果を使って注文を探す
```

という意味です。

### なぜMonadが必要か

Monadは「副作用のためだけのもの」ではありません。

```txt
Maybe
Either
IO
Parser
State
Reader
List
```

など、多くの計算の合成を表します。

Monadの本質は、

```txt
文脈付きの計算を、前の結果に応じて次へつなぐ
```

ことです。

---

## 第26章: do記法

### 学ぶこと

```txt
do
<-
IO
Maybe
Either
Parser
```

### 例

```haskell
main :: IO ()
main = do
  name <- getLine
  putStrLn ("Hello, " ++ name)
```

### なぜ重要か

`do` 記法は命令型に見えますが、本質的にはモナド計算の合成です。

つまりHaskellでは、

```txt
命令を書いている
```

のではなく、

```txt
計算を順番に合成している
```

と考えます。

---

# 第9部: Effect と IO の設計

## 第27章: 副作用とは何か

### 学ぶこと

```txt
副作用
IO
Effect
純粋な計算
外界との相互作用
```

### 副作用の例

```txt
標準出力
標準入力
ファイル読み書き
HTTP通信
DBアクセス
ログ
乱数
現在時刻
例外
DOM操作
```

### Haskellの思想

Haskellは副作用を禁止しているわけではありません。

副作用を、

```txt
純粋な計算と混ぜない
型に出す
境界に集める
```

という設計をします。

---

## 第28章: Pure Core / Effectful Shell

### 学ぶこと

```txt
純粋な中心
副作用の境界
依存の注入
テストしやすい設計
```

### 設計例

```txt
HTTPを呼ぶ
  ↓
JSONを受け取る
  ↓
純粋関数で変換する
  ↓
DBに保存する
```

このとき、変換ロジックは純粋関数にします。

```haskell
convert :: ApiResponse -> Either DomainError DomainModel
```

I/Oは外側に置きます。

```haskell
program :: IO ()
```

### なぜ重要か

純粋な関数はテストしやすく、再利用しやすく、推論しやすいです。

Haskellらしいアプリケーション設計では、

```txt
副作用を薄く
純粋ロジックを厚く
```

します。

---

## 第29章: Reader / State / Writer

### 学ぶこと

```txt
Reader
State
Writer
環境
状態
ログ
```

### なぜ必要か

`IO` だけで全てを書くと、設計が雑になります。

```haskell
Config -> IO a
```

のような依存をどう扱うか、状態をどう扱うか、ログをどう扱うかを抽象化するために、Reader、State、Writerを学びます。

---

## 第30章: モナド変換子

### 学ぶこと

```txt
MaybeT
ExceptT
ReaderT
StateT
Monad Transformer
mtl
```

### なぜ必要か

現実のアプリケーションでは、複数の文脈が重なります。

```txt
設定を読む
失敗するかもしれない
ログを出す
IOする
```

これらをどう合成するかが、モナド変換子のテーマです。

### 実務で重要な設計

```haskell
newtype App a = App
  { runApp :: ReaderT Env IO a
  }
```

このような構成は、実務Haskellでよく出てきます。

---

# 第10部: エラー設計

## 第31章: partial function を避ける

### 学ぶこと

```txt
head
tail
read
fromJust
undefined
error
bottom
```

### なぜ危険か

```haskell
head []
```

は実行時エラーになります。

Haskellは型が強いですが、すべての実行時エラーを消せるわけではありません。

`undefined` や非停止計算のようなものは、意味論上 `bottom` と呼ばれます。Haskell 2010 Report でも、エラーは意味論的には bottom と等価に扱われると説明されています。([Haskell][4])

### Haskellらしい回避

```haskell
safeHead :: [a] -> Maybe a
safeHead [] = Nothing
safeHead (x:_) = Just x
```

失敗可能性を型に出します。

---

## 第32章: エラーを型で設計する

### 学ぶこと

```txt
DomainError
ParseError
ValidationError
Either
ExceptT
```

### 例

```haskell
data RegistrationError
  = InvalidEmail
  | PasswordTooShort
  | UserAlreadyExists
```

```haskell
register :: RegistrationInput -> Either RegistrationError User
```

### なぜ重要か

エラーは文字列ではなく、ドメインの一部です。

Haskellらしい設計では、エラーも型として設計します。

---

# 第11部: モジュール・プロジェクト・ツール

## 第33章: モジュールシステム

### 学ぶこと

```txt
module
import
qualified import
export list
抽象データ型
```

### なぜ重要か

Haskellでは、モジュールによって名前空間を分け、公開するものを制御します。

```haskell
module User
  ( User
  , mkUser
  , userEmail
  ) where
```

コンストラクタを公開しなければ、不正な値を外部から作れなくできます。

これは、

```txt
型で制約する
モジュールで構築方法を制限する
```

という設計です。

---

## 第34章: Cabal / Stack / Hackage

### 学ぶこと

```txt
Cabal
cabal-install
Stack
Hackage
Stackage
package.yaml
.cabal
依存関係
```

### 位置づけ

CabalはHaskellのライブラリやプログラムをビルド・パッケージングするためのシステムで、Haskell公式サイトでも、パッケージ作者や配布者が移植性のある形でアプリケーションをビルドできる共通インターフェースと説明されています。([Haskell][5])

Stackは再現性のあるビルド計画、複数パッケージのプロジェクト、一貫したコマンド体系を重視するツールとして説明され、GHC、Cabal、Hackage、Stackageの上に成り立つエコシステムとして位置づけられています。([Stack][6])

### Haskell専門家に必要な力

```txt
ライブラリプロジェクトを作れる
実行可能アプリを作れる
テストスイートを分けられる
依存バージョンを管理できる
Hackageの型ドキュメントを読める
```

---

## 第35章: Haskell Language Server

### 学ぶこと

```txt
HLS
LSP
型ホバー
補完
診断
定義ジャンプ
フォーマット
```

Haskell Language Server は公式のHaskell Language Server実装で、診断、ホバー、シグネチャヘルプ、定義ジャンプ、補完、フォーマット、コードアクションなどの機能を提供します。([Haskell Language Server][7])

### なぜ重要か

Haskellでは型エラーを読む力が重要です。
HLSは、型を常に見ながら開発するための補助線になります。

---

# 第12部: テストと仕様

## 第36章: 例ベースのテスト

### 学ぶこと

```txt
Hspec
tasty
unit test
golden test
doctest
```

### なぜ必要か

型は多くのバグを防ぎますが、仕様ミスまでは防げません。

```txt
型で構造を保証する
テストで振る舞いを保証する
```

という役割分担が必要です。

---

## 第37章: プロパティベーステスト

### 学ぶこと

```txt
QuickCheck
Hedgehog
Arbitrary
property
law testing
```

QuickCheckは、プログラムの性質をランダムテストするためのHaskellライブラリとして説明されています。([GitHub][8])

### 例

```haskell
prop_reverseReverse :: [Int] -> Bool
prop_reverseReverse xs =
  reverse (reverse xs) == xs
```

### なぜHaskellらしいのか

Haskellでは、関数が純粋であるため、

```txt
入力を生成する
性質を検査する
反例を探す
```

というテストと相性が良いです。

特に型クラスの法則は、QuickCheckで検査する文化があります。

---

# 第13部: パーサー・DSL・関数型設計

## 第38章: パーサーコンビネータ

### 学ぶこと

```txt
Parser
parsec
megaparsec
attoparsec
Alternative
Applicative parser
Monad parser
```

### なぜHaskellらしいのか

パーサーを「状態を持つ処理」としてではなく、

```txt
小さなパーサーを合成して大きなパーサーを作る
```

と考えます。

```haskell
parserA <|> parserB
```

のように、パーサーそのものが合成可能な値になります。

---

## 第39章: DSL設計

### 学ぶこと

```txt
Embedded DSL
Free Monad
Tagless Final
GADT DSL
Interpreter pattern
```

### なぜ重要か

Haskellでは、型と関数合成を使って、小さな言語を作ることが得意です。

例えば、

```txt
クエリ言語
設定言語
ワークフロー
ビルドルール
検証ルール
```

などをHaskell内に埋め込んだDSLとして設計できます。

---

# 第14部: Lens とデータアクセス

## 第40章: Lensとは何か

### 学ぶこと

```txt
Lens
Prism
Traversal
Optics
Getter
Setter
```

### なぜ必要か

Haskellのデータは不変です。

ネストしたデータを更新する場合、

```txt
元の値を壊さずに
一部だけ変えた新しい値を作る
```

必要があります。

Lensは、それを合成可能にする抽象です。

### 注意

Lensは強力ですが、初心者が早く学びすぎるとHaskellの本質を見失いやすいです。

このチュートリアルでは、ADT、Functor、Applicative、Traversableを理解した後に扱います。

---

# 第15部: 並行・並列・STM

## 第41章: 軽量スレッドと async

### 学ぶこと

```txt
forkIO
async
wait
race
concurrently
```

### なぜHaskellと相性が良いか

純粋な計算は外部状態を勝手に変更しません。

そのため、副作用のある部分を明確に分けておくと、並行処理の見通しが良くなります。

---

## 第42章: STM

### 学ぶこと

```txt
STM
TVar
atomically
retry
orElse
```

### なぜ重要か

STMは Software Transactional Memory です。

共有状態をロックで直接扱うのではなく、トランザクションとして扱います。

Haskellらしい並行処理では、

```txt
危険な共有状態操作を抽象化する
型で操作範囲を区別する
```

という発想が重要です。

---

# 第16部: 性能・最適化・GHC

## 第43章: GHCの基礎

### 学ぶこと

```txt
GHC
GHCi
runghc
コンパイル
RTS
Core
最適化
```

GHC User’s Guide は、GHCを Haskell 2010 向けの対話的・バッチ式コンパイルシステムとして扱い、GHCi、runghc、GHCの使い方、言語拡張、プロファイリング、デバッグ、FFI、JavaScript backend、WebAssembly backendなどを含む広範な内容を文書化しています。([Haskell Downloads][9])

### なぜ重要か

Haskell専門家は、Haskellの表層構文だけでなく、

```txt
遅延評価がどう実行されるか
最適化がどう効くか
メモリをどう使うか
```

を理解する必要があります。

---

## 第44章: プロファイリング

### 学ぶこと

```txt
time profiling
heap profiling
cost centre
eventlog
criterion
weigh
```

### なぜ必要か

Haskellでは、遅延評価のために性能問題が直感と違う場所に現れることがあります。

```txt
どこで計算されているか
どこでメモリを保持しているか
どのサンクが溜まっているか
```

を観察する必要があります。

---

## 第45章: 正格性制御

### 学ぶこと

```txt
seq
deepseq
BangPatterns
StrictData
foldl'
UNPACK
```

### なぜ重要か

Haskellらしさは遅延評価にありますが、実務では正格性の制御も必要です。

専門家は、

```txt
遅延にする理由
正格にする理由
```

を説明できなければなりません。

---

# 第17部: 高度な型システム

## 第46章: kind と高階型

### 学ぶこと

```txt
kind
*
Type
* -> *
高階型
高カインド型
Functor kind
Monad kind
```

### 補足

会話で出てきた「高階型」は、文脈によって2つの意味で使われがちです。

```txt
高階関数: 関数を受け取る/返す関数
高カインド型: 型を受け取る型、例 Maybe, [], IO
```

Haskellの `Functor` や `Monad` は、`Maybe` や `IO` のような型コンストラクタに対して定義されます。

---

## 第47章: GADT

### 学ぶこと

```txt
GADTs
式の型をより細かく表す
型安全なAST
```

### 例

```haskell
data Expr a where
  IntLit  :: Int -> Expr Int
  BoolLit :: Bool -> Expr Bool
  Add     :: Expr Int -> Expr Int -> Expr Int
```

### なぜ重要か

GADTを使うと、式の型をデータ構造そのものに埋め込めます。

これにより、

```txt
Bool と Int を間違えて足す
```

ような不正な式を型で防げます。

---

## 第48章: Phantom Types

### 学ぶこと

```txt
Phantom type
状態を型に持たせる
権限を型に持たせる
```

### 例

```haskell
data Authenticated
data Anonymous

newtype User session = User UserId
```

### なぜ重要か

値には現れない情報を型に持たせることで、

```txt
認証済みでないと呼べない関数
検証済みでないと保存できない値
```

などを表現できます。

---

## 第49章: DataKinds / TypeFamilies / Type-level programming

### 学ぶこと

```txt
DataKinds
TypeFamilies
TypeOperators
TypeLits
型レベル自然数
型レベル文字列
```

### なぜ重要か

高度なHaskellでは、値レベルだけでなく型レベルでも計算します。

ただし、型レベルプログラミングは濫用すると保守性を下げます。

この章では、

```txt
型で守るべき制約
実行時に検証すべき制約
```

の境界を学びます。

---

## 第50章: RankNTypes / Existential Types

### 学ぶこと

```txt
RankNTypes
forall
existential types
抽象化
コールバック
継続
```

### なぜ重要か

通常の多相性よりも高度な抽象を扱うために必要です。

ライブラリ設計、Lens、ST、Resource管理などで重要になります。

---

## 第51章: Deriving と Generics

### 学ぶこと

```txt
deriving
DeriveGeneric
DerivingStrategies
DerivingVia
Generic
aeson
```

### なぜ重要か

Haskellでは、型を定義した後に、

```txt
Show
Eq
Ord
Generic
JSON変換
```

などを自動導出できます。

ただし、導出は便利である一方、意味が正しいかを考える必要があります。

---

# 第18部: 実務アプリケーション設計

## 第52章: CLIアプリを作る

### 学ぶこと

```txt
optparse-applicative
text
bytestring
file IO
logging
```

### 作るもの

```txt
JSONファイルを読み込むCLI
設定ファイルを読むCLI
エラーをEitherで設計したCLI
```

---

## 第53章: Web APIを作る

### 学ぶこと

```txt
servant
wai
warp
aeson
http-client
```

### HaskellらしいWeb API設計

```txt
ルーティングを型で表す
リクエスト/レスポンスを型で表す
エラーを型で表す
```

---

## 第54章: DBを扱う

### 学ぶこと

```txt
persistent
beam
postgresql-simple
transaction
connection pool
```

### 設計上の問い

```txt
DBエラーをどこでEitherに変換するか
ドメイン型とDB型を分けるか
不正な状態をDBから読んだ場合どうするか
```

---

## 第55章: JSONと外部API

### 学ぶこと

```txt
aeson
FromJSON
ToJSON
newtype wrapper
外部スキーマと内部ドメインの分離
```

### なぜ重要か

外部APIのJSONを、そのままドメイン型にしないことが重要です。

```txt
外部表現
内部表現
検証済みドメインモデル
```

を分けます。

---

# 第19部: FFI・JS・WASM・Nix

## 第56章: FFI

### 学ぶこと

```txt
Foreign Function Interface
C連携
安全な境界
marshal
```

Haskell 2010 Report には Foreign Function Interface の章も含まれており、Haskellは閉じた研究用言語ではなく、外部言語との連携も標準的なテーマとして扱われます。

---

## 第57章: JavaScript / WebAssembly backend

### 学ぶこと

```txt
GHC JavaScript backend
GHC WebAssembly backend
PureScriptとの比較
フロントエンドとの接続
```

### PureScriptとの関係

PureScriptはHaskellにかなり似たJavaScript向け言語です。

一方、HaskellそのものもGHCのバックエンドとしてJavaScriptやWebAssembly方面に展開しています。

ここでは、

```txt
HaskellをWebで使う
PureScriptを使う
Elmを使う
TypeScript + Effect/fp-tsを使う
```

の違いを比較します。

---

## 第58章: Nixと再現可能ビルド

### 学ぶこと

```txt
Nix
NixOS
haskell.nix
再現可能な開発環境
CI
```

### なぜ重要か

Haskellプロジェクトでは、GHCバージョン、依存パッケージ、OSライブラリの整合性が重要です。

NixはHaskellそのものではありませんが、Haskell実務では重要な周辺技術です。

---

# 第20部: Haskell周辺言語との比較

## 第59章: PureScript

### 学ぶこと

```txt
Haskell風構文
型クラス
代数的データ型
パターンマッチ
JavaScript出力
正格評価
```

### Haskellとの違い

```txt
Haskell: 非正格・遅延評価
PureScript: 基本的に正格評価
```

PureScriptは、フロントエンドエンジニアがHaskell的な型設計をJavaScript圏で使うときに有力です。

---

## 第60章: Elm

### 学ぶこと

```txt
純粋関数型
Web UI
The Elm Architecture
副作用の分離
```

### Haskellとの違い

ElmはHaskellより意図的にシンプルです。

```txt
型クラスなし
高カインド型なし
学習しやすい
Web UIに特化
```

---

## 第61章: Clean

### 学ぶこと

```txt
純粋関数型
遅延評価
Haskellに近い言語
一意型
```

Cleanは、純粋・遅延評価という意味ではHaskellに近い言語です。

---

## 第62章: OCaml / F# / Scala

### 学ぶこと

```txt
ML系
実務関数型
型推論
パターンマッチ
非純粋
正格評価
```

### Haskellとの違い

```txt
Haskell: 純粋性と遅延評価が中心
OCaml/F#/Scala: 実務的な関数型・命令型の混合
```

ScalaはCatsやZIOなどを使うとHaskell風の設計に近づきます。

---

## 第63章: Idris / Agda / Lean / F*

### 学ぶこと

```txt
依存型
証明
型駆動開発
定理証明
全域性
```

### Haskellとの違い

Haskellは高度な型システムを持ちますが、基本的には定理証明器ではありません。

Idris、Agda、Lean、F* は、型で証明や仕様をより強く扱う方向の言語です。

---

## 第64章: Roc / Unison / Gleam

### 学ぶこと

```txt
新しい関数型言語
型安全
Effect
分散
BEAM
```

### Haskellとの関係

これらはHaskellの影響を受けつつも、それぞれ別の目的を持っています。

```txt
Roc: 新しい関数型アプリケーション言語
Unison: コードをハッシュで管理する独自設計
Gleam: Erlang/BEAM上の型安全関数型言語
```

---

## 第65章: TypeScript + Effect / fp-ts

### 学ぶこと

```txt
Either
Option
Effect
Task
関数合成
型付き副作用
```

### Haskellとの関係

TypeScriptのままHaskell的な考え方を取り入れるなら、Effectやfp-tsが候補になります。

ただし、Haskellとは違って、言語全体が純粋性を強制するわけではありません。

---

# 第21部: Haskellの歴史と哲学

## 第66章: なぜHaskellは生まれたのか

### 学ぶこと

```txt
Haskellの歴史
研究言語としての背景
標準化
Haskell 98
Haskell 2010
GHC
```

Haskellの歴史については、Hudak、Hughes、Peyton Jones、Wadlerらによる “A History of Haskell: Being Lazy With Class” が代表的な資料で、Haskellの起源、設計原則、技術的貢献、実装、ツール、応用、影響を扱う論文として紹介されています。([Microsoft][10])

### なぜ歴史を学ぶのか

Haskellの設計は偶然ではありません。

```txt
純粋性
遅延評価
型クラス
モナド的I/O
```

は、研究と実用の間で生まれた設計判断です。

歴史を学ぶと、

```txt
なぜHaskellはこうなっているのか
なぜ他の言語と違うのか
```

が見えてきます。

---

## 第67章: Haskellの哲学

### 中心思想

```txt
副作用を分離する
型で設計する
関数を合成する
不正な状態を作れなくする
抽象には法則を求める
小さな純粋関数を信頼する
```

### Haskellらしい判断基準

Haskellでは、次のように考えます。

```txt
この関数は純粋にできるか
この失敗は型に出せるか
この状態はADTで表せるか
このIDはnewtypeにすべきか
この抽象は法則を持つか
MonadよりApplicativeで十分ではないか
IOをもっと外側に追い出せないか
```

---

# 第22部: プロフェッショナルへの総合演習

## 第68章: 小規模演習

### 作るもの

```txt
安全なリスト操作ライブラリ
JSONパーサー
CLI Todoアプリ
CSV変換ツール
```

### 評価基準

```txt
partial functionを使っていない
Maybe/Eitherで失敗を表している
newtypeで意味を分けている
純粋ロジックとIOが分離されている
テストがある
```

---

## 第69章: 中規模演習

### 作るもの

```txt
ユーザー登録API
認証付きCLI
Markdownパーサー
小さなインタプリタ
並行Webクローラ
```

### 評価基準

```txt
ドメイン型が明確
エラー型が明確
ReaderTやExceptTを適切に使っている
QuickCheckで性質をテストしている
プロファイリングできる
```

---

## 第70章: 大規模演習

### 作るもの

```txt
型安全なWeb API
DSLとインタプリタ
パッケージとして公開できるライブラリ
STMを使った並行システム
Parser + Evaluator + Pretty Printer を持つ小言語
```

### 評価基準

```txt
型が設計を説明している
モジュール境界がきれい
副作用が制御されている
抽象が法則を持つ
ベンチマークがある
ドキュメントがある
依存関係が整理されている
```

---

# 第23部: 専門家レベルのチェックリスト

## 言語理解

```txt
純粋関数型を説明できる
参照透過性を説明できる
非正格意味論と遅延評価を区別できる
正格評価が必要な場面を説明できる
bottom / undefined / error の危険性を説明できる
```

## 型設計

```txt
ADTでドメインを表現できる
不正な状態を型で表現できなくできる
Maybe/Eitherを適切に使える
newtypeを自然に使える
型クラスとその法則を説明できる
高カインド型を理解している
```

## 抽象

```txt
Functorを使える
Applicativeを使える
Monadを使える
Traversableを使える
Monad Transformerを使える
ReaderT設計を理解している
Lens/Opticsの意義を理解している
```

## 実務

```txt
Cabalプロジェクトを作れる
Stackプロジェクトを読める
HLSを使える
Hackageドキュメントを読める
テストを書ける
QuickCheckで法則を検査できる
プロファイリングできる
CI/CDに組み込める
```

## 高度な型

```txt
GADTsを使える
Phantom Typesを使える
DataKindsを読める
TypeFamiliesを読める
RankNTypesを読める
DerivingViaを使える
型レベル設計のやりすぎを避けられる
```

## 設計判断

```txt
この抽象は本当に必要か判断できる
型を複雑にしすぎない判断ができる
IOを境界に追いやれる
性能問題を測定して改善できる
読みやすさと抽象度のバランスを取れる
```

---

# これまでの会話キーワード対応表

| キーワード                       | このチュートリアルでの扱い |
| --------------------------- | ------------- |
| 純粋関数型                       | 第0章、第4章、第27章  |
| 静的型付け                       | 第8章           |
| 型推論                         | 第8章           |
| 代数的データ型                     | 第11章          |
| パターンマッチ                     | 第12章          |
| 型クラス                        | 第20章〜第22章     |
| 遅延評価                        | 第18章          |
| 非正格意味論                      | 第18章          |
| 正格評価                        | 第19章、第59章     |
| モナド                         | 第25章          |
| Effect                      | 第27章〜第30章     |
| IO                          | 第1章、第27章      |
| 参照透過性                       | 第4章           |
| 不変性                         | 第3章           |
| 多相的                         | 第9章           |
| 高階関数                        | 第6章           |
| 高階型 / 高カインド型                | 第46章          |
| カリー化                        | 第5章           |
| 部分適用                        | 第5章           |
| 関数合成                        | 第7章           |
| ポイントフリー                     | 第7章           |
| 再帰                          | 第15章          |
| fold                        | 第16章          |
| Maybe                       | 第13章          |
| Either                      | 第14章          |
| Result型的エラーハンドリング           | 第14章、第32章     |
| newtype                     | 第10章          |
| 不正な状態を型で表現できなくする            | 第11章          |
| 型クラスの法則                     | 第21章          |
| Functor                     | 第23章          |
| Applicative                 | 第24章          |
| Monad                       | 第25章          |
| do記法                        | 第26章          |
| bottom / undefined          | 第31章          |
| GHC拡張                       | 第17部全体        |
| GHC2024                     | 推奨環境、第17部     |
| 型レベルプログラミング                 | 第49章          |
| モジュールシステム                   | 第33章          |
| FFI                         | 第56章          |
| STM                         | 第42章          |
| プロパティベーステスト                 | 第37章          |
| QuickCheck                  | 第37章          |
| パーサーコンビネータ                  | 第38章          |
| Lens                        | 第40章          |
| PureScript                  | 第59章          |
| Elm                         | 第60章          |
| Clean                       | 第61章          |
| OCaml / F# / Scala          | 第62章          |
| Idris / Agda / Lean / F*    | 第63章          |
| Roc / Unison / Gleam        | 第64章          |
| Nix                         | 第58章          |
| TypeScript + Effect / fp-ts | 第65章          |

---

# 最終的な教材構成イメージ

このチュートリアルを本や講座にするなら、全体は次のような構成になります。

```txt
第0部   Haskellとは何か
第1部   Hello, World! と IO
第2部   値・式・関数
第3部   型で考える
第4部   ADTとパターンマッチ
第5部   再帰・リスト・fold
第6部   遅延評価と正格性
第7部   型クラス
第8部   Functor / Applicative / Monad
第9部   EffectとIO設計
第10部  エラー設計
第11部  モジュール・ツール・パッケージ
第12部  テストと仕様
第13部  パーサー・DSL
第14部  Lensとデータアクセス
第15部  並行・並列・STM
第16部  性能・GHC・プロファイリング
第17部  高度な型システム
第18部  実務アプリケーション
第19部  FFI・JS・WASM・Nix
第20部  Haskell周辺言語との比較
第21部  歴史と哲学
第22部  総合演習
第23部  専門家チェックリスト
```

---

# このチュートリアルの核

最後に、この構成全体の核を一文でまとめると、こうです。

**Haskellを学ぶとは、構文を覚えることではなく、「値」「型」「副作用」「合成」「法則」でプログラムを設計する考え方を身につけることです。**

Haskellらしさは、単に `map` や `fold` を使うことではありません。

本質は、

```txt
副作用を型で分ける
失敗を型で表す
状態を型で表す
不正な状態を作れなくする
小さな純粋関数を合成する
抽象に法則を求める
必要なところだけ高度な型を使う
```

という設計思想です。

[1]: https://www.haskell.org/ "Haskell Language"
[2]: https://www.haskell.org/downloads/ "Downloads"
[3]: https://ghc.gitlab.haskell.org/ghc/doc/users_guide/exts/control.html "6.1.1. Controlling editions and extensions — Glasgow Haskell Compiler 9.15.20260306 User's Guide"
[4]: https://www.haskell.org/definition/haskell2010.pdf?utm_source=chatgpt.com "Haskell 2010 Language Report"
[5]: https://www.haskell.org/cabal/ "The Haskell Cabal | Overview"
[6]: https://docs.haskellstack.org/en/stable/ "Stack"
[7]: https://haskell-language-server.readthedocs.io/ "haskell-language-server — haskell-language-server 2.14.0.0 documentation"
[8]: https://github.com/nick8325/quickcheck "GitHub - nick8325/quickcheck: Automatic testing of Haskell programs. · GitHub"
[9]: https://downloads.haskell.org/ghc/latest/docs/users_guide/ "Welcome to the GHC User’s Guide — Glasgow Haskell Compiler 9.14.1 User's Guide"
[10]: https://www.microsoft.com/en-us/research/publication/a-history-of-haskell-being-lazy-with-class/ "A History of Haskell: being lazy with class - Microsoft Research"
