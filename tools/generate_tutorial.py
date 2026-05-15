#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import textwrap


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Chapter:
    number: int
    part: int
    part_title: str
    title: str
    focus: str
    terms: tuple[str, ...]
    example: str
    expected: str


PARTS = {
    0: "Haskellを学ぶ前に",
    1: "Hello, World! から始める",
    2: "値・式・関数",
    3: "型で考える",
    4: "代数的データ型とパターンマッチ",
    5: "再帰・リスト・fold",
    6: "遅延評価と非正格意味論",
    7: "型クラス",
    8: "Functor / Applicative / Monad",
    9: "Effect と IO の設計",
    10: "エラー設計",
    11: "モジュール・プロジェクト・ツール",
    12: "テストと仕様",
    13: "パーサー・DSL・関数型設計",
    14: "Lens とデータアクセス",
    15: "並行・並列・STM",
    16: "性能・最適化・GHC",
    17: "高度な型システム",
    18: "実務アプリケーション設計",
    19: "FFI・JS・WASM・Nix",
    20: "Haskell周辺言語との比較",
    21: "Haskellの歴史と哲学",
    22: "プロフェッショナルへの総合演習",
}


def hs(code: str) -> str:
    return textwrap.dedent(code).strip()


GENERIC_EXAMPLE = hs(
    """
    module Main where

    main :: IO ()
    main = putStrLn "この章の例は本文の問いに合わせて変更してください。"
    """
)

