module Main where

newtype UserId = UserId Int deriving Show
newtype ProductId = ProductId Int deriving Show

showUser :: UserId -> String
showUser (UserId n) = "user-" ++ show n

main :: IO ()
main = putStrLn (showUser (UserId 42))
