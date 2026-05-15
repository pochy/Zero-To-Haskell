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