EXAMPLES: dict[int, tuple[str, str]] = {
    27: (hs("""
    module Main where

    pureMessage :: String -> String
    pureMessage name = "Hello, " ++ name

    main :: IO ()
    main = putStrLn (pureMessage "Ada")
    """), "Hello, Ada"),
    28: (hs("""
    module Main where

    normalize :: String -> String
    normalize = unwords . words

    main :: IO ()
    main = do
      let raw = "  Haskell   Tutorial  "
      putStrLn (normalize raw)
    """), "Haskell Tutorial"),
    29: (hs("""
    module Main where

    newtype Config = Config { greeting :: String }

    greet :: Config -> String -> String
    greet config name = greeting config ++ ", " ++ name

    main :: IO ()
    main = putStrLn (greet (Config "Hello") "Ada")
    """), "Hello, Ada"),
    30: (hs("""
    module Main where

    data AppError = MissingName deriving Show
    newtype Env = Env { defaultName :: String }

    runApp :: Env -> Maybe String -> Either AppError String
    runApp env input =
      Right ("Hello, " ++ maybe (defaultName env) id input)

    main :: IO ()
    main = print (runApp (Env "guest") Nothing)
    """), "Right \"Hello, guest\""),
    31: (hs("""
    module Main where

    safeHead :: [a] -> Maybe a
    safeHead [] = Nothing
    safeHead (x:_) = Just x

    main :: IO ()
    main = print (safeHead ([] :: [Int]))
    """), "Nothing"),
    32: (hs("""
    module Main where

    data RegistrationError = EmptyEmail | ShortPassword deriving Show

    register :: String -> String -> Either RegistrationError String
    register "" _ = Left EmptyEmail
    register _ password | length password < 8 = Left ShortPassword
    register email _ = Right email

    main :: IO ()
    main = print (register "ada@example.com" "secret")
    """), "Left ShortPassword"),
    33: (hs("""
    module Main where

    newtype Email = Email String deriving Show

    mkEmail :: String -> Maybe Email
    mkEmail value
      | '@' `elem` value = Just (Email value)
      | otherwise = Nothing

    main :: IO ()
    main = print (mkEmail "ada@example.com")
    """), "Just (Email \"ada@example.com\")"),
    34: (hs("""
    module Main where

    main :: IO ()
    main = putStrLn "cabal build all はプロジェクト全体をビルドします"
    """), "cabal build all はプロジェクト全体をビルドします"),
    35: (hs("""
    module Main where

    add :: Int -> Int -> Int
    add x y = x + y

    main :: IO ()
    main = print (add 20 22)
    """), "42"),
    36: (hs("""
    module Main where

    double :: Int -> Int
    double x = x * 2

    main :: IO ()
    main = print (double 21 == 42)
    """), "True"),
    37: (hs("""
    module Main where

    propReverseReverse :: [Int] -> Bool
    propReverseReverse xs = reverse (reverse xs) == xs

    main :: IO ()
    main = print (propReverseReverse [1,2,3])
    """), "True"),
    38: (hs("""
    module Main where

    parseDigit :: Char -> Maybe Int
    parseDigit c
      | c >= '0' && c <= '9' = Just (fromEnum c - fromEnum '0')
      | otherwise = Nothing

    main :: IO ()
    main = print (parseDigit '7')
    """), "Just 7"),
    39: (hs("""
    module Main where

    data Expr = Lit Int | Add Expr Expr

    eval :: Expr -> Int
    eval (Lit n) = n
    eval (Add a b) = eval a + eval b

    main :: IO ()
    main = print (eval (Add (Lit 10) (Lit 32)))
    """), "42"),
    40: (hs("""
    module Main where

    data User = User { name :: String, age :: Int } deriving Show

    birthday :: User -> User
    birthday user = user { age = age user + 1 }

    main :: IO ()
    main = print (birthday (User "Ada" 36))
    """), "User {name = \"Ada\", age = 37}"),
    41: (hs("""
    module Main where

    import Control.Concurrent

    main :: IO ()
    main = do
      done <- newEmptyMVar
      _ <- forkIO (putMVar done "finished")
      takeMVar done >>= putStrLn
    """), "finished"),
    42: (hs("""
    module Main where

    import Control.Concurrent.STM

    main :: IO ()
    main = do
      counter <- newTVarIO (0 :: Int)
      atomically (modifyTVar' counter (+1))
      readTVarIO counter >>= print
    """), "1"),
    43: (hs("""
    module Main where

    main :: IO ()
    main = putStrLn "ghc -O2 Main.hs で最適化ビルドできます"
    """), "ghc -O2 Main.hs で最適化ビルドできます"),
    44: (hs("""
    module Main where

    work :: Int -> Int
    work n = sum [1..n]

    main :: IO ()
    main = print (work 1000)
    """), "500500"),
    45: (hs("""
    {-# LANGUAGE BangPatterns #-}
    module Main where

    strictSum :: [Int] -> Int
    strictSum = go 0
      where
        go !acc [] = acc
        go !acc (x:xs) = go (acc + x) xs

    main :: IO ()
    main = print (strictSum [1..100])
    """), "5050"),
    46: (hs("""
    module Main where

    wrapMaybe :: a -> Maybe a
    wrapMaybe = Just

    main :: IO ()
    main = print (wrapMaybe "kind * -> * の例")
    """), "Just \"kind * -> * の例\""),
    47: (hs("""
    {-# LANGUAGE GADTs #-}
    module Main where

    data Expr a where
      IntLit :: Int -> Expr Int
      Add :: Expr Int -> Expr Int -> Expr Int

    eval :: Expr a -> a
    eval (IntLit n) = n
    eval (Add a b) = eval a + eval b

    main :: IO ()
    main = print (eval (Add (IntLit 20) (IntLit 22)))
    """), "42"),
    48: (hs("""
    module Main where

    data Raw
    data Verified
    newtype Email state = Email String deriving Show

    verify :: Email Raw -> Maybe (Email Verified)
    verify (Email value)
      | '@' `elem` value = Just (Email value)
      | otherwise = Nothing

    main :: IO ()
    main = print (verify (Email "a@example.com"))
    """), "Just (Email \"a@example.com\")"),
    49: (hs("""
    {-# LANGUAGE DataKinds #-}
    module Main where

    data Visibility = Public | Private
    newtype Document (v :: Visibility) = Document String deriving Show

    main :: IO ()
    main = print (Document "guide" :: Document 'Public)
    """), "Document \"guide\""),
    50: (hs("""
    {-# LANGUAGE RankNTypes #-}
    module Main where

    applyToBoth :: (forall a. a -> a) -> (Int, Bool)
    applyToBoth f = (f 1, f True)

    main :: IO ()
    main = print (applyToBoth id)
    """), "(1,True)"),
    51: (hs("""
    {-# LANGUAGE DeriveGeneric #-}
    module Main where

    import GHC.Generics (Generic)

    data User = User String Int deriving (Show, Eq, Generic)

    main :: IO ()
    main = print (User "Ada" 36 == User "Ada" 36)
    """), "True"),
    52: (hs("""
    module Main where

    renderTodo :: String -> String
    renderTodo title = "[ ] " ++ title

    main :: IO ()
    main = putStrLn (renderTodo "write CLI")
    """), "[ ] write CLI"),
    53: (hs("""
    module Main where

    data Route = GetUser Int | Health

    describe :: Route -> String
    describe Health = "GET /health"
    describe (GetUser n) = "GET /users/" ++ show n

    main :: IO ()
    main = putStrLn (describe (GetUser 42))
    """), "GET /users/42"),
    54: (hs("""
    module Main where

    data DbUser = DbUser Int String
    data User = User String deriving Show

    toDomain :: DbUser -> Either String User
    toDomain (DbUser _ email)
      | '@' `elem` email = Right (User email)
      | otherwise = Left "invalid email in database"

    main :: IO ()
    main = print (toDomain (DbUser 1 "a@example.com"))
    """), "Right (User \"a@example.com\")"),
    55: (hs("""
    module Main where

    data ExternalUser = ExternalUser String
    newtype Email = Email String deriving Show

    validate :: ExternalUser -> Maybe Email
    validate (ExternalUser value)
      | '@' `elem` value = Just (Email value)
      | otherwise = Nothing

    main :: IO ()
    main = print (validate (ExternalUser "a@example.com"))
    """), "Just (Email \"a@example.com\")"),
    56: (hs("""
    module Main where

    -- 実際のFFIでは foreign import ccall を使う。
    cBoundary :: Int -> Int
    cBoundary n = n + 1

    main :: IO ()
    main = print (cBoundary 41)
    """), "42"),
    57: (hs("""
    module Main where

    viewModel :: String -> String
    viewModel name = "<h1>Hello, " ++ name ++ "</h1>"

    main :: IO ()
    main = putStrLn (viewModel "Web")
    """), "<h1>Hello, Web</h1>"),
    58: (hs("""
    module Main where

    main :: IO ()
    main = putStrLn "再現可能ビルドではGHCと依存関係のバージョンを固定します"
    """), "再現可能ビルドではGHCと依存関係のバージョンを固定します"),
    59: (hs("""
    module Main where

    main :: IO ()
    main = putStrLn "Haskellは非正格、PureScriptは基本的に正格評価です"
    """), "Haskellは非正格、PureScriptは基本的に正格評価です"),
    60: (hs("""
    module Main where

    data Msg = Increment | Decrement

    update :: Msg -> Int -> Int
    update Increment n = n + 1
    update Decrement n = n - 1

    main :: IO ()
    main = print (update Increment 41)
    """), "42"),
    61: (hs("""
    module Main where

    main :: IO ()
    main = putStrLn "Cleanも純粋性と遅延評価を重視する言語です"
    """), "Cleanも純粋性と遅延評価を重視する言語です"),
    62: (hs("""
    module Main where

    main :: IO ()
    main = putStrLn "OCaml/F#/Scalaは実務的な関数型と命令型を混ぜられます"
    """), "OCaml/F#/Scalaは実務的な関数型と命令型を混ぜられます"),
    63: (hs("""
    module Main where

    main :: IO ()
    main = putStrLn "依存型言語では型が証明の役割をさらに強く持ちます"
    """), "依存型言語では型が証明の役割をさらに強く持ちます"),
    64: (hs("""
    module Main where

    main :: IO ()
    main = putStrLn "Roc, Unison, Gleamは目的ごとにHaskellの影響を再設計しています"
    """), "Roc, Unison, Gleamは目的ごとにHaskellの影響を再設計しています"),
    65: (hs("""
    module Main where

    data Option a = None | Some a deriving Show

    main :: IO ()
    main = print (Some "TypeScriptでも似た抽象を作れる")
    """), "Some \"TypeScriptでも似た抽象を作れる\""),
    66: (hs("""
    module Main where

    main :: IO ()
    main = putStrLn "Haskellの設計は純粋性、遅延評価、型クラスの実験から育ちました"
    """), "Haskellの設計は純粋性、遅延評価、型クラスの実験から育ちました"),
    67: (hs("""
    module Main where

    decide :: Bool -> String
    decide canBePure =
      if canBePure then "純粋関数にする" else "IOの境界に置く"

    main :: IO ()
    main = putStrLn (decide True)
    """), "純粋関数にする"),
    68: (hs("""
    module Main where

    safeLast :: [a] -> Maybe a
    safeLast [] = Nothing
    safeLast xs = Just (last xs)

    main :: IO ()
    main = print (safeLast [1,2,3])
    """), "Just 3"),
    69: (hs("""
    module Main where

    data AppError = NotFound | InvalidInput deriving Show

    handle :: Maybe String -> Either AppError String
    handle Nothing = Left NotFound
    handle (Just "") = Left InvalidInput
    handle (Just value) = Right ("ok: " ++ value)

    main :: IO ()
    main = print (handle (Just "request"))
    """), "Right \"ok: request\""),
    70: (hs("""
    module Main where

    data Pipeline a = Step String a deriving Show

    build :: String -> Pipeline String
    build name = Step "parse -> validate -> run -> report" name

    main :: IO ()
    main = print (build "final project")
    """), "Step \"parse -> validate -> run -> report\" \"final project\""),
}


