module Tutorial.Capstone
  ( AppError(..)
  , Priority(..)
  , Task(..)
  , TaskInput(..)
  , parsePriority
  , mkTaskInput
  , buildTask
  , renderTask
  , runWorkflow
  ) where

import Data.Char (isSpace, toLower)

data Priority = Low | Normal | High
  deriving (Eq, Show)

data TaskInput = TaskInput
  { inputTitle :: String
  , inputPriority :: Priority
  }
  deriving (Eq, Show)

data Task = Task
  { taskId :: Int
  , taskTitle :: String
  , taskPriority :: Priority
  }
  deriving (Eq, Show)

data AppError
  = EmptyTitle
  | UnknownPriority String
  | InvalidTaskId Int
  deriving (Eq, Show)

parsePriority :: String -> Either AppError Priority
parsePriority raw =
  case map toLower (trim raw) of
    "low" -> Right Low
    "normal" -> Right Normal
    "high" -> Right High
    other -> Left (UnknownPriority other)

mkTaskInput :: String -> String -> Either AppError TaskInput
mkTaskInput rawTitle rawPriority = do
  title <- nonEmptyTitle rawTitle
  priority <- parsePriority rawPriority
  Right (TaskInput title priority)

buildTask :: Int -> TaskInput -> Either AppError Task
buildTask ident input
  | ident <= 0 = Left (InvalidTaskId ident)
  | otherwise = Right (Task ident (inputTitle input) (inputPriority input))

renderTask :: Task -> String
renderTask task =
  "#" ++ show (taskId task)
    ++ " [" ++ renderPriority (taskPriority task) ++ "] "
    ++ taskTitle task

runWorkflow :: Int -> String -> String -> Either AppError String
runWorkflow ident title priority = do
  input <- mkTaskInput title priority
  task <- buildTask ident input
  Right (renderTask task)

nonEmptyTitle :: String -> Either AppError String
nonEmptyTitle raw =
  case trim raw of
    "" -> Left EmptyTitle
    title -> Right title

renderPriority :: Priority -> String
renderPriority Low = "low"
renderPriority Normal = "normal"
renderPriority High = "high"

trim :: String -> String
trim = dropWhileEnd isSpace . dropWhile isSpace

dropWhileEnd :: (a -> Bool) -> [a] -> [a]
dropWhileEnd predicate = reverse . dropWhile predicate . reverse
