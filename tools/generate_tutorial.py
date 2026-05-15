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
        "Haskellを学ぶ前に": "foundations",
        "Hello, World! から始める": "hello_world",
        "値・式・関数": "values_expressions_functions",
        "型で考える": "thinking_with_types",
        "代数的データ型とパターンマッチ": "adt_pattern_matching",
        "再帰・リスト・fold": "recursion_lists_fold",
        "遅延評価と非正格意味論": "lazy_evaluation",
        "型クラス": "typeclasses",
        "Functor / Applicative / Monad": "functor_applicative_monad",
        "Effect と IO の設計": "effects_io_design",
        "エラー設計": "error_design",
        "モジュール・プロジェクト・ツール": "modules_projects_tools",
        "テストと仕様": "testing_specification",
        "パーサー・DSL・関数型設計": "parsers_dsl_design",
        "Lens とデータアクセス": "lens_data_access",
        "並行・並列・STM": "concurrency_parallelism_stm",
        "性能・最適化・GHC": "performance_ghc",
        "高度な型システム": "advanced_types",
        "実務アプリケーション設計": "application_design",
        "FFI・JS・WASM・Nix": "ffi_js_wasm_nix",
        "Haskell周辺言語との比較": "language_comparisons",
        "Haskellの歴史と哲学": "history_philosophy",
        "プロフェッショナルへの総合演習": "professional_projects",
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
        "型エイリアスと newtype": "newtype",
        "代数的データ型": "algebraic_data_types",
        "パターンマッチ": "pattern_matching",
        "Maybe": "maybe",
        "Either": "either",
        "ループではなく再帰": "recursion",
        "map / filter / fold": "map_filter_fold",
        "リスト内包表記": "list_comprehension",
        "遅延評価とは何か": "lazy_evaluation",
        "遅延評価は万能ではない": "strictness",
        "型クラスとは何か": "typeclasses",
        "型クラスの法則": "typeclass_laws",
        "標準的な型クラス": "standard_typeclasses",
        "Functor": "functor",
        "Applicative": "applicative",
        "Monad": "monad",
        "do記法": "do_notation",
        "副作用とは何か": "effects",
        "Pure Core / Effectful Shell": "pure_core_effectful_shell",
        "Reader / State / Writer": "reader_state_writer",
        "モナド変換子": "monad_transformers",
        "partial function を避ける": "partial_functions",
        "エラーを型で設計する": "typed_errors",
        "モジュールシステム": "module_system",
        "Cabal / Stack / Hackage": "cabal_stack_hackage",
        "Haskell Language Server": "haskell_language_server",
        "例ベースのテスト": "example_based_tests",
        "プロパティベーステスト": "property_based_tests",
        "パーサーコンビネータ": "parser_combinators",
        "DSL設計": "dsl_design",
        "Lensとは何か": "lens",
        "軽量スレッドと async": "async",
        "STM": "stm",
        "GHCの基礎": "ghc_basics",
        "プロファイリング": "profiling",
        "正格性制御": "strictness_control",
        "kind と高階型": "kinds_higher_kinded_types",
        "GADT": "gadt",
        "Phantom Types": "phantom_types",
        "DataKinds / TypeFamilies / Type-level programming": "type_level_programming",
        "RankNTypes / Existential Types": "rankn_existentials",
        "Deriving と Generics": "deriving_generics",
        "CLIアプリを作る": "cli_app",
        "Web APIを作る": "web_api",
        "DBを扱う": "database",
        "JSONと外部API": "json_external_api",
        "FFI": "ffi",
        "JavaScript / WebAssembly backend": "javascript_webassembly",
        "Nixと再現可能ビルド": "nix_reproducible_builds",
        "PureScript": "purescript",
        "Elm": "elm",
        "Clean": "clean",
        "OCaml / F# / Scala": "ocaml_fsharp_scala",
        "Idris / Agda / Lean / F*": "idris_agda_lean_fstar",
        "Roc / Unison / Gleam": "roc_unison_gleam",
        "TypeScript + Effect / fp-ts": "typescript_effect_fpts",
        "なぜHaskellは生まれたのか": "history_of_haskell",
        "Haskellの哲学": "haskell_philosophy",
        "小規模演習": "small_project",
        "中規模演習": "medium_project",
        "大規模演習": "large_project",
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


TERM_EXPLANATIONS = {
    "純粋関数型": "副作用を隠さず、同じ入力から同じ出力を得る計算を中心に設計する考え方。",
    "参照透過性": "式をその結果で置き換えても意味が変わらない性質。テスト、最適化、並行化の土台になる。",
    "遅延評価": "値が必要になるまで評価しない評価戦略。無限リストや制御構造の表現力につながる。",
    "型で設計する": "コメントや慣習ではなく、型で不正な状態や失敗可能性を表す設計態度。",
    "main": "プログラムの入口。Haskellでは `IO ()` というアクションとして表す。",
    "IO": "外界とやり取りする計算を表す型。純粋な値と副作用を混ぜないための境界。",
    "GHCi": "Haskellの対話環境。式を試し、型を読み、コンパイル前に理解を固める場所。",
    ":t": "GHCiで式の型を見るコマンド。Haskell学習で最初に身につけるべき読み方。",
    "type": "既存の型に別名を付ける構文。意味の区別ではなく読みやすさを助ける。",
    "newtype": "実行時コストを増やさず、意味の違う値を別の型として扱う構文。",
    "Maybe": "値があるかもしれないし、ないかもしれないことを表す型。",
    "Either": "成功値か失敗理由のどちらかを表す型。例外を隠さず設計に出す。",
    "Functor": "文脈を壊さず、中身だけを変換できる抽象。",
    "Applicative": "互いに依存しない文脈付き計算を合成する抽象。",
    "Monad": "前の計算結果に応じて次の計算を選ぶための抽象。",
    "Pure Core": "ビジネスルールや変換を純粋関数として置く中心部分。",
    "Effectful Shell": "ファイル、DB、HTTP、ログなど外界とのやり取りを引き受ける薄い外側。",
    "servant": "Web APIのルート、入出力、エラーを型として表すHaskellライブラリ。",
    "DSL": "特定領域の問題を表す小さな言語。HaskellではADTやGADTで設計しやすい。",
}


TERM_FALLBACKS = {
    0: "Haskellを手順ではなく意味の体系として読むための基礎語です。",
    1: "最初の実行結果を型と副作用の境界から読むための語です。",
    2: "状態更新ではなく式の変換としてコードを組み立てるための語です。",
    3: "値の意味を型で狭め、誤用をコンパイル時に見つけるための語です。",
    4: "データの形と分岐を型として表し、不正な状態を減らすための語です。",
    5: "リストや再帰構造に沿って計算を組み立てるための語です。",
    6: "いつ評価されるかを読み、表現力とメモリ使用量の交換条件を見るための語です。",
    7: "共通操作を法則付きの抽象として扱うための語です。",
    8: "文脈付き計算をどの程度の依存関係で合成するか判断するための語です。",
    9: "純粋な中心と副作用の境界を設計するための語です。",
    10: "失敗を実行時例外ではなく型と戻り値で表すための語です。",
    11: "コードを保守可能なプロジェクトとして分割・公開・ビルドするための語です。",
    12: "型だけでは表せない仕様を実行可能な検査として残すための語です。",
    13: "小さな部品を合成して入力言語やドメイン語彙を作るための語です。",
    14: "不変データの一部に安全かつ合成可能にアクセスするための語です。",
    15: "並行実行で共有状態や失敗の境界を明示するための語です。",
    16: "GHCと実行時の振る舞いを測定しながら改善するための語です。",
    17: "通常の型より強い制約を表す価値があるか判断するための語です。",
    18: "外部表現と内部ドメインを分けて実務アプリを設計するための語です。",
    19: "Haskell外の環境と接続するときの安全性と再現性を考えるための語です。",
    20: "他言語との違いからHaskellの設計判断を相対化するための語です。",
    21: "Haskellの設計がなぜ今の形になったかを説明するための語です。",
    22: "型、効果、性能、運用をまとめて設計するための語です。",
}


