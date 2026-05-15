module Main where

main :: IO ()
main = print (map (* 2) (filter odd [1..6]))
