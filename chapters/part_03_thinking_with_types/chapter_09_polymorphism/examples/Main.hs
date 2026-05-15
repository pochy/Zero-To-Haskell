module Main where

keep :: a -> a
keep x = x

main :: IO ()
main = print (keep True)
