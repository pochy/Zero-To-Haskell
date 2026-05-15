module Main where

ones :: [Int]
ones = 1 : ones

main :: IO ()
main = print (take 5 ones)
