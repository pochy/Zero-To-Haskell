module Main where

newtype Email = Email String deriving Show

mkEmail :: String -> Maybe Email
mkEmail value
  | '@' `elem` value = Just (Email value)
  | otherwise = Nothing

main :: IO ()
main = print (mkEmail "ada@example.com")