CHAPTERS = [
    Chapter(0, 0, PARTS[0], "Haskellとは何か", "手順ではなく意味を書く言語としてHaskellを見る", ("純粋関数型", "参照透過性", "遅延評価", "型で設計する"), hs("""
    module Main where

    double :: Int -> Int
    double x = x * 2

    main :: IO ()
    main = print (double 21)
    """), "42"),
    Chapter(1, 1, PARTS[1], "Hello, World! の本当の意味", "`IO ()` を命令ではなく値として理解する", ("main", "IO", "putStrLn", "アクション"), hs("""
    module Main where

    main :: IO ()
    main = putStrLn "Hello, World!"
    """), "Hello, World!"),
    Chapter(2, 1, PARTS[1], "GHCiで「型を見る」習慣を作る", "実装より先に型を読む習慣を作る", ("GHCi", ":t", ":info", "型推論"), hs("""
    module Main where

    -- GHCiでは次も試す:
    -- :t map
    -- :t filter
    -- :t putStrLn
    main :: IO ()
    main = putStrLn "GHCiでは :t で型を見る"
    """), "GHCiでは :t で型を見る"),
    Chapter(3, 2, PARTS[2], "変数ではなく「束縛」", "値は書き換える箱ではなく名前に束縛された意味だと捉える", ("値", "束縛", "不変性", "式"), hs("""
    module Main where

    answer :: Int
    answer = 40 + 2

    main :: IO ()
    main = print answer
    """), "42"),
    Chapter(4, 2, PARTS[2], "参照透過性", "式を同じ値で置き換えても意味が変わらない感覚を身につける", ("参照透過性", "純粋関数", "等式推論", "副作用"), hs("""
    module Main where

    add :: Int -> Int -> Int
    add x y = x + y

    main :: IO ()
    main = print (add 1 2 == 3)
    """), "True"),
    Chapter(5, 2, PARTS[2], "関数とは何か", "関数適用、カリー化、部分適用を設計の道具として使う", ("関数適用", "カリー化", "部分適用", "ラムダ式"), hs("""
    module Main where

    add :: Int -> Int -> Int
    add x y = x + y

    add10 :: Int -> Int
    add10 = add 10

    main :: IO ()
    main = print (add10 5)
    """), "15"),
    Chapter(6, 2, PARTS[2], "高階関数", "関数を値として渡し、処理の形を抽象化する", ("高階関数", "map", "filter", "fold"), hs("""
    module Main where

    main :: IO ()
    main = print (map (* 2) (filter odd [1..6]))
    """), "[2,6,10]"),
    Chapter(7, 2, PARTS[2], "関数合成とポイントフリースタイル", "小さな変換を合成して読みやすい処理の流れを作る", ("(.)", "($)", "ポイントフリー", "パイプライン"), hs("""
    module Main where

    process :: [Int] -> Int
    process = sum . map (* 2) . filter (> 0)

    main :: IO ()
    main = print (process [-1, 2, 3])
    """), "10"),
    Chapter(8, 3, PARTS[3], "型注釈と型推論", "型をコンパイラ向け情報ではなく設計メモとして使う", ("型注釈", "型推論", "静的型付け", "仕様"), hs("""
    module Main where

    fullName :: String -> String -> String
    fullName first last = first ++ " " ++ last

    main :: IO ()
    main = putStrLn (fullName "Ada" "Lovelace")
    """), "Ada Lovelace"),
    Chapter(9, 3, PARTS[3], "多相性", "型変数から関数ができることとできないことを読む", ("多相性", "型変数", "パラメトリック", "制約"), hs("""
    module Main where

    keep :: a -> a
    keep x = x

    main :: IO ()
    main = print (keep True)
    """), "True"),
    Chapter(10, 3, PARTS[3], "型エイリアスと newtype", "意味の違う値を型で分ける", ("type", "newtype", "ドメインモデル", "型安全"), hs("""
    module Main where

    newtype UserId = UserId Int deriving Show
    newtype ProductId = ProductId Int deriving Show

    showUser :: UserId -> String
    showUser (UserId n) = "user-" ++ show n

    main :: IO ()
    main = putStrLn (showUser (UserId 42))
    """), "user-42"),
    Chapter(11, 4, PARTS[4], "代数的データ型", "不正な状態を型で表現できなくする", ("data", "直和型", "直積型", "コンストラクタ"), hs("""
    module Main where

    data User = Guest | Registered String deriving Show

    describe :: User -> String
    describe Guest = "guest"
    describe (Registered email) = "registered: " ++ email

    main :: IO ()
    main = putStrLn (describe (Registered "a@example.com"))
    """), "registered: a@example.com"),
    Chapter(12, 4, PARTS[4], "パターンマッチ", "型の形に沿って安全に値を分解する", ("パターンマッチ", "case", "網羅性", "分解"), hs("""
    module Main where

    data Status = Draft | Published String

    label :: Status -> String
    label Draft = "draft"
    label (Published title) = "published: " ++ title

    main :: IO ()
    main = putStrLn (label (Published "Guide"))
    """), "published: Guide"),
    Chapter(13, 4, PARTS[4], "Maybe", "値がない可能性を型に出す", ("Maybe", "Just", "Nothing", "nullを避ける"), hs("""
    module Main where

    safeHead :: [a] -> Maybe a
    safeHead [] = Nothing
    safeHead (x:_) = Just x

    main :: IO ()
    main = print (safeHead [10, 20, 30])
    """), "Just 10"),
    Chapter(14, 4, PARTS[4], "Either", "失敗理由を型として扱う", ("Either", "Left", "Right", "エラー型"), hs("""
    module Main where

    parsePositive :: Int -> Either String Int
    parsePositive n
      | n > 0 = Right n
      | otherwise = Left "positive number required"

    main :: IO ()
    main = print (parsePositive 3)
    """), "Right 3"),
    Chapter(15, 5, PARTS[5], "ループではなく再帰", "データ構造の形に従って計算を書く", ("再帰", "基底ケース", "再帰ケース", "構造的再帰"), hs("""
    module Main where

    sumList :: [Int] -> Int
    sumList [] = 0
    sumList (x:xs) = x + sumList xs

    main :: IO ()
    main = print (sumList [1,2,3,4])
    """), "10"),
    Chapter(16, 5, PARTS[5], "map / filter / fold", "リスト処理を変換・選別・畳み込みとして読む", ("map", "filter", "foldr", "foldl'"), hs("""
    module Main where

    main :: IO ()
    main = print (foldr (+) 0 (map (*2) [1,2,3]))
    """), "12"),
    Chapter(17, 5, PARTS[5], "リスト内包表記", "宣言的にリストを生成する", ("リスト内包表記", "generator", "guard", "宣言的"), hs("""
    module Main where

    main :: IO ()
    main = print [x * 2 | x <- [1..6], odd x]
    """), "[2,6,10]"),
    Chapter(18, 6, PARTS[6], "遅延評価とは何か", "必要になるまで評価しないことで可能になる表現を理解する", ("遅延評価", "非正格", "サンク", "無限リスト"), hs("""
    module Main where

    ones :: [Int]
    ones = 1 : ones

    main :: IO ()
    main = print (take 5 ones)
    """), "[1,1,1,1,1]"),
    Chapter(19, 6, PARTS[6], "遅延評価は万能ではない", "遅延と正格性のトレードオフを知る", ("スペースリーク", "seq", "BangPatterns", "foldl'"), hs("""
    module Main where

    import Data.List (foldl')

    main :: IO ()
    main = print (foldl' (+) 0 [1..100])
    """), "5050"),
    Chapter(20, 7, PARTS[7], "型クラスとは何か", "型ごとの共通操作を法則付きの抽象として扱う", ("型クラス", "インスタンス", "制約", "オーバーロード"), hs("""
    module Main where

    class Printable a where
      printable :: a -> String

    instance Printable Bool where
      printable True = "yes"
      printable False = "no"

    main :: IO ()
    main = putStrLn (printable True)
    """), "yes"),
    Chapter(21, 7, PARTS[7], "型クラスの法則", "型が合うだけでなく期待される法則を守る", ("Functor laws", "Monoid laws", "law testing", "信頼"), hs("""
    module Main where

    main :: IO ()
    main = print (fmap id (Just 10) == (Just 10 :: Maybe Int))
    """), "True"),
    Chapter(22, 7, PARTS[7], "標準的な型クラス", "よく使う型クラスの役割と階層を読む", ("Eq", "Ord", "Show", "Monoid"), hs("""
    module Main where

    main :: IO ()
    main = print (mappend [1,2] [3,4])
    """), "[1,2,3,4]"),
    Chapter(23, 8, PARTS[8], "Functor", "文脈を壊さず中身だけ変換する", ("Functor", "fmap", "<$>", "文脈"), hs("""
    module Main where

    main :: IO ()
    main = print (fmap (+1) (Just 10))
    """), "Just 11"),
    Chapter(24, 8, PARTS[8], "Applicative", "独立した文脈付き計算を組み合わせる", ("Applicative", "pure", "<*>", "独立性"), hs("""
    module Main where

    data User = User String Int deriving Show

    main :: IO ()
    main = print (User <$> Just "Ada" <*> Just 36)
    """), "Just (User \"Ada\" 36)"),
    Chapter(25, 8, PARTS[8], "Monad", "前の結果に応じて次の計算を選ぶ", ("Monad", ">>=", "return", "依存する計算"), hs("""
    module Main where

    findUser :: Int -> Maybe String
    findUser 1 = Just "Ada"
    findUser _ = Nothing

    orders :: String -> Maybe [String]
    orders name = Just [name ++ "-order"]

    main :: IO ()
    main = print (findUser 1 >>= orders)
    """), "Just [\"Ada-order\"]"),
    Chapter(26, 8, PARTS[8], "do記法", "命令に見える構文をモナド合成として読む", ("do", "<-", "IO", "合成"), hs("""
    module Main where

    main :: IO ()
    main = do
      let name = "Ada"
      putStrLn ("Hello, " ++ name)
    """), "Hello, Ada"),
]


