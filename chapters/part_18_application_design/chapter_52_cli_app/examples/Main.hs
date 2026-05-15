module Main where

renderTodo :: String -> String
renderTodo title = "[ ] " ++ title

main :: IO ()
main = putStrLn (renderTodo "write CLI")