WHY_BY_PART = {
    0: "Haskellを学ぶ最初の壁は構文ではなく、プログラムを手順ではなく意味として読むことです。この部では、値、型、副作用、合成、法則という軸を先に置きます。",
    1: "`Hello, World!` は単なる出力ではありません。`main :: IO ()` を理解すると、Haskellが副作用をどう型に出すかが見えます。",
    2: "Haskellでは代入で状態を動かすより、式と関数を合成して意味を作ります。この部では、命令列ではなく変換としてプログラムを見る練習をします。",
    3: "型はコンパイラのためだけの注釈ではなく、設計の最短の説明です。意味の違う値を分け、使えない操作を型で防ぎます。",
    4: "ADTとパターンマッチは、不正な状態を作れない設計の中心です。分岐を文字列やフラグで隠さず、型そのものに表します。",
    5: "ループを状態更新として見るのではなく、データ構造の形に沿った再帰や畳み込みとして見ると、処理の意味が明確になります。",
    6: "遅延評価はHaskellの表現力を支えますが、性能問題の原因にもなります。信頼しつつ観察する姿勢が必要です。",
    7: "型クラスは便利なインターフェースではなく、法則を伴う抽象です。型が合うことと、期待される振る舞いを守ることを分けて考えます。",
    8: "Functor、Applicative、Monadは、文脈付き計算を合成するための段階です。比喩ではなく、どの依存関係を表しているかで選びます。",
    9: "実務Haskellでは、純粋な中心を厚くし、副作用の外側を薄く保ちます。これはテスト容易性と変更容易性に直結します。",
    10: "Haskellでも実行時エラーは起こせます。partial functionを避け、失敗を型で表すことでレビュー可能なエラー設計にします。",
    11: "モジュール、Cabal、HLSはコードを学習用断片から保守可能なプロジェクトへ変えるための基盤です。",
    12: "型は構造を守りますが、仕様までは自動で保証しません。例ベースと性質ベースのテストで振る舞いを固定します。",
    13: "パーサーやDSLは、小さな部品を合成して大きな意味を作るHaskellらしさがよく現れる領域です。",
    14: "不変データを扱うと、ネストした値の更新が課題になります。Lensはその操作を合成可能にします。",
    15: "純粋な計算と副作用の境界が明確だと、並行処理でも共有状態の危険を局所化できます。",
    16: "Haskellの性能は直感と違う場所で決まることがあります。GHC、RTS、プロファイルを使って測定で判断します。",
    17: "高度な型は制約をより強く表せますが、濫用すると読みにくくなります。型で守る価値がある境界を見極めます。",
    18: "CLI、Web API、DB、JSONでは外部世界と内部ドメインを分ける判断が重要です。型はその境界線を明確にします。",
    19: "FFI、JS/WASM、NixはHaskellを外部環境へ接続します。安全な境界と再現性を意識して扱います。",
    20: "周辺言語と比較すると、Haskellの純粋性、遅延評価、型クラスの特徴が相対的に見えるようになります。",
    21: "Haskellの設計は偶然ではありません。歴史と哲学を知ると、なぜこの言語が今の形なのか判断しやすくなります。",
    22: "最後は個別知識を統合します。型、法則、純粋性、副作用、性能、ドキュメントを同時に満たす設計を作ります。",
}


PITFALL_BY_PART = {
    0: "初心者はHaskellを既存言語の別構文として読みがちです。最初から「何を変更するか」ではなく「何を意味するか」を読む必要があります。",
    1: "`IO` を命令や魔法の箱として扱うと、純粋関数との境界が曖昧になります。",
    2: "値の再代入やforループを探すと、Haskellのコードが遠回りに見えます。",
    3: "型注釈を面倒な制約として扱うと、型が設計メモになる利点を逃します。",
    4: "状態を文字列フラグやnullableなフィールドで表すと、不正な組み合わせが作れてしまいます。",
    5: "すぐに自前再帰を書くと、標準のmap/filter/foldで表せる単純な意図が隠れます。",
    6: "遅延評価を万能視すると、スペースリークや評価タイミングの誤解につながります。",
    7: "型クラスをOOPの継承として読むと、法則とインスタンス設計の意味を見落とします。",
    8: "Monadを副作用専用の概念として覚えると、Maybe、Either、Parser、Stateの共通性が見えません。",
    9: "`IO` だけで全体を書くと、テスト困難で変更に弱いプログラムになります。",
    10: "`head`、`read`、`fromJust` を便利だから使うと、型で守れる失敗を実行時に押し戻してしまいます。",
    11: "すべてを一つのファイルに置くと、公開境界や依存関係の意図が見えなくなります。",
    12: "型が通ったから正しいと考えると、仕様ミスや境界条件を見逃します。",
    13: "パーサーやDSLを巨大なcase文で書くと、合成可能性が失われます。",
    14: "Lensを早く使いすぎると、まず理解すべきADTとレコード更新の設計が曖昧になります。",
    15: "共有状態をロックだけで考えると、競合条件と例外時の整合性が難しくなります。",
    16: "性能を勘で直すと、遅延評価の実際のコストを外しやすくなります。",
    17: "高度な型を使えば良い設計になるわけではありません。保守性との交換条件があります。",
    18: "外部JSONやDB行をそのままドメイン型にすると、外部制約が内部設計を汚染します。",
    19: "外部環境との境界を雑に扱うと、型安全性や再現性の利点が消えます。",
    20: "似た構文だけを見ると、評価戦略、Effect、型クラスの違いを見落とします。",
    21: "歴史を知らないと、遅延評価や型クラスを単なる癖として扱ってしまいます。",
    22: "抽象、性能、運用、ドキュメントのどれか一つだけを見ると、実務設計としては不十分です。",
}


