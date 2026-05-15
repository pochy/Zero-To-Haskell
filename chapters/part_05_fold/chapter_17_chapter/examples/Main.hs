module Main where

main :: IO ()
main = print [x * 2 | x <- [1..6], odd x]
