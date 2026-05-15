module Main where

viewModel :: String -> String
viewModel name = "<h1>Hello, " ++ name ++ "</h1>"

main :: IO ()
main = putStrLn (viewModel "Web")
