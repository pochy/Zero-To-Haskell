module Main where

double :: Int -> Int
double x = x * 2

main :: IO ()
main = print (double 21 == 42)