EXTRA_TITLES = [
    (27, 9, "副作用とは何か", "外界との相互作用を型で境界に出す", ("副作用", "IO", "外界", "純粋な計算")),
    (28, 9, "Pure Core / Effectful Shell", "純粋な中心と副作用の薄い外側に分ける", ("Pure Core", "Effectful Shell", "依存注入", "テスト容易性")),
    (29, 9, "Reader / State / Writer", "環境・状態・ログを計算の文脈として扱う", ("Reader", "State", "Writer", "環境")),
    (30, 9, "モナド変換子", "複数の文脈を重ねる設計を学ぶ", ("MaybeT", "ExceptT", "ReaderT", "mtl")),
    (31, 10, "partial function を避ける", "実行時に壊れる関数を型で置き換える", ("head", "fromJust", "undefined", "bottom")),
    (32, 10, "エラーを型で設計する", "エラーを文字列ではなくドメイン型にする", ("DomainError", "Either", "ExceptT", "ValidationError")),
    (33, 11, "モジュールシステム", "公開境界で不変条件を守る", ("module", "import", "export list", "抽象データ型")),
    (34, 11, "Cabal / Stack / Hackage", "Haskellプロジェクトと依存関係を管理する", ("Cabal", "Stack", "Hackage", "依存関係")),
    (35, 11, "Haskell Language Server", "型を見ながら開発する環境を作る", ("HLS", "LSP", "診断", "補完")),
    (36, 12, "例ベースのテスト", "具体例で仕様の基礎を固定する", ("Hspec", "tasty", "unit test", "doctest")),
    (37, 12, "プロパティベーステスト", "性質をランダム生成で検査する", ("QuickCheck", "property", "Arbitrary", "law testing")),
    (38, 13, "パーサーコンビネータ", "小さなパーサーを合成して言語を読む", ("Parser", "parsec", "megaparsec", "Alternative")),
    (39, 13, "DSL設計", "小さな言語を型と関数で設計する", ("Embedded DSL", "Free Monad", "Tagless Final", "Interpreter")),
    (40, 14, "Lensとは何か", "不変データの一部を合成可能に扱う", ("Lens", "Prism", "Traversal", "Optics")),
    (41, 15, "軽量スレッドと async", "並行処理を構造化して扱う", ("forkIO", "async", "wait", "concurrently")),
    (42, 15, "STM", "共有状態をトランザクションとして扱う", ("STM", "TVar", "atomically", "retry")),
    (43, 16, "GHCの基礎", "Haskellがどうコンパイル・実行されるかを見る", ("GHC", "GHCi", "RTS", "Core")),
    (44, 16, "プロファイリング", "性能問題を推測ではなく測定する", ("time profiling", "heap profiling", "cost centre", "eventlog")),
    (45, 16, "正格性制御", "必要な場所で評価を強制する", ("seq", "deepseq", "BangPatterns", "StrictData")),
    (46, 17, "kind と高階型", "型の型を読み、高カインド型を理解する", ("kind", "Type", "* -> *", "高カインド型")),
    (47, 17, "GADT", "型安全なASTをデータ構造に埋め込む", ("GADTs", "型安全AST", "式", "制約")),
    (48, 17, "Phantom Types", "値にない状態や権限を型に持たせる", ("Phantom type", "状態", "権限", "検証済み")),
    (49, 17, "DataKinds / TypeFamilies / Type-level programming", "型レベル計算の使いどころを判断する", ("DataKinds", "TypeFamilies", "TypeLits", "型レベル")),
    (50, 17, "RankNTypes / Existential Types", "高度な多相性で抽象境界を作る", ("RankNTypes", "forall", "existential", "抽象化")),
    (51, 17, "Deriving と Generics", "導出を便利さだけでなく意味として扱う", ("deriving", "Generic", "DerivingVia", "aeson")),
    (52, 18, "CLIアプリを作る", "純粋ロジックを持つCLIを作る", ("optparse-applicative", "text", "file IO", "logging")),
    (53, 18, "Web APIを作る", "ルート、入出力、エラーを型で表す", ("servant", "wai", "warp", "aeson")),
    (54, 18, "DBを扱う", "DB境界とドメイン境界を分ける", ("persistent", "beam", "transaction", "connection pool")),
    (55, 18, "JSONと外部API", "外部表現と内部モデルを分離する", ("aeson", "FromJSON", "ToJSON", "newtype wrapper")),
    (56, 19, "FFI", "外部言語との境界を安全に扱う", ("FFI", "C連携", "marshal", "境界")),
    (57, 19, "JavaScript / WebAssembly backend", "HaskellをWeb実行環境へ接続する選択肢を知る", ("JavaScript backend", "WebAssembly backend", "PureScript", "frontend")),
    (58, 19, "Nixと再現可能ビルド", "環境差分を減らすビルド設計を知る", ("Nix", "haskell.nix", "CI", "再現可能")),
    (59, 20, "PureScript", "Haskell的設計をJavaScript圏で使う選択肢を比較する", ("PureScript", "正格評価", "型クラス", "JavaScript")),
    (60, 20, "Elm", "Web UI向けに単純化された純粋関数型を比較する", ("Elm", "TEA", "副作用分離", "Web UI")),
    (61, 20, "Clean", "Haskellに近い遅延純粋言語を比較する", ("Clean", "一意型", "遅延評価", "純粋")),
    (62, 20, "OCaml / F# / Scala", "ML系・実務関数型との違いを見る", ("OCaml", "F#", "Scala", "正格評価")),
    (63, 20, "Idris / Agda / Lean / F*", "依存型と証明の世界との境界を知る", ("依存型", "証明", "全域性", "型駆動")),
    (64, 20, "Roc / Unison / Gleam", "新しい関数型言語の設計意図を比較する", ("Roc", "Unison", "Gleam", "BEAM")),
    (65, 20, "TypeScript + Effect / fp-ts", "Haskell的発想をTypeScriptで使う限界を知る", ("Effect", "fp-ts", "Option", "Task")),
    (66, 21, "なぜHaskellは生まれたのか", "歴史から設計判断の理由を読む", ("Haskell 98", "Haskell 2010", "GHC", "研究")),
    (67, 21, "Haskellの哲学", "型・純粋性・合成・法則を判断軸にする", ("純粋性", "型で設計", "法則", "抽象")),
    (68, 22, "小規模演習", "安全な小さなライブラリやCLIを完成させる", ("safe list", "CLI", "Either", "テスト")),
    (69, 22, "中規模演習", "ドメイン型とエラー設計を持つアプリを作る", ("API", "Parser", "ReaderT", "QuickCheck")),
    (70, 22, "大規模演習", "型安全なアーキテクチャを設計・実装・説明する", ("DSL", "STM", "benchmark", "package")),
]


