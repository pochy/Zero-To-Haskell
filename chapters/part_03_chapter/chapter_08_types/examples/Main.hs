module Main where

fullName :: String -> String -> String
fullName first last = first ++ " " ++ last

main :: IO ()
main = putStrLn (fullName "Ada" "Lovelace")
