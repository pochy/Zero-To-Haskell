module Main where

import Tutorial.Capstone
  ( AppError(..)
  , Priority(..)
  , parsePriority
  , runWorkflow
  )
import Tutorial.Core (coreIdea)

main :: IO ()
main = do
  assert "core idea mentions type design" ("型で設計" `contains` coreIdea)
  assert "priority parser trims and lowers" (parsePriority " HIGH " == Right High)
  assert "unknown priority is typed" (parsePriority "urgent" == Left (UnknownPriority "urgent"))
  assert "workflow renders task" (runWorkflow 7 " Ship docs " "normal" == Right "#7 [normal] Ship docs")
  assert "empty title is typed" (runWorkflow 1 "   " "low" == Left EmptyTitle)
  assert "invalid id is typed" (runWorkflow 0 "ok" "low" == Left (InvalidTaskId 0))

assert :: String -> Bool -> IO ()
assert label ok =
  if ok
    then putStrLn ("pass: " ++ label)
    else error ("failed: " ++ label)

contains :: String -> String -> Bool
contains needle haystack =
  any (needle `prefixOf`) (suffixes haystack)

prefixOf :: Eq a => [a] -> [a] -> Bool
prefixOf [] _ = True
prefixOf _ [] = False
prefixOf (x:xs) (y:ys) = x == y && prefixOf xs ys

suffixes :: [a] -> [[a]]
suffixes [] = [[]]
suffixes xs@(_:rest) = xs : suffixes rest