PHILOSOPHY_BY_PART = {
    0: (
        "Haskellの出発点は、プログラムを「機械に実行させる手順」ではなく「値同士の関係」として書くことです。"
        "この発想はラムダ計算に由来し、計算を名前付きの箱や逐次的な命令ではなく、式の変形として扱います。"
        "そのため、Haskellを学ぶ最初の目的は構文を早く覚えることではなく、コードがどの意味を固定しているのかを読む目を作ることです。\n\n"
        "純粋性、型、遅延評価、型クラス、モナドは別々の便利機能ではありません。"
        "それらは、プログラムの意味を局所的に理解し、誤用を早く発見し、部品を安全に合成するために互いに支え合っています。"
        "この部で先に思想を置くのは、あとで出てくる構文を単なる記号として暗記しないためです。"
    ),
    1: (
        "Hello, World! は普通の言語では「画面に文字を出す命令」として扱われます。"
        "Haskellではここからすでに違います。`main` は命令の列ではなく、`IO ()` という型を持つ値です。"
        "これは、外界に触る計算を純粋な式から分離するというHaskellの哲学を、最初の一行から見せています。\n\n"
        "`IO` は副作用を禁止するための仕組みではありません。副作用を型として見える場所に置くための仕組みです。"
        "この違いを早く理解すると、Haskellが実務で扱いにくい言語ではなく、外界との接点をレビューしやすくする言語だと分かります。"
    ),
    2: (
        "Haskellの値、式、関数は、状態を少しずつ変えるための部品ではなく、意味を組み立てるための部品です。"
        "同じ名前に別の値を再代入しないのは、不便にするためではありません。"
        "ある式が常に同じ意味を持つことで、読者もコンパイラも安心して置き換え、合成、最適化できるからです。\n\n"
        "この考え方に慣れると、プログラムは時間順の命令列ではなく、入力から出力への変換の集まりとして見えます。"
        "Haskellらしい短いコードは、単に記号を省略しているのではなく、変換の境界が明確だから短く読めるのです。"
    ),
    3: (
        "Haskellの型は、コンパイラを満足させるための飾りではありません。"
        "型は設計上の判断を最も短く、最も機械的に検査できる形で残す方法です。"
        "同じ `String` でも、メールアドレス、ユーザー名、ファイルパス、外部APIのトークンは意味が違います。"
        "その違いを型にしないなら、違いはコメント、命名、運用上の注意に逃げてしまいます。\n\n"
        "型で設計するとは、実装前に完璧な型を作ることではありません。"
        "間違えたくない境界、混ぜたくない値、必ず処理したい失敗を型に押し出し、プログラムの読み方を狭めることです。"
    ),
    4: (
        "代数的データ型は、ドメインに存在する状態をそのままコードへ写すための道具です。"
        "多くのバグは、実際には存在しない状態をプログラムが表現できてしまうことから生まれます。"
        "ADTは、可能な形だけをコンストラクタとして並べ、不可能な組み合わせをそもそも作れなくします。\n\n"
        "パターンマッチは、作った型の構造に責任を持って向き合う仕組みです。"
        "分岐が増えて面倒に見える場面でも、網羅性チェックによって「この状態を考え忘れている」という設計ミスを早く発見できます。"
    ),
    5: (
        "Haskellで再帰やfoldを学ぶ理由は、ループ構文の代替を覚えるためではありません。"
        "データ構造には形があり、計算もその形に沿って書ける、という見方を身につけるためです。"
        "リストなら空リストと先頭要素、木なら葉と枝、という形に沿って処理を書くと、分岐と停止条件が自然に現れます。\n\n"
        "`map`、`filter`、`fold` は、よく使う関数名の暗記項目ではなく、処理の意図に名前を与える語彙です。"
        "変換なのか、選別なのか、集約なのかを先に決めることで、コードの読み方が安定します。"
    ),
    6: (
        "遅延評価は、Haskellを他の多くの実務言語と大きく分ける特徴です。"
        "値は必要になるまで評価されないため、無限リスト、制御構造の抽象化、大きなデータの一部だけの利用が自然に書けます。"
        "これは単なる最適化ではなく、計算を「いつ実行するか」から少し切り離して「何であるか」として扱う設計です。\n\n"
        "一方で、遅延評価は魔法ではありません。必要な値を先延ばしにするということは、未評価の計算を保持する可能性があるということでもあります。"
        "Haskellを実務で使うには、遅延を表現力として使う場面と、正格性で評価を制御する場面を分けて判断する必要があります。"
    ),
    7: (
        "型クラスは、型ごとの共通操作を定義する仕組みですが、それだけなら単なるインターフェースです。"
        "Haskellで重要なのは、型クラスがしばしば法則と一緒に使われることです。"
        "`Eq` なら等価性らしく振る舞うこと、`Monoid` なら単位元と結合性を守ることが期待されます。\n\n"
        "つまり型クラスは、呼び出し側が実装の詳細を知らなくても安全に推論できる約束です。"
        "型が合うだけでなく、その抽象に期待される意味を守るからこそ、汎用的な関数が信頼して使えます。"
    ),
    8: (
        "Functor、Applicative、Monadは、難解な比喩で覚えるものではありません。"
        "これらはすべて、文脈付きの値や計算をどう合成するかを段階的に表す設計語彙です。"
        "中身だけを変えるならFunctor、独立した文脈を組み合わせるならApplicative、前の結果で次を選ぶならMonadです。\n\n"
        "この区別は実務でも効きます。Monadだけで何でも書くと依存関係が強く見えます。"
        "Applicativeで足りる設計は、処理が独立していることを型と構造で示せます。"
        "抽象を選ぶことは、処理同士の関係を説明することです。"
    ),
    9: (
        "Haskellの副作用設計は、「副作用を避ける」という単純な道徳ではありません。"
        "ファイル、DB、HTTP、ログ、現在時刻は実務アプリに必要です。"
        "重要なのは、それらをビジネスルールの中心に混ぜ込まず、境界に集めることです。\n\n"
        "Pure Core / Effectful Shellはそのための実践的な形です。"
        "中心の純粋関数はテストしやすく、外側の `IO` は入出力と接続だけに集中できます。"
        "この分離は、変更容易性、障害調査、レビューのしやすさに直接つながります。"
    ),
    10: (
        "Haskellにも実行時エラーはあります。だからこそ、失敗を型に出す設計が重要です。"
        "`head`、`read`、`fromJust` のような関数は便利ですが、失敗可能性を型から隠します。"
        "隠された失敗は、テストや本番運用で初めて見つかる問題になります。\n\n"
        "失敗を `Maybe` や `Either`、独自のエラー型で表すと、呼び出し側は成功と失敗の両方を扱う必要があります。"
        "これは面倒を増やしているのではなく、設計上の責任をコンパイラに見える場所へ移しています。"
    ),
    11: (
        "モジュールやCabalは、プロジェクトを整理するためだけの道具ではありません。"
        "Haskellではモジュールの公開リストによって、どのコンストラクタや関数を外へ見せるかを制御できます。"
        "これは不変条件を守るための設計境界です。\n\n"
        "小さな例では一つのファイルで十分ですが、実務では依存関係、公開API、ビルド単位、開発環境が品質に影響します。"
        "Haskell Language ServerやCabalを使うのは便利だからだけでなく、型を読みながら設計を継続的に確認するためです。"
    ),
    12: (
        "型は強力ですが、すべての仕様を型だけで表すわけではありません。"
        "例えば、ソート結果が昇順であること、正規化が冪等であること、パーサーが往復変換を満たすことは、型だけでは十分に表せない場合があります。"
        "そこでテストは、型が表さない振る舞いを実行可能な仕様として残す役割を持ちます。\n\n"
        "例ベースのテストは具体的な期待を固定し、プロパティベーステストは広い入力空間で性質を確認します。"
        "Haskellのテストは、型と競合するものではなく、型設計の外側を補強するものです。"
    ),
    13: (
        "パーサーやDSLは、Haskellの合成的な設計思想がよく現れる領域です。"
        "大きな入力処理を一つの巨大な関数で書く代わりに、小さなパーサーや構文要素を作り、それらを合成して大きな意味を表します。"
        "この方法では、各部品の責任が明確になり、失敗位置や文法上の制約も扱いやすくなります。\n\n"
        "DSL設計は、ドメインの言葉をそのまま型と関数に写す試みです。"
        "うまく設計されたDSLは、利用者にできることとできないことを自然に示し、誤った組み合わせを減らします。"
    ),
    14: (
        "不変データは安全ですが、深くネストした構造の一部を更新するときに冗長になりがちです。"
        "LensやOpticsは、その一部へのアクセスや更新を合成可能な値として扱うための考え方です。"
        "ただし、これは最初に覚えるべき魔法の道具ではありません。\n\n"
        "まずADTとレコード更新でデータの形を理解し、その上で繰り返し現れるアクセスパターンに名前を付けると、Lensの価値が見えます。"
        "Lensの目的は記法を短くすることではなく、データアクセスの意図を再利用可能にすることです。"
    ),
    15: (
        "並行・並列処理では、純粋性の価値がさらに大きくなります。"
        "純粋な計算は共有状態を勝手に変更しないため、並列に実行しても意味が変わりにくくなります。"
        "危険が集中するのは、外界や共有状態に触る境界です。\n\n"
        "Haskellの `async` やSTMは、並行処理を場当たり的なスレッド操作ではなく、構造化された計算やトランザクションとして扱うための道具です。"
        "成功時だけでなく、例外、キャンセル、競合時に意味が壊れないかを考えることが重要です。"
    ),
    16: (
        "Haskellの性能は、見た目のコード量や直感だけでは判断しにくいことがあります。"
        "遅延評価、最適化、インライン化、メモリ保持、RTSの挙動が絡むため、勘で直すと問題を悪化させることがあります。"
        "だからGHC、Core、プロファイリングを使って観察します。\n\n"
        "性能改善は、抽象を捨てることではありません。"
        "まず測定し、ボトルネックを特定し、必要な場所だけ正格性やデータ構造を調整します。"
        "Haskellらしい性能設計は、意味の明確さと測定に基づく局所的な改善の両立です。"
    ),
    17: (
        "高度な型システムは、プログラムのより細かい制約をコンパイル時に表すための道具です。"
        "GADT、Phantom Types、DataKinds、RankNTypesは、通常のADTでは表しにくい不変条件を型に押し上げられます。"
        "例えば、型安全なASTや状態遷移の段階を型で表せます。\n\n"
        "ただし、高度な型は常に良い設計を意味しません。"
        "読みにくさ、学習コスト、エラーメッセージの難しさも増えます。"
        "使うべきなのは、型で守る価値が実際にあり、チームがその意図を説明できる境界です。"
    ),
    18: (
        "実務アプリケーションでは、外部世界と内部ドメインを分けることが品質を大きく左右します。"
        "CLIの文字列、HTTPのJSON、DBの行、外部APIのレスポンスは、そのままビジネスルールの型ではありません。"
        "外部表現には欠損、形式違い、互換性、バージョン差分が含まれます。\n\n"
        "Haskellでは、外部表現を受け取り、検証し、内部ドメイン型へ変換する境界を明示します。"
        "その後のPure Coreは、検証済みの値だけを扱えるため、実装とテストが単純になります。"
    ),
    19: (
        "FFI、JavaScript、WebAssembly、Nixは、Haskellを外部環境につなぐための話題です。"
        "ここでは、Haskellの型安全性が薄くなる境界を意識する必要があります。"
        "外部言語、OS、ビルド環境、パッケージ管理は、Haskellの型だけでは完全には守れません。\n\n"
        "だからこそ、marshal、設定、再現可能ビルド、境界のテストが重要になります。"
        "外部連携はHaskellらしさの外側ではなく、Haskellの安全な中心を外部世界へ接続する設計問題です。"
    ),
    20: (
        "Haskell周辺の言語を比較する目的は、優劣を決めることではありません。"
        "純粋性、遅延評価、型クラス、Effect、実務エコシステムの違いを見ることで、Haskellがどの問題に強く、どの交換条件を選んでいるかが分かります。\n\n"
        "似た構文を持つ言語でも、設計思想は大きく違います。"
        "比較は、Haskellを相対化し、自分のプロジェクトでどの設計を採用すべきか判断するための訓練です。"
    ),
    21: (
        "Haskellの歴史と哲学は、教材の最後に添える飾りではありません。"
        "純粋性、遅延評価、型クラスは偶然に寄せ集められた機能ではなく、研究と実験の中で選ばれてきた設計です。"
        "その背景を知ると、なぜHaskellが他言語と違う形をしているのか理解しやすくなります。\n\n"
        "歴史を学ぶ目的は、過去を暗記することではありません。"
        "現在の設計判断に対して、なぜその制約があるのか、どんな問題を解こうとしているのかを説明できるようにすることです。"
    ),
    22: (
        "総合演習では、個別の知識を並べるだけでは足りません。"
        "型でドメインを設計し、純粋な中心を作り、副作用を境界に置き、失敗を型に出し、テストで仕様を固定し、性能と運用のリスクを説明する必要があります。"
        "これはHaskellを専門的に使うための統合力です。\n\n"
        "最終的に重要なのは、コードが動くことだけではありません。"
        "なぜその型にしたのか、なぜその副作用を境界に置いたのか、なぜその抽象を使ったのかを説明できることです。"
        "Haskellのプロフェッショナルな設計は、実装と説明責任が一体になっています。"
    ),
}


