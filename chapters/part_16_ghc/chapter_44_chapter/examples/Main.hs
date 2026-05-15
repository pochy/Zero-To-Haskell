module Main where

work :: Int -> Int
work n = sum [1..n]

main :: IO ()
main = print (work 1000)
