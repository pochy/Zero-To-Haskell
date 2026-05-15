module Main where

main :: IO ()
main = print (fmap (+1) (Just 10))