WHY_SHOULD_BY_PART = {
    0: "なぜなら、意味の境界を読めないまま構文だけを覚えると、後の型、Monad、IOがすべて暗記項目になるからです。最初に思想を置くことで、各機能を一つの設計判断として接続できます。",
    1: "なぜなら、副作用がどこにあるかを最初から型で読む習慣が、後の実務設計で巨大な `IO` を避ける土台になるからです。",
    2: "なぜなら、再代入や手続きの流れに頼らないことで、式の置き換え、テスト、合成、リファクタリングが安全になるからです。",
    3: "なぜなら、意味の違う値を同じ型で扱うと、誤用がレビューや運用に漏れやすいからです。型はその誤用を早い段階で止める境界になります。",
    4: "なぜなら、存在しない状態を表せる設計は、いつかその状態への対処を強制するからです。ADTは問題領域の形をコードに閉じ込めます。",
    5: "なぜなら、処理の形を名前で表せると、コードを一行ずつ追わなくても意図を読めるからです。これは保守性に直結します。",
    6: "なぜなら、遅延評価は表現力と性能リスクを同時にもたらすからです。仕組みを理解せずに使うと、便利さと危険の境界を見失います。",
    7: "なぜなら、抽象は利用者の推論を支える約束だからです。法則を守らない型クラスインスタンスは、型が合っても設計として信頼できません。",
    8: "なぜなら、合成の抽象を選ぶことは依存関係を表明することだからです。必要以上に強い抽象を使うと、設計が持つ自由度を隠してしまいます。",
    9: "なぜなら、副作用を中心に混ぜると、テスト、再利用、障害調査が難しくなるからです。境界に押し出すことで、中心の意味を安定させます。",
    10: "なぜなら、失敗可能性を隠すと、呼び出し側が対処すべき事実を知らないまま使えてしまうからです。失敗を型に出すと、扱い忘れを減らせます。",
    11: "なぜなら、公開境界を設計しないプロジェクトは、不変条件を利用者の注意に頼ることになるからです。モジュールは設計を守る壁になります。",
    12: "なぜなら、型が正しくても仕様が間違っていることはあるからです。テストは、型では表さなかった期待を実行可能な形で残します。",
    13: "なぜなら、入力処理やDSLは仕様変更が起きやすく、巨大な分岐にすると変更範囲が読みにくくなるからです。合成可能な部品に分けると進化させやすくなります。",
    14: "なぜなら、不変データの更新を場当たり的に散らすと、変更箇所と意図が追いにくくなるからです。アクセスの意図を値として扱えると再利用できます。",
    15: "なぜなら、並行処理のバグは再現しにくく、レビューだけでは見つけにくいからです。構造化された境界で危険を局所化する必要があります。",
    16: "なぜなら、性能改善は根拠がないと抽象を壊すだけになりやすいからです。測定に基づいて小さく直すことで、意味と速度を両立できます。",
    17: "なぜなら、高度な型は強力なぶん、設計意図を説明できないと負債になるからです。守る価値のある制約だけを型へ押し上げるべきです。",
    18: "なぜなら、外部表現は常に壊れたり変わったりするからです。内部モデルを守る境界を作ることで、変更の影響を閉じ込められます。",
    19: "なぜなら、外部環境との接続点はHaskellの型だけでは守りきれないからです。境界を明示し、再現性と検査を追加する必要があります。",
    20: "なぜなら、言語の選択は思想と交換条件の選択だからです。比較できると、Haskellの強みを適切な場所で使えます。",
    21: "なぜなら、背景を知らないと制約を単なる不便として扱いがちだからです。歴史を知ると、制約が何を守るためのものか説明できます。",
    22: "なぜなら、実務では個別技術だけでなく、それらを組み合わせる判断が品質を決めるからです。説明できる設計だけが長期的に保守できます。",
}


OTHER_LANGUAGE_BY_PART = {
    0: "多くの命令型言語では、まず変数を用意し、状態を変え、手順を追って結果へ進みます。Haskellでは、まず値の意味と型を固定し、副作用を境界として読む点が違います。",
    1: "他言語のHello Worldは副作用から始まります。Haskellも表示はしますが、その表示を `IO` という型に閉じ込め、純粋な計算と混ざらないようにします。",
    2: "命令型言語では代入とループが自然な表現です。Haskellでは、同じ処理を式、関数適用、合成として表すため、コードの時間的な流れより意味の流れを重視します。",
    3: "動的型や弱いドメイン型の設計では、値の意味を命名やコメントで補いがちです。Haskellでは、意味の違いを型にすることで、呼び出し側の自由を意図的に狭めます。",
    4: "他言語ではenum、nullable、文字列フラグを組み合わせることがあります。HaskellのADTは、直和と直積で状態空間を直接設計する点が特徴です。",
    5: "forループ中心の言語では、処理手順を細かく追います。Haskellでは、map、filter、foldによって処理の種類を先に宣言します。",
    6: "多くの言語は正格評価を基本とし、式はすぐ評価されます。Haskellでは必要になるまで評価しないため、制御構造やデータ生成の考え方が変わります。",
    7: "OOPのインターフェースはオブジェクトの振る舞いに注目しがちです。Haskellの型クラスは値と型の関係、そして法則に基づく推論を重視します。",
    8: "他言語では例外、null、Promise、コールバックなどが別々に見えます。Haskellでは文脈付き計算の合成として共通の構造を見ます。",
    9: "多くのアプリでは入出力、検証、ビジネスルールが同じ関数に混ざりがちです。Haskellでは `IO` の境界を手がかりに、混ざった責任を分離します。",
    10: "例外中心の設計では、関数の型だけでは失敗が見えないことがあります。Haskellでは失敗を戻り値の型へ出し、利用者に処理を促します。",
    11: "他言語のモジュールは名前空間として使われることも多いですが、Haskellでは公開リストが不変条件を守る設計手段になります。",
    12: "型の弱い環境ではテストが多くの構造的な問題も背負います。Haskellでは型が構造を、テストが振る舞いを主に担当するように役割分担できます。",
    13: "正規表現や巨大なif文で入力を処理する設計に比べ、Haskellのパーサー/DSLは小さな意味単位を合成して大きな言語を作ります。",
    14: "ミュータブルなオブジェクトなら深い更新も直接代入できます。Haskellでは不変性を保つため、更新の意図を明示的な変換として扱います。",
    15: "共有ミュータブル状態をロックで守る設計に比べ、Haskellでは純粋計算を広く保ち、必要な共有だけをSTMなどで局所化します。",
    16: "低レベル言語では手動制御が前面に出ます。Haskellでは高水準の意味を保ちながら、必要な箇所だけGHCやRTSの情報で調整します。",
    17: "多くの言語では実行時チェックやテストで守る制約を、Haskellでは型レベルへ移せる場合があります。ただし、その分だけ説明コストも増えます。",
    18: "動的なWebアプリでは外部JSONをそのまま内部で回すことがあります。Haskellでは境界で検証し、内部ではより狭いドメイン型を使います。",
    19: "外部連携ではどの言語でも型の外へ出ます。Haskellでは、その外へ出る場所を明示し、純粋で型安全な中心を守る意識が特に強くなります。",
    20: "似た構文の言語でも、評価戦略、Effect、型推論、エコシステムは違います。Haskellとの比較では、表面より設計上の約束を見ます。",
    21: "多くの実務言語は産業上の要求から進化しました。Haskellは研究言語としての背景が強く、言語設計上の実験が実務にも影響しています。",
    22: "他言語でも設計原則は重要ですが、Haskellでは型、純粋性、効果の分離が言語機能として強く支援します。その支援を使い切ることが目標です。",
}


