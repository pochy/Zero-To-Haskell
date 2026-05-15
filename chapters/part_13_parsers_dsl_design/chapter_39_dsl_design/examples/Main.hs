module Main where

data Expr = Lit Int | Add Expr Expr

eval :: Expr -> Int
eval (Lit n) = n
eval (Add a b) = eval a + eval b

main :: IO ()
main = print (eval (Add (Lit 10) (Lit 32)))
