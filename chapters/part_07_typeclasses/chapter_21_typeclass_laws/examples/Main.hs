module Main where

main :: IO ()
main = print (fmap id (Just 10) == (Just 10 :: Maybe Int))