def term_lines(ch: Chapter) -> str:
    lines = []
    for term in ch.terms:
        explanation = TERM_EXPLANATIONS.get(term, TERM_FALLBACKS[ch.part].format(term=term))
        lines.append(f"- `{term}`: {explanation}")
    return "\n".join(lines)


def key_term(ch: Chapter) -> str:
    preferred = {
        10: "newtype",
        24: "Applicative",
        25: "Monad",
        26: "do",
        28: "Pure Core",
        31: "bottom",
        32: "DomainError",
        33: "module",
        36: "Hspec",
        37: "QuickCheck",
        43: "GHC",
        53: "servant",
        70: "DSL",
    }
    return preferred.get(ch.number, ch.terms[0])


def official_link(ch: Chapter) -> str:
    if ch.number in {1, 2, 34, 35, 43}:
        return "- Haskell Downloads: https://www.haskell.org/downloads/\n- GHC User's Guide: https://ghc.gitlab.haskell.org/ghc/doc/users_guide/"
    if ch.number in {36, 37}:
        return "- QuickCheck: https://hackage.haskell.org/package/QuickCheck\n- Cabal: https://www.haskell.org/cabal/"
    if ch.number in {56, 57}:
        return "- Haskell 2010 Report: https://www.haskell.org/definition/haskell2010.pdf\n- GHC User's Guide: https://ghc.gitlab.haskell.org/ghc/doc/users_guide/"
    return "- Haskell 2010 Report: https://www.haskell.org/definition/haskell2010.pdf\n- GHC User's Guide: https://ghc.gitlab.haskell.org/ghc/doc/users_guide/"


def extra_guidance(ch: Chapter) -> str:
    if ch.number == 0:
        return """
## この章だけの読み方

この章では、まだ多くの構文を覚えなくて構いません。注目するのは次の分離です。

```text
double :: Int -> Int
main   :: IO ()
```

`double` は純粋な関数です。同じ `21` を渡せば、常に `42` を返します。一方で `main` は外界に結果を表示する計算です。Haskellの設計では、まずこの二つを混ぜない感覚を作ります。

Dockerで進めている場合は、リポジトリルートから次を実行できます。

```bash
docker-compose run --rm tutorial runghc chapters/part_00_foundations/chapter_00_what_is_haskell/examples/Main.hs
```
"""
    if ch.number == 1:
        return """
## `IO ()` をどう読むか

`main = putStrLn "Hello, World!"` は「文字列を出力せよ」という命令文ではなく、`IO ()` という型の値を `main` という名前に束縛しています。

```text
putStrLn "Hello, World!" :: IO ()
```

`()` は意味のある値を返さないことを表します。重要なのは、Haskellが「外界に触る計算」を `IO` として型に出している点です。これにより、純粋な関数と副作用のある計算をレビュー時にも区別できます。

Dockerで進めている場合:

```bash
docker-compose run --rm tutorial runghc chapters/part_01_hello_world/chapter_01_hello_world/examples/Main.hs
```
"""
    if ch.number == 2:
        return """
## GHCiで実際に型を見る

対話環境に入るには次を実行します。

```bash
docker-compose run --rm tutorial ghci
```

GHCiが起動したら、次を入力します。

```text
:t map
:t filter
:t putStrLn
:info Maybe
```

見るべき点は、関数名ではなく矢印 `->` の並びです。`map :: (a -> b) -> [a] -> [b]` は「`a` を `b` に変える関数」と「`a` のリスト」を受け取り、「`b` のリスト」を返す、と読めます。
"""
    return ""


def professional_questions(ch: Chapter) -> str:
    questions = [
        f"`{key_term(ch)}` は、この例でどの間違いを防いでいるか。",
        "型注釈だけを見て、入力、出力、失敗可能性をどこまで説明できるか。",
        "純粋な計算と外界に触る計算の境界はどこにあるか。",
        "この設計を大きなアプリに入れるなら、どのモジュール境界に置くか。",
    ]
    if ch.part in {6, 16}:
        questions.append("遅延評価や性能上の不安があるなら、何を測定すべきか。")
    if ch.part in {18, 22}:
        questions.append("この設計を運用するなら、ログ、エラー、テスト、ドキュメントのどれを追加するか。")
    return "\n".join(f"- {q}" for q in questions)


def design_philosophy_section(ch: Chapter) -> str:
    return f"""
## 背景と設計思想

{PHILOSOPHY_BY_PART[ch.part]}

この章で扱う `{key_term(ch)}` は、単体のテクニックではなく、この思想をコード上の判断に落とすための入口です。関数名や演算子を覚えるだけでなく、その概念がどの不安を減らし、どの設計上の責任を明示しているのかを読んでください。

## なぜそうすべきなのか

{WHY_SHOULD_BY_PART[ch.part]}

実務では、短く書けることよりも、後から読んだ人が安全に変更できることの方が重要です。Haskellでは、型、純粋性、合成、副作用の境界を使って「どこを変えてよいか」「何を壊してはいけないか」をコードそのものに残します。

## 他言語的な発想との違い

{OTHER_LANGUAGE_BY_PART[ch.part]}

既に他の言語を知っているほど、最初はHaskellの書き方が遠回りに見えます。しかし多くの場合、その遠回りに見える部分が、後で仕様変更、テスト、並行実行、運用障害に向き合うときの足場になります。
"""


BAD_GOOD_BY_PART = {
    0: ("既存言語の手順をHaskell構文へ直訳する。", "まず型、純粋な意味、副作用の境界を分けて読む。"),
    1: ("`main` の中に全ての処理を詰め込む。", "小さな純粋関数を作り、`main` は表示や入力だけに近づける。"),
    2: ("値を書き換えるつもりで処理を追う。", "式が別の式へ置き換わる変換として読む。"),
    3: ("同じ `String` や `Int` で意味の違う値を混ぜる。", "`newtype` やADTで意味を分け、誤用を型で防ぐ。"),
    4: ("文字列フラグやnullable相当の値で状態を表す。", "ADTで取りうる状態だけを表し、パターンマッチで網羅する。"),
    5: ("すべてを手書き再帰で処理する。", "処理の形が変換、選別、畳み込みのどれかを先に見る。"),
    6: ("遅延評価なら大きなデータも常に安全だと考える。", "必要な評価量と保持されるサンクを観察し、必要なら正格化する。"),
    7: ("型クラスを便利なメソッド集としてだけ使う。", "インスタンスが守るべき法則と利用者の期待を明文化する。"),
    8: ("Monadを副作用の別名として覚える。", "依存する計算を合成する抽象として、MaybeやEitherでも読む。"),
    9: ("アプリ全体を `IO` の巨大な手続きにする。", "Pure Coreを厚くし、Effectful Shellを薄く保つ。"),
    10: ("`head`、`read`、`fromJust` で失敗を隠す。", "`Maybe`、`Either`、ドメインエラー型で失敗を設計に出す。"),
    11: ("全部を一つのファイルで公開する。", "モジュールのexport listで不変条件を守る。"),
    12: ("コンパイルが通ることだけを正しさとみなす。", "例ベースとプロパティベースのテストで仕様を固定する。"),
    13: ("入力処理を巨大な条件分岐にする。", "小さなパーサーやDSLノードを合成して読む。"),
    14: ("ネストした更新を場当たり的なレコード更新で散らす。", "更新対象を明示し、必要な範囲だけ合成可能にする。"),
    15: ("共有状態をロックと気合いで守る。", "構造化並行やSTMで失敗と整合性の境界を狭める。"),
    16: ("性能問題を直感で直す。", "GHCオプション、RTS、プロファイルで測定してから変更する。"),
    17: ("高度な型を使うこと自体を目的にする。", "防げる誤用と読みにくさの交換条件を評価する。"),
    18: ("JSONやDB行を内部ドメインとして直接使う。", "外部表現、変換、内部モデルを分ける。"),
    19: ("外部環境との境界を型なしの文字列や慣習に任せる。", "marshal、設定、ビルド環境を明示的な境界として扱う。"),
    20: ("構文の似ている/違うだけで言語を比較する。", "評価戦略、型、Effect、運用の違いで比較する。"),
    21: ("Haskellの特徴を癖や好みとして片付ける。", "歴史的な問題設定と設計上の狙いから読む。"),
    22: ("抽象だけ、性能だけ、運用だけを個別に最適化する。", "型、効果、性能、テスト、運用を一つの設計判断として説明する。"),
}


