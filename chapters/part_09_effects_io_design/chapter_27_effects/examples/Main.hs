module Main where

pureMessage :: String -> String
pureMessage name = "Hello, " ++ name

main :: IO ()
main = putStrLn (pureMessage "Ada")