for n, part, title, focus, terms in EXTRA_TITLES:
    example, expected = EXAMPLES.get(n, (GENERIC_EXAMPLE, "本文の問いに合わせた出力を観察する"))
    CHAPTERS.append(Chapter(n, part, PARTS[part], title, focus, tuple(terms), example, expected))


def slug(value: str) -> str:
    table = {
        "Haskellとは何か": "what_is_haskell",
        "Hello, World! の本当の意味": "hello_world",
        "GHCiで「型を見る」習慣を作る": "ghci_types",
        "変数ではなく「束縛」": "bindings",
        "参照透過性": "referential_transparency",
        "関数とは何か": "functions",
        "高階関数": "higher_order_functions",
        "関数合成とポイントフリースタイル": "composition",
        "型注釈と型推論": "types",
        "多相性": "polymorphism",
    }
    if value in table:
        return table[value]
    s = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").lower()
    return s or "chapter"


def chapter_dir(ch: Chapter) -> Path:
    return ROOT / "chapters" / f"part_{ch.part:02d}_{slug(ch.part_title)}" / f"chapter_{ch.number:02d}_{slug(ch.title)}"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def term_lines(terms: tuple[str, ...]) -> str:
    return "\n".join(f"- `{t}`: この章で設計判断に使う中心語です。" for t in terms)