STUMBLE_BY_PART = {
    0: "最初は構文を全部理解しようとせず、純粋な値と `IO` の境界だけを読んでください。",
    1: "`IO ()` は実行済みの結果ではなく、外界に触る計算の値です。",
    2: "Haskellの `=` は再代入ではなく、名前と意味の束縛です。",
    3: "型注釈はコンパイラへの説明であると同時に、レビューする人への仕様です。",
    4: "パターンマッチで分岐が増えるのは冗長さではなく、状態を明示した結果です。",
    5: "自前再帰を書く前に、標準関数で意図を表せないか確認してください。",
    6: "遅延評価は便利ですが、メモリ使用量を見なくてよい理由にはなりません。",
    7: "インスタンスはコンパイルできるだけでなく、利用者が期待する法則を守る必要があります。",
    8: "`do` は命令列に見えますが、モナド合成の構文です。",
    9: "`IO` をなくすのではなく、境界へ追いやって小さくします。",
    10: "失敗を隠す関数は、型で表せる問題を実行時へ押し戻します。",
    11: "モジュール分割は整理整頓ではなく、不変条件の公開境界です。",
    12: "テストは型の代わりではなく、型では表せない振る舞いの補助線です。",
    13: "パーサーやDSLは大きく作らず、小さな部品の合成として育てます。",
    14: "Lens系の抽象は、まず素朴なADT更新を理解してから導入します。",
    15: "並行処理では成功時だけでなく、例外時とキャンセル時の境界も考えます。",
    16: "最適化は推測ではなく、測定結果に名前を付ける作業です。",
    17: "高度な型は説明責任も増やします。チームが読める設計か確認してください。",
    18: "外部データの都合を内部モデルへ直接持ち込まないでください。",
    19: "外部連携では型安全性が薄くなる場所を境界としてレビューします。",
    20: "他言語比較は優劣ではなく、設計上の交換条件を読む練習です。",
    21: "歴史や哲学は飾りではなく、現在の設計判断の理由です。",
    22: "総合演習では、動くことより設計判断を説明できることを重視します。",
}


def bad_good_section(ch: Chapter) -> str:
    bad, good = BAD_GOOD_BY_PART[ch.part]
    return f"""
## 悪い設計からHaskellらしい設計へ

悪い出発点:

```text
{bad}
```

この章で目指す形:

```text
{good}
```

変更するときは、コードが短くなるかよりも、**どの不正状態や誤用が表現できなくなったか** を説明してください。Haskellらしさは記号の多さではなく、意味の境界が型と関数に現れていることです。
"""


def stumble_text(ch: Chapter) -> str:
    return f"""```text
Q. この章で最初に見るべき場所はどこですか？
A. まずトップレベル定義の型を見ます。型から入力、出力、失敗可能性、副作用の有無を読みます。

Q. つまずいたら何を小さくすればよいですか？
A. 具体型、純粋関数、短い入力例に戻します。抽象を理解する前に、値がどう変わるかを観察します。

Q. この章でありがちな誤解は何ですか？
A. {STUMBLE_BY_PART[ch.part]}
```"""


def readme(ch: Chapter) -> str:
    example_file = "examples/Main.hs"
    return f"""
# 第{ch.number}章: {ch.title}

## この章でできるようになること

この章の目的は、**{ch.focus}** ことです。

Haskellでは構文を覚えるだけでは足りません。値、型、副作用、合成、法則のどれを今扱っているのかを意識すると、短いコードでも設計の意図が読めるようになります。

## まず知るべき言葉

{term_lines(ch)}

## なぜこれを学ぶのか

{WHY_BY_PART[ch.part]}

{PITFALL_BY_PART[ch.part]}

この章では、`{key_term(ch)}` を中心に、目の前のコードを「何を実行するか」ではなく「どんな値を作り、どんな型で制約し、どんな計算として合成するか」という観点で読みます。

{design_philosophy_section(ch)}

## 手順 1: 例を読む

この章では `{example_file}` の次のコードを読みます。写経する場合は、型注釈を先に読み、出力を予想してから実行してください。

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

{extra_guidance(ch)}

{bad_good_section(ch)}

## プロの設計判断

Haskellでは、便利だからそう書くのではなく、意味を狭めるために型や抽象を使います。意味を狭めると、呼び出し側が間違えにくくなり、コンパイラが設計の一部を検査できます。

次の問いに答えてください。

{professional_questions(ch)}

## よくあるつまずき

{stumble_text(ch)}

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

## 1. 最小変更で観察する

`examples/Main.hs` を一箇所だけ変更し、`{ch.focus}` という観点で何が変わったかを説明してください。変更前に出力を予想してから実行します。

## 2. 型から仕様を読む

サンプル内のトップレベル定義をすべて抜き出し、型が説明している仕様を書いてください。型だけでは分からない仕様も一つ挙げます。

## 3. わざと悪い設計にする

この章の考え方を使わない書き方を一つ考え、どんな誤用やバグが起きやすくなるかを書いてください。

例: `newtype` を `type` に戻す、`Maybe` を部分関数に戻す、純粋関数を `IO` の中に埋め込む、など。

## 4. 設計判断を書く

「{ch.focus}」を、次の形式で短く説明してください。

```text
この章の設計は ______ を型または関数の境界で明示する。
それにより ______ という誤用を防ぐ。
ただし実務では ______ とのトレードオフがある。
```

## 提出物

```text
1. 変更したコード
2. 実行結果または期待結果
3. 型から読み取れる仕様
4. わざと悪くした設計と、その問題点
5. この章の設計判断
```

## 進級チェック

```text
□ {key_term(ch)} を、この章のコードと結びつけて説明できる
□ サンプルの型注釈を読める
□ 純粋関数とIOアクションを区別できる
□ この章の設計を使わない場合の失敗を説明できる
```
"""


def solution(ch: Chapter) -> str:
    bad, good = BAD_GOOD_BY_PART[ch.part]
    return f"""
# 第{ch.number}章 Solution Guide: {ch.title}

## 観察の答え方

この章の例は、`{key_term(ch)}` を使って **{ch.focus}** ことを確認するための最小コードです。出力だけを写すのではなく、どの定義が純粋で、どの定義が `IO` の境界にあるかを説明します。

## 型から読む仕様

型注釈がある定義は、入力、出力、失敗可能性、副作用の有無を明示しています。型だけで分からないことは、値の範囲、性能、外部システムの状態、利用者に見せるエラーメッセージです。

## 悪い設計の例

```text
{bad}
```

この形は短く見えても、レビュー時に「何が起きうるか」を型から読みにくくします。誤用がコンパイル後や運用時に見つかるなら、Haskellの強みを活かせていません。

## 改善の方向

```text
{good}
```

模範解答では、コード量よりも境界の明確さを優先します。`String`、`Int`、巨大な `IO`、部分関数、文字列フラグが出てきたら、型、ADT、`Maybe`、`Either`、小さな純粋関数へ置き換えられないか検討します。

## なぜこの設計判断を選ぶのか

{WHY_SHOULD_BY_PART[ch.part]}

別案として、慣れた言語のように手続き、例外、文字列フラグ、巨大な入出力関数で書くこともできます。短期的にはその方が速く見える場合があります。しかし、型に現れない前提はレビューで見落とされやすく、テストしにくく、仕様変更時に壊れやすくなります。

この章の解答では、動くコードだけでなく、**なぜその境界にしたのか** を説明できることを合格基準にします。

## レビュー観点

```text
□ {key_term(ch)} を使う理由を説明している
□ 型が防ぐ誤用と、型だけでは防げない仕様を分けている
□ Pure Core と Effectful Shell の境界を指摘している
□ 実務で追加すべきテスト、ログ、ドキュメントを一つ挙げている
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
{rows}

## 10/10教材としての使い方

- [CHECKPOINTS.md](CHECKPOINTS.md) で到達段階ごとの進級条件を確認します。
- [glossary.md](glossary.md) で用語をコード例、誤解、関連章と一緒に確認します。
- 各章の `solutions.md` は、答え合わせではなく設計レビューの観点として使います。
- [projects/capstone](projects/capstone) で、型安全な小規模アプリを設計、実装、テストします。

## Dockerで始める

```bash
docker-compose build tutorial
docker-compose run --rm tutorial cabal build all
docker-compose run --rm tutorial runghc chapters/part_01_hello_world/chapter_01_hello_world/examples/Main.hs
docker-compose run --rm tutorial cabal test all
```

ローカルのGHC/Cabalを入れずに進められます。Docker内のGHC 9.10.3で、`cabal build all` と全章の `examples/Main.hs` を実行確認する方針です。

GHCupを使う場合は `START_HERE.md` の環境構築手順を参照してください。
"""


