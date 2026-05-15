module Main where

data Pipeline a = Step String a deriving Show

build :: String -> Pipeline String
build name = Step "parse -> validate -> run -> report" name

main :: IO ()
main = print (build "final project")