def official_link(ch: Chapter) -> str:
    if ch.number in {1, 2, 34, 35, 43}:
        return "- Haskell Downloads: https://www.haskell.org/downloads/\n- GHC User's Guide: https://ghc.gitlab.haskell.org/ghc/doc/users_guide/"
    if ch.number in {36, 37}:
        return "- QuickCheck: https://hackage.haskell.org/package/QuickCheck\n- Cabal: https://www.haskell.org/cabal/"
    if ch.number in {56, 57}:
        return "- Haskell 2010 Report: https://www.haskell.org/definition/haskell2010.pdf\n- GHC User's Guide: https://ghc.gitlab.haskell.org/ghc/doc/users_guide/"
    return "- Haskell 2010 Report: https://www.haskell.org/definition/haskell2010.pdf\n- GHC User's Guide: https://ghc.gitlab.haskell.org/ghc/doc/users_guide/"


def readme(ch: Chapter) -> str:
    example_file = "examples/Main.hs"
    return f"""
# 第{ch.number}章: {ch.title}

## この章でできるようになること

この章の目的は、**{ch.focus}** ことです。Haskellでは構文を覚えるだけでは足りません。値、型、副作用、合成、法則のどれを今扱っているのかを意識すると、短いコードでも設計の意図が読めるようになります。

## まず知るべき言葉

{term_lines(ch.terms)}

## なぜこれを学ぶのか

初心者はHaskellを「PythonやJavaScriptの別構文」として読もうとしてつまずきます。しかしHaskellでは、代入、例外、暗黙の副作用、null、可変状態を中心に考えると、言語の長所が見えません。

この章では、目の前のコードを「何を実行するか」ではなく「どんな値を作り、どんな型で制約し、どんな計算として合成するか」という観点で読みます。プロフェッショナルなHaskellコードは、実装の細部よりも型と境界が先に設計されています。

## 手順 1: 例を読む

`{example_file}` を作って、次のコードを置きます。

```haskell
{ch.example}
```

## 手順 2: 実行する

GHCupでGHCを入れている場合は、章ディレクトリで次を実行します。

```bash
runghc examples/Main.hs
```

この環境にGHCがない場合は、コードを目で追い、型注釈、純粋関数、`main :: IO ()` の境界を確認してください。

## 手順 3: 出力を観察する

期待する観察結果:

```text
{ch.expected}
```

出力だけでなく、どの部分が純粋な計算で、どの部分が外界に触れる計算なのかを分けて見ます。`main` の外へ純粋な関数を切り出せるほど、テストしやすく、型で読みやすいコードになります。

## 設計として考える

この章の中心は `{ch.terms[0]}` です。Haskellでは、便利だからそう書くのではなく、意味を狭めるために型や抽象を使います。意味を狭めると、呼び出し側が間違えにくくなり、コンパイラが設計の一部を検査できます。

次の問いに答えてください。

- この例で、型が説明している仕様は何か。
- 実行時に失敗しそうな場所はどこか。
- その失敗を型に出すなら、`Maybe`、`Either`、独自エラー型のどれが自然か。
- この章の考え方を使うと、命令型言語で書いていた処理をどう分解できるか。

## よくあるつまずき

```text
Q. Haskellのコードは短いのに、なぜ説明が長いのですか？
A. 短い構文の背後に、型、評価、副作用の境界があるからです。最初は説明を厚く読み、慣れたら型だけで意図を読む練習をします。

Q. 実行できない環境では学べませんか？
A. 実行は重要ですが、Haskellでは型を読む練習も同じくらい重要です。まずコードを読み、環境構築後に同じ例を実行してください。
```

## 次の章に進む条件

```text
1. この章の中心語を自分の言葉で説明できる。
2. サンプルの型注釈を見て、入力と出力を説明できる。
3. 純粋な部分とIOの境界を指摘できる。
```

## 公式 docs で確認する箇所

{official_link(ch)}
"""