def start_here() -> str:
    return """
# START HERE

## 今日やること

1. DockerまたはGHCupでHaskellを実行できる状態にする。
2. 第0章で思想を読む。
3. 第1章の `Hello, World!` を実行する。
4. 第2章でGHCiの `:t` を使い、型を見る習慣を作る。

## Dockerで始める

ローカル環境を汚したくない場合はDockerで進めます。

```bash
docker-compose build tutorial
docker-compose run --rm tutorial cabal build all
docker-compose run --rm tutorial runghc chapters/part_01_hello_world/chapter_01_hello_world/examples/Main.hs
docker-compose run --rm tutorial ghci
```

コンテナ内で章を進める場合:

```bash
docker-compose run --rm tutorial bash
cd chapters/part_01_hello_world/chapter_01_hello_world
runghc examples/Main.hs
```

## GHCupで始める

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
solutions.md で設計観点を確認する
進級チェックに答える
公式docsを確認する
```

## 到達チェック

詳しい進級条件は [CHECKPOINTS.md](CHECKPOINTS.md) を使います。第0部から第5部までは基礎語彙、第6部から第12部までは型と仕様、第13部以降は実務設計と運用判断を確認します。

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
    terms = [
        ("純粋関数", "同じ入力に対して同じ出力を返し、外界を勝手に変えない関数。", "double x = x * 2", "ランダム値や現在時刻を勝手に読む関数は純粋ではありません。", "第0章, 第4章"),
        ("参照透過性", "式をその値で置き換えても意味が変わらない性質。", "double 21 == 42", "表示やファイル書き込みは同じ置き換えでは読めません。", "第4章"),
        ("IO", "外界とやり取りする計算を表す型。", "putStrLn \"hi\" :: IO ()", "`IO` は命令済みの結果ではなく、実行される計算の値です。", "第1章, 第27章"),
        ("型推論", "明示しない型をコンパイラが推測する仕組み。", ":t map", "型を書かなくてよいことと、型を読まなくてよいことは違います。", "第2章, 第8章"),
        ("newtype", "実行時コストを増やさず、意味の違う型を作る構文。", "newtype Email = Email String", "`type Email = String` は誤用を防ぎません。", "第10章"),
        ("代数的データ型", "直和と直積でドメインの形を表すデータ型。", "data Status = Draft | Published", "文字列フラグより、取りうる状態を型で閉じる方が安全です。", "第11章"),
        ("パターンマッチ", "データ型の形に従って値を分解する方法。", "case value of Just x -> x", "網羅性警告は設計の見落としを知らせます。", "第12章"),
        ("Maybe", "値がない可能性を表す型。", "safeHead [] == Nothing", "`null` の代用品ではなく、失敗可能性を明示する型です。", "第13章"),
        ("Either", "成功値か失敗理由のどちらかを表す型。", "Either RegistrationError User", "左側にただの `String` を置くと、機械的に扱いにくくなります。", "第14章, 第32章"),
        ("型クラス", "複数の型に共通する操作を法則付きで表す仕組み。", "class Render a where render :: a -> String", "OOPの継承と同じものとして読むと、法則の役割を見落とします。", "第20章"),
        ("Functor", "文脈を壊さず中身だけ変換する抽象。", "fmap (+1) (Just 1)", "文脈を変えるならFunctorでは表せません。", "第23章"),
        ("Applicative", "独立した文脈付き計算を組み合わせる抽象。", "(+) <$> Just 1 <*> Just 2", "前の結果で次を選ぶ場合はMonadが必要です。", "第24章"),
        ("Monad", "前の結果に応じて次の計算を選ぶ抽象。", "parse s >>= validate", "副作用専用の概念ではありません。", "第25章"),
        ("遅延評価", "値が必要になるまで評価しない評価戦略。", "take 5 [1..]", "常に高速または省メモリになるわけではありません。", "第18章"),
        ("正格性", "値をどこまで先に評価するかに関する性質。", "go !acc xs", "正格にすれば常に良いわけではなく、測定が必要です。", "第19章, 第45章"),
        ("Pure Core", "ビジネスルールを純粋関数として置く中心部分。", "normalize :: Text -> Text", "`IO` を消すことではなく、境界へ集めることが目的です。", "第28章"),
        ("Effectful Shell", "ファイル、DB、HTTP、ログなど外界とのやり取りを受け持つ外側。", "main = readFile path >>= ...", "外側が厚すぎるとテストと変更が難しくなります。", "第28章"),
        ("bottom", "実行時エラーや非停止など、正常な値を返さない計算。", "head []", "型があるように見えても、実行時に値を返さないことがあります。", "第31章"),
        ("ReaderT", "環境を読む計算を他の文脈と組み合わせる道具。", "ReaderT Env IO a", "全ての依存をReaderTに入れると境界が曖昧になります。", "第29章, 第30章"),
        ("GADT", "コンストラクタごとにより細かい戻り型を書けるデータ型。", "data Expr a where Lit :: Int -> Expr Int", "通常のADTで十分な場所に使うと読みにくくなります。", "第47章"),
    ]
    sections = []
    for name, definition, example, mistake, related in terms:
        sections.append(f"""## {name}

{definition}

```haskell
{example}
```

なぜ重要か: この概念は、Haskellのコードを単なる関数呼び出しではなく、意味、制約、合成、副作用の境界として読むための足場です。

よくある誤解: {mistake}

関連章: {related}""")
    return "# Glossary\n\n" + "\n\n".join(sections)


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
  exposed-modules:
    Tutorial.Capstone
    Tutorial.Core
  hs-source-dirs: src
  build-depends: base >=4.18 && <5

executable capstone
  import: warnings
  main-is: Main.hs
  hs-source-dirs: app
  build-depends: base >=4.18 && <5, haskell-complete-tutorial

test-suite tutorial-tests
  import: warnings
  type: exitcode-stdio-1.0
  main-is: Main.hs
  hs-source-dirs: test
  build-depends: base >=4.18 && <5, haskell-complete-tutorial
"""


def checkpoints() -> str:
    return """
# Checkpoints

このファイルは、23部/71章を Level 0-9 相当の到達段階として確認するための進級表です。章を読んだ量ではなく、設計判断を説明できるかで進みます。

| Level | 対象 | 到達条件 |
| --- | --- | --- |
| 0 Philosophy | 第0部 | Haskellを「手順」ではなく「意味、型、副作用の境界」として説明できる |
| 1 First Touch | 第1部 | DockerでHello Worldを実行し、`main :: IO ()` を説明できる |
| 2 Expressions | 第2部-第5部 | 束縛、関数、ADT、再帰、foldを使い、純粋な変換を書ける |
| 3 Type Design | 第3部-第4部, 第10部 | `newtype`、`Maybe`、`Either` で不正状態と失敗を型に出せる |
| 4 Laziness and Laws | 第6部-第8部 | 遅延評価、型クラス法則、Functor/Applicative/Monadの使い分けを説明できる |
| 5 Effects | 第9部 | Pure Core / Effectful Shellで小さなアプリを分割できる |
| 6 Specification | 第12部 | 例ベーステストと性質ベーステストの役割を分けて使える |
| 7 Integration | 第13部-第18部 | CLI/API/DB/JSON境界で外部表現と内部モデルを分けられる |
| 8 Operations | 第15部-第19部 | 並行性、性能、FFI、再現可能ビルドの運用上のリスクを説明できる |
| 9 Professional | 第20部-第22部 | capstoneを設計、実装、テストし、トレードオフをレビューできる |

## 思想面の到達条件

```text
□ なぜHaskellが純粋性を重視するのか説明できる
□ なぜ型で不正状態を表現不能にするのか説明できる
□ なぜ副作用を `IO` と境界へ分けるのか説明できる
□ なぜ遅延評価が表現力と性能リスクの両方を持つのか説明できる
□ なぜ型クラスやMonadが単なる便利機能ではなく、合成と推論の道具なのか説明できる
□ なぜHaskellらしい設計が、他言語の手続き的設計と違う形になるのか説明できる
```

## 進級レビューの形式

```text
1. この段階で防げるようになった誤用
2. 型で表した仕様
3. 型では表せないためテストした仕様
4. 副作用の境界
5. 実務で残る運用リスク
6. なぜその設計を選ぶべきか
7. 他の設計を選んだ場合に増えるリスク
```

## Capstone合格条件

```text
□ ドメイン型が `String` や `Int` の裸の値を減らしている
□ 入力検証が `Either AppError a` として表れている
□ Pure Coreを直接テストできる
□ `main` は入出力と表示に近い薄い層になっている
□ エラー、ログ、テスト、ドキュメントの追加方針を説明できる
```
"""


