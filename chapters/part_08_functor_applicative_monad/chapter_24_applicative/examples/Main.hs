module Main where

data User = User String Int deriving Show

main :: IO ()
main = print (User <$> Just "Ada" <*> Just 36)
