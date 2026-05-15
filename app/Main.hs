module Main where

import Tutorial.Capstone (runWorkflow)

main :: IO ()
main =
  case runWorkflow 1 " Write tutorial review " "high" of
    Left err -> putStrLn ("error: " ++ show err)
    Right rendered -> putStrLn rendered