def exercises(ch: Chapter) -> str:
    return f"""
# 第{ch.number}章 Exercises: {ch.title}

## 1. 小さく変更する

`examples/Main.hs` の値、関数名、入力データのどれかを一つだけ変更してください。変更後、出力がどう変わるかを実行前に予想します。

## 2. 出力を比較する

元の出力と変更後の出力を比較し、どの式が結果に影響したかを書きます。出力が変わらなかった場合は、なぜ変わらないのかを型または評価順序から説明します。

## 3. 設計判断を書く

この章のテーマである「{ch.focus}」を、次の形式で短く説明してください。

```text
この設計は ______ を防ぐために使う。
代わりに ______ と書くと、______ という問題が起きやすい。
実務では ______ の境界に注意する。
```

## 提出物

```text
1. 変更したコード
2. 実行結果または期待結果
3. 型から読み取れる仕様
4. この章の設計判断
```

## 進級チェック

```text
□ {ch.terms[0]} を自分の言葉で説明できる
□ サンプルの型注釈を読める
□ 純粋関数とIOアクションを区別できる
□ 次の章で何を深めるのか説明できる
```
"""


def sample(ch: Chapter) -> str:
    return ch.example + "\n"


def root_readme() -> str:
    rows = "\n".join(
        f"| 第{p}部 | {title} | {sum(1 for c in CHAPTERS if c.part == p)}章 |"
        for p, title in PARTS.items()
    )
    return f"""
# Haskell 完全チュートリアル

このリポジトリは、`TUTORIAL.md` の構想を元にした日本語のHaskellチュートリアルです。Hello, World! から始めて、型設計、副作用の分離、Functor / Applicative / Monad、テスト、実務アプリケーション、GHC、並行処理、高度な型、総合演習まで進みます。

最初に読むファイルは [START_HERE.md](START_HERE.md) です。

## 学習方針

この教材は、APIや構文の暗記ではなく、**型で世界を設計し、純粋関数で意味を記述し、副作用を型で隔離し、小さな計算を合成して大きなプログラムを作る** 力を育てます。

## 構成

| 部 | テーマ | 章数 |
| --- | --- | --- |
{rows}

## 最初のコマンド

```bash
ghcup tui
cabal update
cabal build all
runghc chapters/part_01_hello_world/chapter_01_hello_world/examples/Main.hs
```

この作業環境ではGHC/Cabalが未導入だったため、コード例の実コンパイルは未実施です。教材内の手順はGHCupでGHCとcabal-installを入れた環境を前提にしています。
"""


