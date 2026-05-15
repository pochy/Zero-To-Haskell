module Main where

main :: IO ()
main = print (foldr (+) 0 (map (*2) [1,2,3]))