def capstone_module() -> str:
    return """
module Tutorial.Capstone
  ( AppError(..)
  , Priority(..)
  , Task(..)
  , TaskInput(..)
  , parsePriority
  , mkTaskInput
  , buildTask
  , renderTask
  , runWorkflow
  ) where

import Data.Char (isSpace, toLower)

data Priority = Low | Normal | High
  deriving (Eq, Show)

data TaskInput = TaskInput
  { inputTitle :: String
  , inputPriority :: Priority
  }
  deriving (Eq, Show)

data Task = Task
  { taskId :: Int
  , taskTitle :: String
  , taskPriority :: Priority
  }
  deriving (Eq, Show)

data AppError
  = EmptyTitle
  | UnknownPriority String
  | InvalidTaskId Int
  deriving (Eq, Show)

parsePriority :: String -> Either AppError Priority
parsePriority raw =
  case map toLower (trim raw) of
    "low" -> Right Low
    "normal" -> Right Normal
    "high" -> Right High
    other -> Left (UnknownPriority other)

mkTaskInput :: String -> String -> Either AppError TaskInput
mkTaskInput rawTitle rawPriority = do
  title <- nonEmptyTitle rawTitle
  priority <- parsePriority rawPriority
  Right (TaskInput title priority)

buildTask :: Int -> TaskInput -> Either AppError Task
buildTask ident input
  | ident <= 0 = Left (InvalidTaskId ident)
  | otherwise = Right (Task ident (inputTitle input) (inputPriority input))

renderTask :: Task -> String
renderTask task =
  "#" ++ show (taskId task)
    ++ " [" ++ renderPriority (taskPriority task) ++ "] "
    ++ taskTitle task

runWorkflow :: Int -> String -> String -> Either AppError String
runWorkflow ident title priority = do
  input <- mkTaskInput title priority
  task <- buildTask ident input
  Right (renderTask task)

nonEmptyTitle :: String -> Either AppError String
nonEmptyTitle raw =
  case trim raw of
    "" -> Left EmptyTitle
    title -> Right title

renderPriority :: Priority -> String
renderPriority Low = "low"
renderPriority Normal = "normal"
renderPriority High = "high"

trim :: String -> String
trim = dropWhileEnd isSpace . dropWhile isSpace

dropWhileEnd :: (a -> Bool) -> [a] -> [a]
dropWhileEnd predicate = reverse . dropWhile predicate . reverse
"""


def capstone_main() -> str:
    return """
module Main where

import Tutorial.Capstone (runWorkflow)

main :: IO ()
main =
  case runWorkflow 1 " Write tutorial review " "high" of
    Left err -> putStrLn ("error: " ++ show err)
    Right rendered -> putStrLn rendered
"""


def capstone_readme() -> str:
    return """
# Capstone Project: 型安全なタスク処理アプリ

このプロジェクトは、チュートリアル全体の考え方を小さな実務アプリにまとめる最終演習です。目的は機能の多さではなく、型、純粋性、副作用、エラー、テストの境界を説明できることです。

## 実行

```bash
docker-compose run --rm tutorial cabal run capstone
docker-compose run --rm tutorial cabal test all
```

期待する出力:

```text
#1 [high] Write tutorial review
```

## 設計

- `TaskInput` は外部入力を検証した後の値です。
- `Task` はアプリ内部で扱うドメイン値です。
- `AppError` は失敗理由を文字列ではなく型として表します。
- `runWorkflow` は Pure Core なので、`IO` なしでテストできます。
- `app/Main.hs` は Effectful Shell として、結果の表示だけを担当します。

## レビュー課題

```text
1. `String` のまま扱っている値を、さらに `newtype` に分けるならどこか。
2. `AppError` を利用者向けメッセージへ変換する境界はどこに置くべきか。
3. JSONやDBを追加する場合、外部表現と内部モデルをどこで変換するか。
4. ログ、設定、テストを追加してもPure Coreを保てるか。
```
"""


def test_main() -> str:
    return """
module Main where

import Tutorial.Capstone
  ( AppError(..)
  , Priority(..)
  , parsePriority
  , runWorkflow
  )
import Tutorial.Core (coreIdea)

main :: IO ()
main = do
  assert "core idea mentions type design" ("型で設計" `contains` coreIdea)
  assert "priority parser trims and lowers" (parsePriority " HIGH " == Right High)
  assert "unknown priority is typed" (parsePriority "urgent" == Left (UnknownPriority "urgent"))
  assert "workflow renders task" (runWorkflow 7 " Ship docs " "normal" == Right "#7 [normal] Ship docs")
  assert "empty title is typed" (runWorkflow 1 "   " "low" == Left EmptyTitle)
  assert "invalid id is typed" (runWorkflow 0 "ok" "low" == Left (InvalidTaskId 0))

assert :: String -> Bool -> IO ()
assert label ok =
  if ok
    then putStrLn ("pass: " ++ label)
    else error ("failed: " ++ label)

contains :: String -> String -> Bool
contains needle haystack =
  any (needle `prefixOf`) (suffixes haystack)

prefixOf :: Eq a => [a] -> [a] -> Bool
prefixOf [] _ = True
prefixOf _ [] = False
prefixOf (x:xs) (y:ys) = x == y && prefixOf xs ys

suffixes :: [a] -> [[a]]
suffixes [] = [[]]
suffixes xs@(_:rest) = xs : suffixes rest
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

## 読み方の中心

この教材では、各章を「関数の使い方」として読みません。必ず次の順に読みます。

```text
1. その概念が生まれた背景
2. それが防ぐ誤用
3. 型や純粋性によって明示される責任
4. 他言語的な書き方との違い
5. 実務で残るトレードオフ
```

Haskellらしいコードは、見た目を短くするために特殊な記法を使っているのではありません。意味の違う値を型で分け、副作用を境界へ置き、小さな計算を法則に従って合成するため、結果として他言語と違う形になります。

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

""" + "\n\n".join(by_part)


def main() -> None:
    write(ROOT / ".gitignore", "\n".join(["dist-newstyle/", ".stack-work/", ".hie/", "*.hi", "*.o", ".DS_Store", "tmp/", "result"]) + "\n")
    write(ROOT / "README.md", root_readme())
    write(ROOT / "START_HERE.md", start_here())
    write(ROOT / "glossary.md", glossary())
    write(ROOT / "CHECKPOINTS.md", checkpoints())
    write(ROOT / "TUTORIAL.md", tutorial_index())
    write(ROOT / "cabal.project", "packages: .\n")
    write(ROOT / "haskell-complete-tutorial.cabal", cabal_file())
    write(ROOT / "src" / "Tutorial" / "Core.hs", "module Tutorial.Core where\n\ncoreIdea :: String\ncoreIdea = \"型で設計し、純粋関数で意味を書き、副作用を境界へ置く\"\n")
    write(ROOT / "src" / "Tutorial" / "Capstone.hs", capstone_module())
    write(ROOT / "app" / "Main.hs", capstone_main())
    write(ROOT / "projects" / "capstone" / "README.md", capstone_readme())
    old_placeholder = ROOT / "src" / "Tutorial" / "Placeholder.hs"
    if old_placeholder.exists():
        old_placeholder.unlink()
    write(ROOT / "test" / "Main.hs", test_main())
    for ch in CHAPTERS:
        base = chapter_dir(ch)
        write(base / "README.md", readme(ch))
        write(base / "exercises.md", exercises(ch))
        write(base / "solutions.md", solution(ch))
        write(base / "examples" / "Main.hs", sample(ch))
    print(f"generated {len(CHAPTERS)} chapters")


if __name__ == "__main__":
    main()