def start_here() -> str:
    return """
# START HERE

## 今日やること

1. Haskellの環境を作る。
2. 第0章で思想を読む。
3. 第1章の `Hello, World!` を実行する。
4. 第2章でGHCiの `:t` を使い、型を見る習慣を作る。

## 環境構築

公式にはGHCupを使う方法が推奨されています。

```bash
curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh
ghcup tui
ghc --version
cabal --version
```

VS Code、Neovim、Emacsなどを使う場合は Haskell Language Server も入れてください。

## 各章の使い方

```text
README.md を読む
examples/Main.hs を読む
runghc examples/Main.hs で動かす
exercises.md を解く
進級チェックに答える
公式docsを確認する
```

## 学習時間の目安

```text
第0部から第5部: 1日30-60分で2-3週間
第6部から第12部: 1日60分で3-5週間
第13部から第18部: 小さなアプリを作りながら4-8週間
第19部から第22部: 必要な章を選び、総合演習で確認
```

## つまずいたとき

- 型エラーは敵ではなく、設計のフィードバックです。
- `IO` が出てきたら、副作用の境界を探してください。
- `Maybe` や `Either` が出てきたら、失敗可能性が型に出ていると考えてください。
- 分からない抽象は、まず具体型 `Maybe`、`[]`、`Either String` で試してください。
"""


def glossary() -> str:
    terms = {
        "純粋関数": "同じ入力に対して同じ出力を返し、外界を勝手に変えない関数。",
        "参照透過性": "式をその値で置き換えてもプログラムの意味が変わらない性質。",
        "IO": "外界とやり取りする計算を表す型。命令ではなく値として扱う。",
        "型推論": "明示しない型をコンパイラが推測する仕組み。",
        "代数的データ型": "直和と直積でドメインの形を表すデータ型。",
        "パターンマッチ": "データ型の形に従って値を分解する方法。",
        "Maybe": "値があるかもしれないし、ないかもしれないことを表す型。",
        "Either": "成功か失敗理由のどちらかを表す型。",
        "型クラス": "複数の型に共通する操作を表す仕組み。",
        "Functor": "文脈の中の値へ関数を適用できる抽象。",
        "Applicative": "独立した文脈付き値を組み合わせる抽象。",
        "Monad": "前の結果に応じて次の計算を選ぶ抽象。",
        "遅延評価": "値が必要になるまで評価しない評価戦略。",
        "正格性": "値をどこまで先に評価するかに関する性質。",
        "newtype": "実行時コストを増やさず、意味の違う型を作る構文。",
        "bottom": "実行時エラーや非停止など、正常な値を返さない計算。",
        "ReaderT": "環境を読む計算を他の文脈と組み合わせるための道具。",
        "GADT": "コンストラクタごとにより細かい戻り型を書けるデータ型。",
    }
    body = "\n\n".join(f"## {k}\n\n{v}" for k, v in terms.items())
    return "# Glossary\n\n" + body


def cabal_file() -> str:
    return """
cabal-version: 3.8
name: haskell-complete-tutorial
version: 0.1.0.0
build-type: Simple

common warnings
  ghc-options: -Wall
  default-language: GHC2024

library
  import: warnings
  exposed-modules: Tutorial.Core
  hs-source-dirs: src
  build-depends: base >=4.18 && <5

test-suite tutorial-tests
  import: warnings
  type: exitcode-stdio-1.0
  main-is: Main.hs
  hs-source-dirs: test
  build-depends: base >=4.18 && <5, haskell-complete-tutorial
"""


def tutorial_index() -> str:
    by_part = []
    for p, title in PARTS.items():
        lines = [f"## 第{p}部: {title}"]
        for ch in [c for c in CHAPTERS if c.part == p]:
            rel = chapter_dir(ch).relative_to(ROOT)
            lines.append(f"- 第{ch.number}章: [{ch.title}]({rel}/README.md) - {ch.focus}")
        by_part.append("\n".join(lines))
    return """
# Haskell 完全チュートリアル設計

このファイルは教材全体の索引です。本文は `chapters/` 以下に章ごとに分かれています。

## 核となる一文

Haskellは、型で世界を設計し、純粋関数で意味を記述し、副作用を型で隔離し、小さな計算を合成して大きなプログラムを作る言語です。

## 章一覧

""" + "\n\n".join(by_part)


def main() -> None:
    write(ROOT / ".gitignore", "\n".join(["dist-newstyle/", ".stack-work/", ".hie/", "*.hi", "*.o", ".DS_Store", "tmp/", "result"]) + "\n")
    write(ROOT / "README.md", root_readme())
    write(ROOT / "START_HERE.md", start_here())
    write(ROOT / "glossary.md", glossary())
    write(ROOT / "TUTORIAL.md", tutorial_index())
    write(ROOT / "cabal.project", "packages: .\n")
    write(ROOT / "haskell-complete-tutorial.cabal", cabal_file())
    write(ROOT / "src" / "Tutorial" / "Core.hs", "module Tutorial.Core where\n\ncoreIdea :: String\ncoreIdea = \"型で設計し、純粋関数で意味を書き、副作用を境界へ置く\"\n")
    old_placeholder = ROOT / "src" / "Tutorial" / "Placeholder.hs"
    if old_placeholder.exists():
        old_placeholder.unlink()
    write(ROOT / "test" / "Main.hs", "module Main where\n\nimport Tutorial.Core (coreIdea)\n\nmain :: IO ()\nmain = putStrLn coreIdea\n")
    for ch in CHAPTERS:
        base = chapter_dir(ch)
        write(base / "README.md", readme(ch))
        write(base / "exercises.md", exercises(ch))
        write(base / "examples" / "Main.hs", sample(ch))
    print(f"generated {len(CHAPTERS)} chapters")


if __name__ == "__main__":
    main()
